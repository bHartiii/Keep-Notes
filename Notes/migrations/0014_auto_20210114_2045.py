# Generated by Django 3.0.5 on 2021-01-14 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20210107_2349'),
        ('Notes', '0013_auto_20210114_2022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='collaborator',
        ),
        migrations.AddField(
            model_name='notes',
            name='collaborator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='authentication.User'),
        ),
    ]
