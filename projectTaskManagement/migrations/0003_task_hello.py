# Generated by Django 4.2.4 on 2023-09-06 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectTaskManagement', '0002_project_assignedto'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='hello',
            field=models.CharField(max_length=33, null=True),
        ),
    ]
