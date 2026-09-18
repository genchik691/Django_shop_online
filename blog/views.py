from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.core.mail import send_mail
from django.conf import settings
from .models import BlogPost


# ✅ Список статей — только опубликованные
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # ✅ Фильтрация: только статьи с положительным признаком публикации
        return BlogPost.objects.filter(is_published=True)


# ✅ Просмотр статьи + счётчик просмотров
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        # ✅ Увеличиваем счётчик просмотров при открытии статьи
        obj = super().get_object(queryset)

        # Проверяем, не превысил ли счётчик 100 (для доп. задания)
        if obj.views_count == 99:
            self._send_congratulation(obj)

        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj

    def _send_congratulation(self, obj):
        """Отправка поздравления при достижении 100 просмотров."""
        try:
            send_mail(
                subject='🎉 Статья достигла 100 просмотров!',
                message=f'Поздравляем! Статья "{obj.title}" набрала 100 просмотров.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
            print(f"📧 Поздравление отправлено для статьи: {obj.title}")
        except Exception as e:
            print(f"❌ Ошибка отправки письма: {e}")


# ✅ Создание статьи
class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:list')


# ✅ Редактирование статьи
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blogpost_form.html'

    def get_success_url(self):
        # ✅ Перенаправление после редактирования на страницу просмотра
        return reverse('blog:detail', kwargs={'pk': self.object.pk})


# ✅ Удаление статьи
class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
