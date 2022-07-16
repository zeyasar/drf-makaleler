from django.contrib import admin

from news.models import Gazeteci, Makale

admin.site.register(Makale)
admin.site.register(Gazeteci)

