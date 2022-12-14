# Generated by Django 3.2.15 on 2022-10-03 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('is_primary', models.BooleanField(default=False, verbose_name='is primary owner')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('ownership', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='CarModels.brand')),
            ],
            options={
                'ordering': ['ownership__name', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='country name')),
                ('abbreviation', models.CharField(blank=True, max_length=10, unique=True, verbose_name='abbreviation')),
            ],
        ),
        migrations.CreateModel(
            name='ExteriorFinish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='finish name')),
                ('color_code', models.CharField(help_text='e.g., #cc1111', max_length=7, verbose_name='hex color code')),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('available_finishes', models.ManyToManyField(to='CarModels.ExteriorFinish')),
            ],
            options={
                'ordering': ['brand__name', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ModelYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.DecimalField(decimal_places=1, help_text="may include half-year as '.5', e.g., '1998.'", max_digits=5, verbose_name='model year')),
            ],
            options={
                'ordering': ['year'],
            },
        ),
        migrations.CreateModel(
            name='Trim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('includes', models.JSONField(help_text='see documentation for standard formatting', verbose_name='json field describing and listing options included at this trim level')),
                ('child_trim', models.ForeignKey(blank=True, help_text='this trim level includes and expands on child trim, except as noted', null=True, on_delete=django.db.models.deletion.SET_NULL, to='CarModels.trim', verbose_name='child trim level')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('filtered_exterior_finishes', models.ManyToManyField(help_text='finishes not available with this trim level', to='CarModels.ExteriorFinish', verbose_name='filtered finishes')),
                ('filtered_model_years', models.ManyToManyField(help_text='years this trim level was not available', to='CarModels.ModelYear', verbose_name='filtered model years')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CarModels.model')),
            ],
            options={
                'ordering': ['model__name', 'name'],
            },
        ),
        migrations.AddField(
            model_name='model',
            name='available_model_years',
            field=models.ManyToManyField(to='CarModels.ModelYear'),
        ),
        migrations.AddField(
            model_name='model',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='CarModels.brand'),
        ),
        migrations.AddField(
            model_name='model',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='brand',
            name='primary_country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='CarModels.country', verbose_name='primary country'),
        ),
    ]
