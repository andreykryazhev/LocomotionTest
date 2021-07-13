# Generated by Django 2.0.1 on 2018-03-25 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Mileage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serie_name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('value', models.IntegerField()),
                ('filial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loco_app.Filials')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('stake', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='mileage',
            name='serie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loco_app.Series'),
        ),
    ]
