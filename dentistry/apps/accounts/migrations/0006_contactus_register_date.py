# Generated by Django 5.1.2 on 2024-11-11 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_contactus_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='register_date',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ'),
        ),
    ]