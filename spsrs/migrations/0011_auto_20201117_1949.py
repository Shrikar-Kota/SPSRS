# Generated by Django 3.1.1 on 2020-11-17 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spsrs', '0010_auto_20201117_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateField(max_length=8),
        ),
    ]