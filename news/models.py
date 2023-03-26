from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .resource import TYPE_SELECT
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy


class Authors(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        self.rating = 0
        for comm in Comments.objects.filter(user = self.user):
            self.rating += comm.rate_comment
        for post in Posts.objects.filter(authors = Authors.objects.get(user = self.user)):
            self.rating += post.rate_post * 3
            for comm_post in Comments.objects.filter(posts = post):
                self.rating += comm_post.rate_comment
        self.save()

    def __str__(self):
        return f'Name: {self.user.username}, Rating: {self.rating}'


class Categories(models.Model):
    cat_name = models.CharField(max_length=255, unique=True, help_text=_('category name'))
    #subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='SubscribersUsers')
    sub_user = models.ManyToManyField(User, through='SubscribersUsers')

    def __str__(self):
        return f'{self.cat_name}'

    def get_subscribers_emails(self):
        res = set()
        for user in self.subscribers.all():
            res.add(user.email)
        return res


class Posts(models.Model):
    news = 'NE'
    articles = 'AR'
    TYPE_SELECT = [(news, 'Новость'), (articles, 'Статья')]

    authors = models.ForeignKey(Authors, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=TYPE_SELECT)
    date_create = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=155, default='Unnamed')
    body = models.TextField(default='Text')
    rate_post = models.IntegerField(default=0, db_column='rating')
    name_category = models.ManyToManyField(Categories, through='Post_Category')

    @property
    def post_rating(self):
        return self.rate_post

    @post_rating.setter
    def post_rating(self, value):
        if value >= 0 and isinstance(value, int):
            self.rate_post = value
        else:
            self.rate_post = 0
        self.save()

    def like(self):
        self.rate_post += 1
        self.save()

    def dislike(self):
        self.rate_post -= 1
        self.save()

    def preview(self):
        return f'{self.body[:124]}...'

    def __str__(self):
        return f'Заголовок: {self.header}, Текст: {self.body[:20]}...'

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'posts-{self.pk}')


class Post_Category(models.Model):
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.categories.cat_name} : {self.posts.id}'


class SubscribersUsers(models.Model):
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categories = models.ForeignKey('Categories', on_delete=models.CASCADE)


class Comments(models.Model):
    text_comment = models.TextField(max_length=1500)
    date_create = models.DateTimeField(auto_now_add=True)
    rate_comment = models.IntegerField(default=0, db_column='rating')
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def rate_com(self):
        return self.rate_comment

    @rate_com.setter
    def rate_com(self, value):
        if value >= 0 and isinstance(value, int):
            self.rate_comment = value
        else:
            self.rate_comment = 0
        self.save()

    def __str__(self):
        return self.text_comment.title()

    def like(self):
        self.rate_comment += 1
        self.save()

    def dislike(self):
        self.rate_comment -= 1
        self.save()


class Appointment(models.Model):
    date = models.DateField(default=datetime.utcnow)
    user_name = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f'{self.user_name}: {self.message}'


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    kind = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='kinds',
                             verbose_name=pgettext_lazy('help text for MyModel model', 'This is the help text'))







