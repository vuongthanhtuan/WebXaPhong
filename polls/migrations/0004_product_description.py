# Generated by Django 3.2.7 on 2021-12-07 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20211207_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
