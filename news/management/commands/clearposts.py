from django.core.management.base import BaseCommand, CommandError

from news.models import Posts


class Command(BaseCommand):
    help = 'Удалить все публикации в категории'

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Действительно хотите удалить публиации? yes/no')
        answer = input()

        if answer == 'yes':
            Posts.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Публикации удалены успешно'))
            return

        self.stdout.write(self.style.ERROR('Доступ запрещен'))
















