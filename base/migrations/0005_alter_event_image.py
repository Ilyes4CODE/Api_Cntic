# Generated by Django 5.0 on 2024-03-15 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_event_description_event_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to='event_images/'),
        ),
    ]
