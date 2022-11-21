# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Subscribers

@admin.register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'surname', 'birthday')
