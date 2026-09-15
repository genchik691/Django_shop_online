from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Список статей
    path('', views.BlogPostListView.as_view(), name='list'),
    # Просмотр статьи
    path('<int:pk>/', views.BlogPostDetailView.as_view(), name='detail'),
    # Создание статьи
    path('create/', views.BlogPostCreateView.as_view(), name='create'),
    # Редактирование статьи
    path('<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='update'),
    # Удаление статьи
    path('<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='delete'),
]