# Generated by Django 3.1.6 on 2021-02-18 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_card_board'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='owner',
            field=models.CharField(default='', max_length=128),
        ),
    ]
