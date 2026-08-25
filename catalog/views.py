from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages


def home(request):
    """
    Контроллер главной страницы.
    Рендерит шаблон home.html.
    """
    # ✅ Рендеринг с помощью функции render()
    return render(request, 'catalog/home.html')


def contacts(request):
    """
    Контроллер страницы контактов.
    Рендерит шаблон contacts.html.
    Обрабатывает POST-запросы (форма обратной связи).
    """
    # ✅ Дополнительное задание: обработка формы
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        # Здесь можно сохранить данные в БД или отправить по email
        # Пока просто выводим в консоль (отладка)
        print(f"📨 Получена заявка от {name} ({email})")
        print(f"   Тема: {subject}")
        print(f"   Сообщение: {message[:100]}...")

        # ✅ Передаём сообщение об успешной отправке в шаблон
        success_message = "Спасибо! Ваше сообщение отправлено. Мы свяжемся с вами в ближайшее время."

        # Рендерим шаблон с сообщением об успехе
        return render(request, 'catalog/contacts.html', {
            'success_message': success_message,
        })

    # GET-запрос — просто показываем страницу
    return render(request, 'catalog/contacts.html')


from django.shortcuts import render

# Create your views here.
