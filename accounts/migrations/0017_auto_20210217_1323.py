# Generated by Django 3.0.4 on 2021-02-17 10:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20210215_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7a1c4326-698c-42eb-8b22-1738f3652bd1'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='registermentee',
            name='id',
            field=models.UUIDField(default=uuid.UUID('00c5431b-279b-4b13-8a6d-c0ddd9a44580'), editable=False, primary_key=True, serialize=False),
        ),
    ]
