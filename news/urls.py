from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from django.views.decorators.cache import cache_page

from sign.views import upgrade_me
from .views import (
    PostsList, PostDetail, PostCreate, PostUpdate,
    PostDelete, PostSearch, AppointmentView, subscribe, IndexView, Index
)

urlpatterns = [
    # path('', cache_page(60*5)(PostsList.as_view()), name='list'),
    # path('<int:pk>', cache_page(60)(PostDetail.as_view()), name='detail'),
    path('', PostsList.as_view(), name='list'),
    path('<int:pk>', PostDetail.as_view(), name='detail'),

    path('create/', PostCreate.as_view(), name='create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
    path('search/', PostSearch.as_view(), name='search'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('articles/delete', PostDelete.as_view(), name='articles_delete'),

    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),

    path('mail/', AppointmentView.as_view(template_name='appointment_created.html'), name='appointment'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', subscribe, name='unsubscribe'),
    path('sign/upgrade/', upgrade_me, name='upgrade_me'),
    #path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),

    path('', IndexView.as_view()),
    path('index/', Index.as_view(), name='index'),
]






