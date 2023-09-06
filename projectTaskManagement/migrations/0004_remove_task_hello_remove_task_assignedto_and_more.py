# Generated by Django 4.2.4 on 2023-09-06 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projectTaskManagement', '0003_task_hello'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='hello',
        ),
        migrations.RemoveField(
            model_name='task',
            name='assignedTo',
        ),
        migrations.AddField(
            model_name='task',
            name='assignedTo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
