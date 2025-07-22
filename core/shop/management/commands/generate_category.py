from faker import Faker
from django.core.management.base import BaseCommand
from ...models import BlogCategoryModel
from django.contrib.auth import get_user_model

User= get_user_model()

class Command(BaseCommand):
    help= "This is Fake Data For Category."
    
    def handle(self, *args, **options):
        faker = Faker(locale="fa_IR")
        category= BlogCategoryModel.objects.all()
        for _ in range(10):
            name=faker.word()
            BlogCategoryModel.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS("Successfully generated 10 fake Categories..."))
