# Generated by Django 3.1.1 on 2020-11-17 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spsrs', '0009_auto_20201114_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateField(max_length=10),
        ),
    ]
