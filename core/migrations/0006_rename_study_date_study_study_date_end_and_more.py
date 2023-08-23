# Generated by Django 4.2.4 on 2023-08-23 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_delete_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='study',
            old_name='study_date',
            new_name='study_date_end',
        ),
        migrations.RemoveField(
            model_name='study',
            name='study_move_value',
        ),
        migrations.RemoveField(
            model_name='study',
            name='study_move_volume',
        ),
        migrations.AddField(
            model_name='study',
            name='study_date_start',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
