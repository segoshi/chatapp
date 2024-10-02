from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render


from .models import CustomUser,Talk
from .forms import SignUpForm, TalkForm
from django.contrib.auth.views import LoginView,LogoutView, PasswordChangeView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

class Index(TemplateView):
    template_name = "myapp/index.html"

def signup(request):
    if request.method == 'POST': 
        # フォーム送信データを受け取る
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myapp:index')

    else:
        form = SignUpForm()

    
    return render(request, "myapp/signup.html", {'form': form})

class Login(LoginView):
    template_name = 'myapp/login.html'
    next_page = 'myapp:friends'


def friends(request):
    you = request.user
    #自分以外のユーザーを取得
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
    }

    return render(request, "myapp/friends.html", context)
            





    

def talk_room(request, friend_id):
    if request.method == 'POST':
        #フォーム送信データを受け取る
        form = TalkForm(request.POST)
        if form.is_valid():
            form.save()
            context = {
                        "form":form
                        }
            return redirect(request.path)
        
    else:
        friend = CustomUser.objects.get(id=friend_id)
        you = request.user
        talks_you_to_friend = Talk.objects.filter(Q(sender=you) & Q(receiver=friend))
        talks_friend_to_you = Talk.objects.filter(Q(sender=friend) & Q(receiver=you))
        talk_query = talks_you_to_friend.union(talks_friend_to_you).order_by('-send_datetime')
        
        #senderとreceiverの値をあらかじめyouとfreindにする
        hidden_data = {"sender":you, "receiver":friend}
        form= TalkForm(hidden_data)

        context = {
        "you":you,
        "friend":friend,
        "talk_query":talk_query,
        "form":form, 
        }


    


    return render(request, "myapp/talk_room.html", context) 




#settingページ用のビュー
class Setting(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/setting_index.html'


class Logout(LogoutView):
    next_page = "myapp:index"


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

def setting_complete(request, item):

    context= {
        "item":item
    }

    return render(request, "myapp/setting/setting_complete.html", context)