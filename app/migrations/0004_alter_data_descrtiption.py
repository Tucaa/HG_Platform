# Generated by Django 4.1.2 on 2022-11-14 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_data_created_alter_room_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='descrtiption',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
