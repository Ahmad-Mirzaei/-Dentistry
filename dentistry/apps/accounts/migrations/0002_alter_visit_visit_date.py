# Generated by Django 5.1.2 on 2024-11-09 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='visit_date',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ مراجعه'),
        ),
    ]
