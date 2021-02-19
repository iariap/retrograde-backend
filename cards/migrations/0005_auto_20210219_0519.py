# Generated by Django 3.1.6 on 2021-02-19 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0001_initial'),
        ('cards', '0004_card_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='votes',
        ),
        migrations.AddField(
            model_name='card',
            name='votes',
            field=models.ManyToManyField(to='votes.Vote'),
        ),
    ]