from datetime import date

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField


# Create your models here.
class BaseModel(models.Model):
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(unique=True, editable=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("users.user", on_delete=models.PROTECT)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Car(BaseModel):
    id = ShortUUIDField(length=16, primary_key=True, editable=False)
    name = models.CharField(_("nickname"), max_length=50, unique=True)
    model = models.ForeignKey("CarModels.model", on_delete=models.PROTECT)
    year = models.ForeignKey("CarModels.modelyear", on_delete=models.PROTECT)
    color = models.ForeignKey(
        "CarModels.exteriorfinish", on_delete=models.SET_NULL, blank=True, null=True
    )
    trim = models.ForeignKey(
        "CarModels.trim", on_delete=models.SET_NULL, blank=True, null=True
    )
    purchase_date = models.DateField(_("date purchased"), default=date.today)
    purchase_price = models.DecimalField(
        _("purchase price"), max_digits=14, decimal_places=2, blank=True
    )
    is_active = models.BooleanField(
        _("active"), help_text=_("e.g., if not insured"), default=True
    )
    is_archived = models.BooleanField(
        _("archived"), help_text=_("e.g., if in storage or sold")
    )
    sale_date = models.DateField(_("date sold"), blank=True, null=True)
    sale_price = models.DecimalField(
        _("sale price"), max_digits=14, decimal_places=2, blank=True, null=True
    )
    latest_mileage = models.DecimalField(
        _("latest reported mileage"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    tank_capacity = models.DecimalField(
        _("fuel tank capacity"),
        help_text=_("in gallons [blank if alternative fuel]"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    battery_capacity = models.DecimalField(
        _("battery capacity"),
        help_text=_("in kWh [blank if conventional fuel/non-EV]"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.id, allow_unicode=True)

        super().save(*args, **kwargs)

    def __str__(self):
        str_value = f"{self.name}"
        return str_value
