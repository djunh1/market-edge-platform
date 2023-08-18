# Generated by Django 4.2.4 on 2023-08-18 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('weekday_study', 'Analyze a stocks movements on a given week day'), ('gap_study', 'Analyzes continuation gaps of a stock'), ('move study', 'Analyzes non-gap stock price movements'), ('fundamentals_study', 'Company SEC 10q fundamentals'), ('ep_study', 'Episodic pivot')], default='weekday_study', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=6)),
                ('type', models.CharField(max_length=20)),
                ('study_move_value', models.IntegerField(blank=True, null=True)),
                ('study_move_volume', models.IntegerField(blank=True, null=True)),
                ('study_date', models.DurationField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('study_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.studytype')),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
    ]
