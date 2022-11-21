# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import TemplateMailing, Mailings, MailingsStatus



@admin.register(TemplateMailing)
class TemplateMailingAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Mailings)
class MailingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_create', 'delayed_date')


@admin.register(MailingsStatus)
class MailingsStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_create', 'date_update')
