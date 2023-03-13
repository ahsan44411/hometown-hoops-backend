# Generated by Django 4.1.7 on 2023-03-12 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_leaguesregister_options_leagueteamstats'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeagueSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.TextField(blank=True, null=True)),
                ('leagues_register', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.leaguesregister')),
            ],
        ),
    ]
