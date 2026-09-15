from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, TemplateView
)
from .models import Product


# ✅ Главная страница — ListView
class ProductListView(ListView):
    """Главная страница: список товаров."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    queryset = Product.objects.all()  # ✅ лаконичный запрос


# ✅ Детальная страница товара — DetailView
class ProductDetailView(DetailView):
    """Страница товара."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


# ✅ Страница контактов — TemplateView
class ContactsView(TemplateView):
    """Страница контактов с обработкой POST."""
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        # Обработка формы обратной связи
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        print(f"📨 Сообщение от {name} ({email}): {message}")

        context = self.get_context_data(**kwargs)
        context['success_message'] = 'Спасибо! Ваше сообщение отправлено.'
        return render(request, self.template_name, context)


# ✅ Добавление товара — CreateView (доп. задание)
class AddProductView(CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        print(f"✅ Добавлен новый товар: {form.instance.name}")
        return super().form_valid(form)


