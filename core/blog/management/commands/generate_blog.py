# Django Imports
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from faker import Faker
from io import BytesIO
from PIL import Image
import requests
import random

# Third Party
from blog.models import BlogModel, BlogImageModel, BlogCategoryModel


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker= Faker(locale="fa_IR")
        categories=BlogCategoryModel.objects.all()
        for _ in range(10):
            title=faker.word()
            description= faker.paragraph(nb_sentences=2)
            type=faker.random_int(min=0, max=2)
            status= faker.random_int(min=0, max=2)
            selected_category=random.choice(categories)

            new_blog= BlogModel.objects.create(title=title, description=description, type=type, status=status, category=selected_category)
            image_url = f"https://picsum.photos/200/200?random={random.randint(1, 1000)}"
            response= requests.get(image_url)

            image= Image.open(BytesIO(response.content))
            image_size= len(response.content)

            if image_size > 1048576:
                image = self.resize_image(image)
            
            image_file = self.save_image(image)
            new_blog.image=image_file
            new_blog.save()

            for _ in range(5):

                image_url = f"https://picsum.photos/200/200?random={random.randint(1, 1000)}"
                response = requests.get(image_url)

                image = Image.open(BytesIO(response.content))

                image_size = len(response.content)

                if image_size > 1048576:  # 1MB
                    image = self.resize_image(image)

                image_file = self.save_image(image)
                
                BlogImageModel.objects.create(blog=new_blog, file=image_file)

            

        self.stdout.write(self.style.SUCCESS('Successfully generated 10 fake products'))



    def resize_image(self, image):
        image = image.resize((800, 800), Image.ANTIALIAS)
        return image

    def save_image(self, image):
        img_io = BytesIO()
        image.save(img_io, format="JPEG", quality=85)
        img_io.seek(0)
        return ContentFile(img_io.read(), name="image.jpg")
