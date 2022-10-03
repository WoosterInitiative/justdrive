import datetime
import re
from locale import localeconv

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


class Country(models.Model):
    name = models.CharField(_("country name"), max_length=80, unique=True)
    abbreviation = models.CharField(
        _("abbreviation"), max_length=10, unique=True, blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("countries")

    def __str__(self):
        return self.name


today = datetime.date.today()
year = today.year
max_year = year + 2


def trim_trailing_zeros(value: (str | float)) -> str:
    if is_number(value):
        locale_seperator = localeconv()["decimal_point"]
        parts = str(value).split(locale_seperator)
        if len(parts) < 2:
            # no decimal part, return as-is
            return str(value)

        decimal = parts[1]
        decimal = decimal.rstrip("0")

        if len(decimal) > 0:
            return f"{parts[0]}.{decimal}"
        else:
            return f"{parts[0]}"


def is_number(value: (str | float)) -> bool:
    if value is None:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


class ModelYear(models.Model):
    year = models.DecimalField(
        _("model year"),
        help_text=_("may include half-year as '.5', e.g., '1998.5'"),
        max_digits=5,
        decimal_places=1,
    )
    slug = models.SlugField(unique=True, editable=False)

    # constraints = {
    #     models.CheckConstraint(
    #         check=Q(year__gte=1900), name='model_year_gte_1900'
    #     ),
    #     models.CheckConstraint(
    #         check=Q(year__lte=max_year), name='model_year_lte_current_plus_two'
    #     )
    # }

    class Meta:
        ordering = ["year"]

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_year = trim_trailing_zeros(self.year)
            slug_year = re.sub(r"\.", "_", slug_year)
            self.slug = slugify(slug_year, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        year = trim_trailing_zeros(self.year)
        return f"{year}"


class Brand(BaseModel):
    ownership = models.ForeignKey(
        "self", on_delete=models.PROTECT, blank=True, null=True
    )
    is_primary = models.BooleanField(_("is primary owner"), default=False)
    primary_country = models.ForeignKey(
        Country, verbose_name=_("primary country"), on_delete=models.PROTECT
    )

    class Meta:
        ordering = ["ownership__name", "name"]


class Model(BaseModel):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    available_model_years = models.ManyToManyField(ModelYear)

    class Meta:
        ordering = ["brand__name", "name"]
        # constraints = {
        #     models.UniqueConstraint(fields=['name','brand'], name="unique_model_name")
        # }


class ExteriorFinish(models.Model):
    name = models.CharField(_("finish name"), max_length=80, unique=True)
    color_code = models.CharField(
        _("hex color code"), help_text=_("e.g., #cc1111"), max_length=7, blank=True
    )
    model = models.ForeignKey(
        Model, on_delete=models.CASCADE, verbose_name=_("exterior finish")
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("exterior finishes")

    def __str__(self):
        return self.name


class Trim(BaseModel):
    id = ShortUUIDField(length=10, primary_key=True, editable=False)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    filtered_model_years = models.ManyToManyField(
        ModelYear,
        verbose_name=_("filtered model years"),
        help_text=_("years this trim level was not available"),
        blank=True,
    )
    includes = models.JSONField(
        _("json field describing and listing options included at this trim level"),
        help_text=_("see documentation for standard formatting"),
        blank=True,
        null=True,
    )
    child_trim = models.ForeignKey(
        "self",
        verbose_name=_("child trim level"),
        help_text=_(
            "this trim level includes and expands on child trim, except as noted"
        ),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["model__name", "name"]
        # constraints = (
        #     models.UniqueConstraint(fields=["model", "name"], name="unique_model_trim")
        # )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_string = f"{self.model.name} {self.name} {self.id}"
            self.slug = slugify(slug_string, allow_unicode=True)
        super().save(*args, **kwargs)
