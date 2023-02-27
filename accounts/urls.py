from django.urls import path

from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view()),

    path('login/', LoginView.as_view()),

    path('change-password/', ChangePasswordView.as_view()),

    path('confirm-change-password/', ConfirmChangePasswordView.as_view()),

    path('load-user/', LoadUserView.as_view()),
]
