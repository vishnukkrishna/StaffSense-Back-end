# Generated by Django 4.2.4 on 2023-09-06 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectTaskManagement', '0002_project_assignedto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
