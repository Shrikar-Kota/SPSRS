# Generated by Django 3.1.2 on 2020-11-13 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spsrs', '0004_auto_20201113_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='First',
            field=models.IntegerField(blank=True, choices=[(1, 'Poor'), (2, 'Satisfactory'), (3, 'Good'), (4, 'Very Good'), (5, 'Awesome')], null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='fifth',
            field=models.IntegerField(blank=True, choices=[(1, 'Poor'), (2, 'Satisfactory'), (3, 'Good'), (4, 'Very Good'), (5, 'Awesome')], null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='fourth',
            field=models.IntegerField(blank=True, choices=[(1, 'Poor'), (2, 'Satisfactory'), (3, 'Good'), (4, 'Very Good'), (5, 'Awesome')], null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='second',
            field=models.IntegerField(blank=True, choices=[(1, 'Poor'), (2, 'Satisfactory'), (3, 'Good'), (4, 'Very Good'), (5, 'Awesome')], null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='third',
            field=models.IntegerField(blank=True, choices=[(1, 'Poor'), (2, 'Satisfactory'), (3, 'Good'), (4, 'Very Good'), (5, 'Awesome')], null=True),
        ),
    ]
