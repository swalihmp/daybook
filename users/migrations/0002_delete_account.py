# Generated by Django 4.1.4 on 2023-03-04 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]