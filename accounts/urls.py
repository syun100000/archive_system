from django.urls import path, include
from . import views
from allauth.account.views import LoginView

urlpatterns = [
    path("mypage", views.mypage, name="mypage"),
    path("mypage/report_favorite_add", views.report_favorite_add, name="report_favorite_add"),
    path("mypage/report_favorite_delete", views.report_favorite_delete, name="report_favorite_delete"),
    path("mypage/upload_favorites_add", views.upload_favorite_add, name="upload_favorite_add"),
    path("mypage/upload_favorites_delete", views.upload_favorites_delete, name="upload_favorite_delete"),
    # path("allauth", include('allauth.urls')),　これは現在アプリケーションのurls.pyに記述されている
    # path("edit_email", views.edit_email, name="edit_email"),
    # path('confirm_email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(), name='email_change_done'),
    path('email/change/complete/<str:token>/', views.EmailChangeComplete.as_view(), name='email_change_complete'),
    path("edit_name", views.edit_name, name="edit_name"),
    path("delete_account", views.delete_account, name="delete_account"),
]
