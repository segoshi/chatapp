from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest
from django.shortcuts import redirect, render


from .models import CustomUser,Talk
from .forms import SignUpForm, TalkForm
from django.contrib.auth.views import LoginView,LogoutView, PasswordChangeView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,CreateView
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy



class Index(TemplateView):
    template_name = "myapp/index.html"

class Friends(LoginRequiredMixin, ListView):
    template_name = "myapp/friends.html"
    model = CustomUser
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
        #リクエストのユーザーを取得
        you = self.request.user

        #検索ワードを取得
        searched_name = self.request.GET.get("search")
        #検索に誰もいなかった時のフラグ
        nobody_found = False
        #検索されたかで場合分け
        if searched_name:
            friends = CustomUser.objects.exclude(id=you.id).filter(username__icontains=searched_name)
            if not friends.exists():
                nobody_found = True
        else:
            friends = CustomUser.objects.exclude(id=you.id)

        #トークしたことあるかないかで分ける
        friends_havetalked = friends.filter(Q(talk_sent__receiver__pk=you.pk)|Q(talk_received__sender__pk=you.pk)).distinct()
        friends_nothavetalked = friends.exclude(Q(talk_sent__receiver__pk=you.pk)|Q(talk_received__sender__pk=you.pk)).order_by("-date_joined")




        friend_and_talk = []
        for friend in friends_havetalked:
            #自分とユーザーとのトークを取得
            talks_you_to_friend = Talk.objects.filter(Q(sender__id=you.id) & Q(receiver__id=friend.id))
            talks_friend_to_you = Talk.objects.filter(Q(sender__id=friend.id) & Q(receiver__id=you.id))
            talks_with_friend = talks_you_to_friend.union(talks_friend_to_you)
            last_talk_with_friend = talks_with_friend.latest("send_datetime")

            friend_and_talk.append([friend, last_talk_with_friend])

        #最新のトークの時間で並べかえる
        friend_and_talk.sort(key=lambda x: x[1].send_datetime, reverse=True)
            
        context = {
            "friends_havetalked":friend_and_talk,
            "friends_nothavetalked":friends_nothavetalked,
            "searched_name": searched_name,
            "nobody_found": nobody_found,
        }

        return context


class Talkroom(LoginRequiredMixin, CreateView):
    #メソッドで共通して使う変数を設定
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.friend = CustomUser.objects.get(id=self.kwargs["friend_id"])
        self.you = self.request.user

    #トーク表示部分
    template_name = "myapp/talk_room.html"
    form_class = TalkForm
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
    
        talks_you_to_friend = Talk.objects.filter(Q(sender=self.you) & Q(receiver=self.friend))
        talks_friend_to_you = Talk.objects.filter(Q(sender=self.friend) & Q(receiver=self.you))
        talk_list= talks_you_to_friend.union(talks_friend_to_you).order_by("-send_datetime")

        extra = {
            "you":self.you,
            "friend":self.friend,
            "talk_list": talk_list
        }
        context.update(extra)
        return context

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial["sender"] = self.you
        initial["receiver"] = self.friend
        return initial

    def get_success_url(self):
        # 現在のURLにリダイレクト
        return self.request.path
        
        
    
    


#settingページ用のビュー
class Setting(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/setting_index.html'

class SettingUsername(UpdateView):
    template_name = "myapp/setting/setting_username.html"
    model = CustomUser
    fields = ("username",)
    def get_success_url(self) -> str:
        return reverse("myapp:setting_complete", kwargs={"item": "ユーザー名"})
    

class SettingImage(UpdateView):
    template_name = "myapp/setting/setting_image.html"
    model = CustomUser
    fields = ("user_icon_image",)
    def get_success_url(self) -> str:
        return reverse("myapp:setting_complete", kwargs={"item": "アイコン"})

class SettingEmail(UpdateView):
    template_name = "myapp/setting/setting_email.html"
    model = CustomUser
    fields = ("email",)
    def get_success_url(self) -> str:
        return reverse("myapp:setting_complete", kwargs={"item": "メールアドレス"})

class SettingPassword(PasswordChangeView):
    template_name = "myapp/setting/setting_password.html"
    def get_success_url(self) -> str:
        return reverse("myapp:setting_complete", kwargs={"item": "パスワード"})


class SettingComplete(TemplateView):
    template_name="myapp/setting/setting_complete.html"
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["item"] = self.kwargs["item"]
        return context
    