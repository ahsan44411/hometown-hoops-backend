# Generated by Django 4.1.7 on 2023-03-13 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_leagueschedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leagueschedule',
            name='leagues_register',
        ),
        migrations.AddField(
            model_name='leagueschedule',
            name='league',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.leagues'),
            preserve_default=False,
        ),
    ]
