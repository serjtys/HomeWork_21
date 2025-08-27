from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группы и назначает права'

    def handle(self, *args, **options):
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        content_type = ContentType.objects.get_for_model(Product)

        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=['can_unpublish_product', 'delete_product', 'can_change_publish_status']
        )

        moderator_group.permissions.set(permissions)
        moderator_group.save()

        self.stdout.write(
            self.style.SUCCESS('Группы и права успешно созданы!')
        )