from django.urls import path
from .views import IndexView, BaseRegisterView


urlpatterns = [
    path('', IndexView.as_view()),
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
]




