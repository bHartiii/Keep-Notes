# Generated by Django 3.0.5 on 2020-12-29 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0002_auto_20201230_0227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('content', models.TextField(db_index=True)),
                ('date', models.DateTimeField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.User')),
            ],
        ),
    ]
