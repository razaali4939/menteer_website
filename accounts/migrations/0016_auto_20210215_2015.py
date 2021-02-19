# Generated by Django 3.0.4 on 2021-02-15 17:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210215_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='id',
            field=models.UUIDField(default=uuid.UUID('888dbaa6-396b-4d13-aa52-cb195d03aa4d'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='registermentee',
            name='id',
            field=models.UUIDField(default=uuid.UUID('1ac194e3-9ebd-433c-8e40-3bebbb19cd77'), editable=False, primary_key=True, serialize=False),
        ),
    ]
