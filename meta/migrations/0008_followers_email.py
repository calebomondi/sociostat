# Generated by Django 5.0.6 on 2024-06-15 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0007_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='followers',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
    ]
