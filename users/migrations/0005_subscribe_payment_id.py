# Generated by Django 4.2.17 on 2025-03-09 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_subscribe'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribe',
            name='payment_id',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='ID платежа'),
        ),
    ]
