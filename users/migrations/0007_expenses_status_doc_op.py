# Generated by Django 4.1.4 on 2023-03-08 04:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Doc_op',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opnum', models.IntegerField()),
                ('doc_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
