# Generated by Django 4.2.4 on 2023-08-20 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0004_remove_study_study_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeekdayStudy',
            fields=[
                ('study_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.study')),
                ('study_type', models.ForeignKey(default='WEEKDAY_STUDY', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.studytype')),
            ],
            bases=('core.study',),
        ),
    ]