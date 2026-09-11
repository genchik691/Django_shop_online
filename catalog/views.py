from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Product


# ===== Контроллер для главной страницы =====
def home(request):
    """
    Контроллер главной страницы.
    Получает все товары и передаёт их в шаблон.
    """
    # ✅ Использован лаконичный запрос: Product.objects.all()
    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, 'catalog/home.html', context)


# ===== Контроллер для страницы контактов =====
def contacts(request):
    """
    Контроллер страницы контактов.
    """
    if request.method == 'POST':
        # Обработка формы (дополнительное задание)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        print(f"📨 Сообщение от {name} ({email}): {message}")

        context = {
            'success_message': 'Спасибо! Ваше сообщение отправлено.',
        }
        return render(request, 'catalog/contacts.html', context)

    return render(request, 'catalog/contacts.html')


# ===== Контроллер для детальной страницы товара =====
def product_detail(request, pk):
    """
    Контроллер страницы товара.
    ✅ Получает pk, извлекает объект через ORM и передает его в шаблон
    """
    # ✅ Извлекаем объект через ORM (get_object_or_404)
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product,
    }
    return render(request, 'catalog/product_detail.html', context)


# ===== Контроллер для добавления товара (Дополнительное задание) =====
class AddProductView(CreateView):
    """
    Контроллер для добавления нового товара.
    """
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """
        ✅ Валидная форма, поля обязательны
        ✅ Сохранение в БД
        """
        print(f"✅ Добавлен новый товар: {form.instance.name}")
        return super().form_valid(form)


