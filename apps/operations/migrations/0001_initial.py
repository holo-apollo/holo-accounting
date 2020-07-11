# Generated by Django 3.0.8 on 2020-07-11 13:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        ('counterparties', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, help_text='UAH', max_digits=9)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('bank_id', models.CharField(blank=True, default='', max_length=24, null=True, unique=True)),
                ('is_reviewed', models.BooleanField(default=False)),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='operations', to='counterparties.Counterparty')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operations', to='orders.Order')),
            ],
        ),
    ]
