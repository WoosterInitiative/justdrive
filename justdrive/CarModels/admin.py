from django.contrib import admin

from .models import Brand, Country, ExteriorFinish, Model, ModelYear, Trim


# Register your models here.
@admin.register(ExteriorFinish)
class ExteriorFinishAdmin(admin.ModelAdmin):
    list_display = ["name", "color_code"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "abbreviation"]


@admin.register(ModelYear)
class ModelYearAdmin(admin.ModelAdmin):
    list_display = ["year", "slug"]


class BrandInline(admin.TabularInline):
    model = Brand
    extra = 0


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "ownership"]
    inlines = [BrandInline]


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ["name", "brand"]
    filter_horizontal = ["available_model_years"]


@admin.register(Trim)
class TrimAdmin(admin.ModelAdmin):
    list_display = ["name", "model", "slug"]
