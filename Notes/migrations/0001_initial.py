# Generated by Django 3.0.5 on 2021-01-01 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0002_auto_20201231_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Labels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(db_index=True, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.User')),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_created=True)),
                ('title', models.TextField()),
                ('content', models.TextField(db_index=True)),
                ('isArchive', models.BooleanField(default=False)),
                ('isDelete', models.BooleanField(default=False)),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Notes.Labels')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.User')),
            ],
        ),
    ]
