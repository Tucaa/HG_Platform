# Generated by Django 4.1.2 on 2022-11-15 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_data_contributors'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='room_files',
            field=models.ManyToManyField(related_name='room_files', to='app.room'),
        ),
    ]
