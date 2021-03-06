# Generated by Django 4.0.2 on 2022-04-25 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp', '0002_clubrepresentative_password_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('card_number', models.CharField(max_length=16)),
                ('expiry_date', models.DateField()),
                ('discount_rate', models.FloatField()),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectApp.studentclub')),
            ],
        ),
    ]
