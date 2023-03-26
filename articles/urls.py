from django.urls import path
from news.views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete


urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('create/', PostCreate.as_view(), name='articles_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
]





