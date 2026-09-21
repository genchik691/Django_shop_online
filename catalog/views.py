from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from .models import Product
from .forms import ProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    queryset = Product.objects.all()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        print(f"📨 Сообщение от {name} ({email}): {message}")

        context = self.get_context_data(**kwargs)
        context['success_message'] = 'Спасибо! Ваше сообщение отправлено.'
        return render(request, self.template_name, context)


# ✅ Создание продукта через форму
class AddProductView(CreateView):
    model = Product
    form_class = ProductForm  # ✅ используем кастомную форму
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


# ✅ Редактирование продукта через форму
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm  # ✅ используем кастомную форму
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


# ✅ Удаление продукта
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')


