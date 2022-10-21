from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns=[
    path('',views.feed,name='feed'),
    path('register/',views.register,name='register'),
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name="logout"),
    path('settings/',views.settings,name='settings'),
    path('upload/',views.uploadpost,name='upload'),
    path('likepost/',views.likepost,name='likepost'),
    path('deletepost/<str:pk>',views.deletePost,name='deletepost'),
    path('search/',views.searchuser,name='search'),
    path('commentpost/',views.likepost,name='commentpost'),
    path('userprofile/<str:pk>',views.userprofile,name='userprofile'),
    path('followercount/',views.followerunfollow,name='followercount'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='base/password_reset.html'),name='reset_password'),
    path('password_reset_sent/',auth_views.PasswordResetDoneView.as_view(template_name='base/password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='base/password_reset_form.html'),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset_done.html'),name='password_reset_complete'),
]

