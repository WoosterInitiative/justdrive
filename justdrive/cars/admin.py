from django.contrib import admin

from .models import Car


# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["name", "model_name", "brand_name", "color_name"]

    def model_name(self, obj):
        return obj.model.name

    def brand_name(self, obj):
        return obj.model.brand.name

    def color_name(self, obj):
        return obj.color.name
