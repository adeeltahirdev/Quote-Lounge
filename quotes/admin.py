from django.contrib import admin
from .models import Category, Quote, QuoteLike

admin.site.register(Category)
admin.site.register(Quote)
admin.site.register(QuoteLike)