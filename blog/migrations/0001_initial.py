# Generated by Django 4.1.7 on 2023-03-27 13:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=10)),
                ('pub_date', models.DateField()),
                ('mod_date', models.DateField(default=datetime.date.today)),
                ('tag', models.CharField(max_length=50)),
                ('content', models.TextField()),
            ],
        ),
    ]
