import django
from django.conf import settings

settings.configure(
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/home/serj/PycharmProjects/HomeWork_21_2/skystore/catalog/templates'],
        'APP_DIRS': True,
    }]
)
django.setup()

from django.template.loader import get_template
print(get_template('catalog/home.html').origin.name)