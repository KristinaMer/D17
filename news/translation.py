from .models import Categories, MyModel
# импортируем декоратор для перевода и класс настроек, от которого будем наследоваться
from modeltranslation.translator import register, TranslationOptions


# регистрируем модели для перевода
@register(Categories)
class CategoriesTranslationOptions(TranslationOptions):
    fields = ('cat_name',)  # поля которые надо переводить в виде кортежа


@register(MyModel)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('name',)
















