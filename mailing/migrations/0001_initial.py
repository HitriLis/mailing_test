# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2022-11-21 11:01
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscribers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=254, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('delayed_date', models.DateTimeField(blank=True, null=True, verbose_name='\u041e\u0442\u043b\u043e\u0436\u0435\u043d\u043d\u0430\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0430')),
                ('error_send', models.BooleanField(default=False, verbose_name='\u041e\u0448\u0438\u0431\u043a\u0438 \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438')),
                ('send', models.BooleanField(default=False, verbose_name='\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0430')),
                ('subscribers', models.ManyToManyField(to='subscribers.Subscribers', verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u0447\u0438\u043a\u0438')),
            ],
            options={
                'verbose_name': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430',
                'verbose_name_plural': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='MailingsStatus',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('send', '\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e'), ('opened', '\u041e\u0442\u043a\u0440\u044b\u0442\u043e'), ('error', '\u041e\u0448\u0438\u0431\u043a\u0430')], default='send', max_length=15)),
                ('status_story', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='\u0418\u0441\u0442\u043e\u0440\u0438\u044f')),
                ('mailing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mailing_status', to='mailing.Mailings', verbose_name='\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430')),
                ('subscriber', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscribers.Subscribers', verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u0447\u0438\u043a')),
            ],
            options={
                'verbose_name': '\u0421\u0442\u0430\u0442\u0443\u0441\u044b \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438',
                'verbose_name_plural': '\u0421\u0442\u0430\u0442\u0443\u0441\u044b \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='TemplateMailing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template', models.TextField(verbose_name='\u0428\u0430\u0431\u043b\u043e\u043d')),
            ],
            options={
                'verbose_name': '\u0428\u0430\u0431\u043b\u043e\u043d\u044b \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438',
                'verbose_name_plural': '\u0428\u0430\u0431\u043b\u043e\u043d\u044b \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438',
            },
        ),
        migrations.AddField(
            model_name='mailings',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailing.TemplateMailing', verbose_name='\u0428\u0430\u0431\u043b\u043e\u043d \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438'),
        ),
    ]
