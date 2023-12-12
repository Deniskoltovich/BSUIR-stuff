# Generated by Django 4.2.6 on 2023-11-17 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('quantity', models.IntegerField(default=1)),
                ('city', models.CharField(max_length=32)),
                ('region', models.CharField(default='', max_length=32)),
                ('country', models.CharField(max_length=32)),
                ('date', models.DateField(auto_now_add=True)),
                ('full_price', models.DecimalField(blank=True, decimal_places=2, max_digits=11)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.customer')),
            ],
        ),
        migrations.AddConstraint(
            model_name='bill',
            constraint=models.CheckConstraint(check=models.Q(('price__gte', 0)), name='check_current_price_is_positive'),
        ),
    ]