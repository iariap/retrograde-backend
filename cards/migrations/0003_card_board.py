# Generated by Django 3.1.6 on 2021-02-17 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20210217_0454'),
        ('cards', '0002_card_column'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='board',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='boards.board'),
        ),
    ]
