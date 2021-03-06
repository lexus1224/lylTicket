# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-03 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carriage',
            fields=[
                ('carriage_key', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('carriage_id', models.IntegerField(default=1)),
                ('num_seat', models.IntegerField(default=0)),
                ('seat_type', models.CharField(choices=[('shangwu', '\u5546\u52a1\u5ea7'), ('yideng', '\u4e00\u7b49\u5ea7'), ('erdeng', '\u4e8c\u7b49\u5ea7'), ('ruanwo', '\u8f6f\u5367'), ('yingwo', '\u786c\u5367'), ('yingzuo', '\u786c\u5ea7'), ('wuzuo', '\u65e0\u5ea7')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('run_key', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('order_of_station', models.IntegerField(default=1)),
                ('arrive_time', models.TimeField(max_length=10, verbose_name='\u5230\u7ad9\u65f6\u95f4')),
                ('distance_count', models.FloatField(verbose_name='\u91cc\u7a0b\u6570')),
                ('count_over_night', models.IntegerField(default=-1)),
            ],
            options={
                'ordering': ['train_come_by', 'order_of_station'],
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('seat_key', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('seat_id', models.IntegerField()),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=100)),
                ('carriage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainManage.Carriage')),
            ],
            options={
                'ordering': ['seat_key', 'date'],
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('station_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('station_name', models.CharField(max_length=20, verbose_name='\u9014\u7ecf\u8f66\u7ad9')),
                ('station_city', models.CharField(max_length=20, verbose_name='\u6240\u5c5e\u57ce\u5e02')),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('train_id', models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name='\u5217\u8f66\u7f16\u53f7')),
                ('train_type', models.CharField(default='K', max_length=1, verbose_name='\u5217\u8f66\u7c7b\u578b')),
                ('num_station', models.IntegerField(default=0, verbose_name='\u603b\u7ad9\u70b9\u6570')),
                ('distance', models.FloatField(default=0, verbose_name='\u603b\u91cc\u7a0b\u6570')),
            ],
        ),
        migrations.AddField(
            model_name='run',
            name='station_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainManage.Station'),
        ),
        migrations.AddField(
            model_name='run',
            name='train_come_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainManage.Train'),
        ),
        migrations.AddField(
            model_name='carriage',
            name='train_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainManage.Train'),
        ),
    ]
