from django.template.loader import render_to_string

from django.conf import settings
from .models import User, Posts, Post_Category
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed


def send_notifications(preview, pk, title, subscribers):
    html_context = render_to_string(
        'new_post_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject = title,
        body ='',
        from_email = settings.DEFAULT_FROM_EMAIL,
        to = subscribers
    )
    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@receiver(m2m_changed, sender = Post_Category)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        cat = instance.name_category.all()
        sub_user: list[str] = []
        for category in cat:
            sub_user += category.sub_user.all()

        sub_user = [i.email for i in sub_user]

        send_notifications(instance.preview(), instance.pk, instance.header, sub_user)





#@receiver(post_save, sender = Posts)
# def notify_managers_news(sender, instance, created, **kwargs):
#     if created:
#         subject = f'Новость добавлена: {instance.header} {instance.date_create.strftime("%d-%m-%Y")}'
#     else:
#         subject = f'Изменения в публикации: {instance.header} {instance.date_create.strftime("%d-%m-%Y")}'
#
#     mail_managers(
#         subject = subject,
#         message = f'{instance.header} http://127.0.0.1:8000/news/ {instance.id}'
#     )









