# catalog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from .models import Product
from .forms import ProductForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .services import get_products_by_category

class ProductListView(ListView):
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return get_all_published_products()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.owner != self.request.user and not self.request.user.has_perm('catalog.can_unpublish_product'):
            messages.error(self.request, 'У вас нет прав на редактирование этого товара.')
            return redirect('catalog:product_detail', pk=obj.pk)

        return obj

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.owner != self.request.user and not self.request.user.has_perm('catalog.can_unpublish_product'):
            messages.error(self.request, 'У вас нет прав на удаление этого товара.')
            return redirect('catalog:product_detail', pk=obj.pk)

        return obj


# ✅ Снятие с публикации — только модератор
@login_required
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def product_unpublish(request, pk):
    """Снятие продукта с публикации (только модератор)."""
    product = get_object_or_404(Product, pk=pk)

    if not product.is_published:
        messages.warning(request, f'Товар "{product.name}" уже не опубликован.')
        return redirect('catalog:product_detail', pk=product.pk)

    product.is_published = False
    product.save()
    messages.success(request, f'Товар "{product.name}" снят с публикации.')

    return redirect('catalog:product_detail', pk=product.pk)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    @method_decorator(cache_page(60 * 15))  # 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class CategoryProductsView(ListView):
    """Список продуктов в указанной категории."""
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs.get('category_id')
        return context
