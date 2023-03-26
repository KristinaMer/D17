from django import template

register = template.Library()

words_censor = ['редиска', 'rediska', 'Breaking', 'статья', 'смартфон']

@register.filter()
def censor(value):
    for word in words_censor:
        value = value.replace(word[1:], '*' * len(word[1:]))
    return value






