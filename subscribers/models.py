# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Subscribers(models.Model):
    email = models.EmailField(max_length=254, null=True, blank=True, db_index=True, verbose_name='Почта')
    name = models.CharField(max_length=254, null=True, blank=True, verbose_name='Имя')
    surname = models.CharField(max_length=254, null=True, blank=True, verbose_name='Фамилия')
    birthday = models.DateField(null=True, blank=True, verbose_name='День рождения')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'