from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest


from .models import CustomUser,Talk
from .forms import TalkForm
from django.contrib.auth.views import  PasswordChangeView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView,CreateView
from django.views.generic import TemplateView
from django.db.models import Q, F, OuterRef, Subquery
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404



class Index(TemplateView):
    template_name = "myapp/index.html"

class Friends(LoginRequiredMixin, ListView):
    template_name = "myapp/friends.html"
    model = CustomUser
    paginate_by = 10

    #メソッドで共通して使う変数を設定
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        #検索ワードを取得
        self.searched_text = self.request.GET.get("search")
        #検索に誰もいなかった時のフラグ
        self.nobody_found = False
        #検索されたかで場合分け
        if self.searched_text:
            self.friends = CustomUser.objects.exclude(id=self.request.user.id).filter(Q(username__icontains=self.searched_text)|
                                                                   Q(email__icontains=self.searched_text))
            if not self.friends.exists():
                self.nobody_found = True
        else:
            self.friends = CustomUser.objects.exclude(id=self.request.user.id)



    def get_queryset(self, **kwargs: Any) -> dict[str, Any]:
        super().get_queryset()

        #sender,receiverでTalkを調べるためのサブクエリ
        latest_msg = Talk.objects.filter(
        Q(sender=OuterRef("pk"), receiver=self.request.user)
        | Q(sender=self.request.user, receiver=OuterRef("pk"))
    ).order_by("-send_datetime")[:1]
        

        #サブクエリを呼び出してfriendsのpkで検索
        friend_and_latest_msg = self.friends.annotate(
        latest_msg_content=Subquery(latest_msg.values('content')[:1]),
        latest_msg_datetime=Subquery(latest_msg.values('send_datetime')[:1])
        )

        #最新のメッセージの時間で並べ替え
        friend_and_latest_msg_sorted = friend_and_latest_msg.order_by(F('latest_msg_datetime').asc(nulls_first=True)).reverse()

        return friend_and_latest_msg_sorted
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        extra_context = {
            "nobody_found": self.nobody_found,
            "searched_text": self.searched_text,
            }
        context.update(extra_context)
        return context
        


class Talkroom(LoginRequiredMixin, CreateView):
    template_name = "myapp/talk_room.html"
    form_class = TalkForm
    
    #メソッドで共通して使う変数を設定
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.friend = get_object_or_404(CustomUser.objects.only("id","username"), id=self.kwargs["friend_id"])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
    
        talk_list = Talk.objects.filter(
        Q(sender_id=self.friend.id, receiver_id=self.request.user.id)
        | Q(sender_id=self.request.user.id, receiver=self.friend.id)
        ).order_by("-send_datetime")

        extra_context = {
            "friend":self.friend,
            "talk_list": talk_list,
        }
        context.update(extra_context)
        return context
        
    def form_valid(self, form):
        # sender,receiverの値を設定
        talk = form.save(commit=False)
        talk.sender = self.request.user
        talk.receiver = self.friend
        talk.save()
        return super().form_valid(form)
    

    def get_success_url(self):
        # 現在のURLにリダイレクト
        return self.request.path
        
        
    
    


#settingページ用のビュー
class Setting(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/setting_index.html'

class SettingUsername(LoginRequiredMixin, UpdateView):
    template_name = "myapp/setting/setting_username.html"
    model = CustomUser
    fields = ("username",)
    def get_success_url(self) -> str:
        return reverse("myapp:setting_complete", kwargs={"item": "ユーザー名"})
    

class SettingImage(LoginRequiredMixin, UpdateView):
    template_name = "myapp/setting/setting_image.html"
    model = CustomUser
    fields = ("user_icon_image",)
    def get_success_url(self) -> str:
        return reverse("myapp:setting_complete", kwargs={"item": "アイコン"})

class SettingEmail(LoginRequiredMixin, UpdateView):
    template_name = "myapp/setting/setting_email.html"
    model = CustomUser
    fields = ("email",)
    def get_success_url(self) -> str:
        return reverse("myapp:setting_complete", kwargs={"item": "メールアドレス"})

class SettingPassword(LoginRequiredMixin, PasswordChangeView):
    template_name = "myapp/setting/setting_password.html"
    def get_success_url(self) -> str:
        return reverse("myapp:setting_complete", kwargs={"item": "パスワード"})


class SettingComplete(TemplateView):
    template_name="myapp/setting/setting_complete.html"
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["item"] = self.kwargs["item"]
        return context
    



   
