import pytz
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.core.cache import cache

from .models import Posts, Authors, Categories, Appointment, MyModel
from .filters import PostFilter
from .forms import PostForm

from .tasks import hello, printer

from django.utils.translation import gettext as _
from django.utils.translation import activate, get_supported_language_variant
from django.utils import timezone


class IndexView(View):
    def get(self, request):
        printer.apply_async([10], eta = datetime.now() + timedelta(seconds = 5))
        hello.delay()
        return HttpResponse('Hello!')


class PostsList(ListView):
    model = Posts
    ordering = '-date_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'posts-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset = self.queryset)
            cache.set(f'posts-{self.kwargs["pk"]}, obj')
        return obj


class PostSearch(ListView):
    model = Posts
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = '-date_create'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Posts
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_now'] = datetime.utcnow()
        # context['New post is coming soon'] = None
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['user_auth'] = self.request.user.is_authenticated
        id = self.kwargs.get('pk')
        post = Posts.objects.get(pk=id)
        is_subscribersusers = True
        for cat in post.name_category.all():
            if self.request.user not in cat.sub_user.all():
                is_subscribersusers = False
        context['is_subscribersusers'] = is_subscribersusers
        return context


class PostCreate(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Posts
    template_name = 'post_create.html'
    permission_required = ('posts.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            path_info = self.request.META['PATH_INFO']
            if path_info == '/news/create/':
                post.post_type = 'NE'
            elif path_info == '/articles/create/':
                post.post_type = 'AR'
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Posts
    template_name = 'post_edit.html'
    permission_required = ('posts.change_post')


class PostDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    model = Posts
    template_name = 'post_delete.html'
    success_url = reverse_lazy('list')
    permission_required = ('posts.delete_post')


@login_required
def subscribe(request, pk):
    user = User.objects.get(pk=request.user.id)
    post = Posts.objects.get(pk=pk)
    category = post.name_category.all()
    for cat in category:
        if user not in cat.sub_user.all():
            cat.sub_user.add(user)
    return redirect('/news/')


@login_required
def unsubscribe(request, pk):
    user = User.objects.get(pk=request.user.id)
    post = Posts.objects.get(pk=pk)
    category = post.name_category.all()
    for cat in category:
        if user in cat.sub_user.all():
            cat.sub_user.remove(user)
    return redirect('/news/')


class AppointmentView(View):
    template_name = 'appointment_created.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'appointment_created.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            user_name=request.POST['user_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # отправляем письмо
        send_mail(
            subject=f'{appointment.user_name} {appointment.date.strftime("%Y-%M-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            message=appointment.message,  # сообщение с кратким описанием проблемы
            from_email='skillfactorylearning@mail.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=[]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )

        return redirect('appointments:appointment_create')


# class CategoryListView(ListView):
#     model = Posts
#     template_name = 'category_list.html'
#     context_object_name = 'category_news_list'
#
#     def get_queryset(self):
#         self.category = get_object_or_404(Categories, id = self.kwargs['pk'])
#         queryset = Posts.objects.filter(category = self.category).order_by('-date_create')
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_not_subscribers'] = self.queryset.user not in self.category.subscribers.all()
#         context['category'] = self.category
#         return context

class Index(View):
    def get(self, request):
        current_time = timezone.now()

        # Translators: This message appears on the home page only.
        models = MyModel.objects.all()

        context = {
            'models': models,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }
        return HttpResponse(render(request, 'index.html', context))

    # по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться
    # нвписанным ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')















