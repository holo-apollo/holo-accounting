# Generated by Django 3.0.8 on 2020-07-11 13:06

import django.contrib.postgres.fields.citext
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.citext.CICharField(max_length=254, unique=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('is_archived', models.BooleanField(default=False)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.Unit')),
            ],
        ),
    ]
