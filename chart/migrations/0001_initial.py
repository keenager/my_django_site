# Generated by Django 4.1.7 on 2023-05-30 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HayulGrowth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_month', models.DateField()),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
            ],
        ),
    ]