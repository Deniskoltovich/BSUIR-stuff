# Generated by Django 4.2.6 on 2023-10-20 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('document_series', models.CharField(max_length=2)),
                ('document_number', models.CharField(max_length=16)),
                ('bank_info', models.CharField(max_length=64)),
            ],
        ),
    ]
