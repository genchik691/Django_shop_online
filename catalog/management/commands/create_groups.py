# catalog/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группы "Модератор продуктов" и "Контент-менеджер" с правами'

    def handle(self, *args, **options):
        # ===== Группа "Модератор продуктов" =====
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Право can_unpublish_product
        content_type = ContentType.objects.get_for_model(Product)
        unpublish_permission = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type
        )
        # Право на удаление продукта
        delete_permission = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )

        moderator_group.permissions.add(unpublish_permission, delete_permission)

        if created:
            self.stdout.write(self.style.SUCCESS('✅ Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Группа "Модератор продуктов" уже существует'))

        self.stdout.write(f'   Права: {unpublish_permission.name}, {delete_permission.name}')

        # ===== Группа "Контент-менеджер" (доп. задание) =====
        from blog.models import BlogPost

        content_group, created = Group.objects.get_or_create(name='Контент-менеджер')
        blog_content_type = ContentType.objects.get_for_model(BlogPost)

        blog_permissions = Permission.objects.filter(
            content_type=blog_content_type,
            codename__in=['add_blogpost', 'change_blogpost', 'delete_blogpost', 'view_blogpost']
        )
        content_group.permissions.set(blog_permissions)

        if created:
            self.stdout.write(self.style.SUCCESS('✅ Группа "Контент-менеджер" создана'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Группа "Контент-менеджер" уже существует'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Группы и права настроены!'))