# Generated by Django 3.2.6 on 2021-09-16 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_review_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='ecommerce.png', null=True, upload_to=''),
        ),
    ]
