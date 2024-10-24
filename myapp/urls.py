from django.urls import path
from . import views

app_name = "myapp"
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('friends', views.Friends.as_view(), name='friends'),
    path('talk_room/<int:friend_id>', views.Talkroom.as_view(), name='talk_room'),
    path('setting', views.Setting.as_view(), name='setting'),
    path('setting/username/<int:pk>/', views.SettingUsername.as_view(), name="setting_username"),
    path('setting/image/<int:pk>', views.SettingImage.as_view(), name="setting_image"),
    path('setting/email/<int:pk>', views.SettingEmail.as_view(), name="setting_email"),
    path('setting/password/<int:pk>', views.SettingPassword.as_view(), name="setting_password"),
    path('setting/complete/<str:item>', views.SettingComplete.as_view(), name="setting_complete")


]


