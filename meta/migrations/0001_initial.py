# Generated by Django 5.0.6 on 2024-05-21 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsrCredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usrname', models.CharField(max_length=100)),
                ('llAT', models.CharField(max_length=500)),
                ('pgAT', models.CharField(max_length=500)),
                ('igUserId', models.IntegerField()),
                ('fbPageId', models.IntegerField()),
                ('appID', models.IntegerField()),
                ('appSecret', models.CharField(max_length=200)),
            ],
        ),
    ]
