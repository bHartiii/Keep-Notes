# Generated by Django 3.0.8 on 2021-01-19 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0017_auto_20210115_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='trashedAt',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]