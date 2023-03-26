from django.contrib import admin
from .models import Authors, Categories, Posts, Post_Category, Comments, MyModel
from modeltranslation.admin import TranslationAdmin


def nullfy_posts(modeladmin, request, queryset):
    queryset.update(rate_post = 0)
nullfy_posts.short_description = 'Обнулить рейтинг'

class Post_CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'posts', 'categories')
    list_filter = ['categories']

class PostsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'authors', 'post_type', 'date_create', 'header', 'body', 'rate_post')
    list_filter = ['date_create']
    search_fields = ('authors', 'header')
    actions = [nullfy_posts]

class AuthorsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'rating', 'user')

# class CategoriesAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'cat_name')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_create', 'text_comment', 'rate_comment', 'posts', 'user')



admin.site.register(Authors, AuthorsAdmin)
# admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Post_Category, Post_CategoryAdmin)
admin.site.register(Comments, CommentsAdmin)



# регистрируем модели для перевода в админке
class CategoriesTranslationAdmin(TranslationAdmin):
    model = Categories

class MyModelTranslationAdmin(TranslationAdmin):
    model = MyModel


admin.site.register(Categories, CategoriesTranslationAdmin)
admin.site.register(MyModel, MyModelTranslationAdmin)



