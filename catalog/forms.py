# catalog/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Product


# ✅ Список запрещённых слов вынесен в константу
FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта."""

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        """✅ Стилизация формы — добавление CSS-классов Bootstrap."""
        super().__init__(*args, **kwargs)

        # Стили для всех полей
        for field_name, field in self.fields.items():
            if field_name == 'is_published':
                field.widget.attrs.update({'class': 'form-check-input'})
            elif field_name == 'category':
                field.widget.attrs.update({'class': 'form-select'})
            elif field_name == 'image':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

        # Placeholder для полей
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Введите название товара'
        })
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Введите описание товара'
        })
        self.fields['price'].widget.attrs.update({
            'placeholder': 'Введите цену'
        })

    # ===== ✅ ВАЛИДАЦИЯ ЗАПРЕЩЁННЫХ СЛОВ =====
    def clean_name(self):
        """Проверка названия на запрещённые слова."""
        name = self.cleaned_data.get('name', '')
        name_lower = name.lower()

        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise ValidationError(
                    f'Слово "{word}" запрещено использовать в названии товара.'
                )
        return name

    def clean_description(self):
        """Проверка описания на запрещённые слова."""
        description = self.cleaned_data.get('description', '')
        description_lower = description.lower()

        for word in FORBIDDEN_WORDS:
            if word in description_lower:
                raise ValidationError(
                    f'Слово "{word}" запрещено использовать в описании товара.'
                )
        return description

    # ===== ✅ ВАЛИДАЦИЯ ЦЕНЫ =====
    def clean_price(self):
        """Проверка, что цена не отрицательная."""
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise ValidationError(
                'Цена не может быть отрицательной. '
                'Пожалуйста, укажите положительное число.'
            )
        return price

    # ===== ✅ ВАЛИДАЦИЯ ИЗОБРАЖЕНИЯ (доп. задание) =====
    def clean_image(self):
        """Проверка формата и размера изображения."""
        image = self.cleaned_data.get('image')

        if image:
            # Проверка формата
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError(
                    'Допустимые форматы изображений: JPEG, JPG, PNG.'
                )

            # Проверка размера (5 МБ)
            max_size = 5 * 1024 * 1024  # 5 МБ в байтах
            if image.size > max_size:
                raise ValidationError(
                    f'Размер файла не должен превышать 5 МБ. '
                    f'Ваш файл: {image.size / (1024 * 1024):.2f} МБ.'
                )

        return image
