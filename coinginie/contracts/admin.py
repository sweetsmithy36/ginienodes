from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Contract, Plans, Subscription

# Register your models here.
admin.site.register(Subscription)
admin.site.register(Contract)


@admin.register(Plans)
class PlanAdmin(admin.ModelAdmin):
    list_display = ["name", "min_amount", "max_amount", "profit", "duration_weeks"]
    # formfield_overrides = {
    #     models.TextField: {'widget':TinyMCE()}
    # }
