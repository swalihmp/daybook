# Generated by Django 4.1.4 on 2023-03-14 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_expenses_exp_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayClose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('t_expense', models.BigIntegerField()),
                ('t_income', models.BigIntegerField()),
                ('ClosingAmount', models.BigIntegerField()),
                ('CashInhand', models.BigIntegerField()),
                ('diffrence', models.BigIntegerField()),
            ],
        ),
    ]
