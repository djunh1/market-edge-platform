# Generated by Django 4.2.4 on 2023-08-20 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_study_study_move_value_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='study',
            name='study_type',
        ),
    ]