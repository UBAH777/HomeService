from django.urls import path
from users.views import DummyLoginView, UserRegistrationView, UserLoginView

urlpatterns = [
    path('dummyLogin/', DummyLoginView.as_view(), name='dummy-login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
]
