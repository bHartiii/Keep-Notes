# Generated by Django 3.0.5 on 2021-01-02 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0008_auto_20210102_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='label',
            field=models.ManyToManyField(default=1, to='Notes.Labels'),
        ),
    ]
