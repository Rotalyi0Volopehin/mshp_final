# Generated by Django 3.0.1 on 2020-05-02 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200415_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='total_exp',
            field=models.IntegerField(default=0),
        ),
    ]
