# Generated by Django 3.1.6 on 2021-02-11 14:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210209_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='id',
            field=models.UUIDField(default=uuid.UUID('600e25a2-951d-4b4e-8bb7-3d1929bdb8b8'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='registermentee',
            name='id',
            field=models.UUIDField(default=uuid.UUID('3b9d5ee2-44dc-44b7-b92e-2aadd0d919dc'), editable=False, primary_key=True, serialize=False),
        ),
    ]
