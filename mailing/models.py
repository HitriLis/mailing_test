# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.db import models
from subscribers.models import Subscribers



class TemplateMailing(models.Model):
    template = models.TextField('Шаблон')

    class Meta:
        verbose_name = 'Шаблоны рассылки'
        verbose_name_plural = 'Шаблоны рассылки'


class Mailings(models.Model):
    title =  models.CharField(max_length=254, null=True, blank=True, verbose_name='Название')
    subscribers = models.ManyToManyField(Subscribers, verbose_name='Подписчики')
    date_create = models.DateTimeField(auto_now_add=True)
    delayed_date = models.DateTimeField(null=True, blank=True, verbose_name='Отложенная отправка')
    error_send = models.BooleanField(default=False, verbose_name='Ошибки отправки')
    send = models.BooleanField(default=False, verbose_name='Рассылка отправлена')
    template = models.ForeignKey(
        TemplateMailing,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Шаблон рассылки'
    )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingsStatus(models.Model):
    SEND = 'send'
    OPENED = 'opened'
    ERROR = 'error'

    SEND_STATUS = (
        (SEND, 'Отправлено'),
        (OPENED, 'Открыто'),
        (ERROR, 'Ошибка'),
    )
    id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=15,
        choices=SEND_STATUS,
        default=SEND,
    )
    status_story = JSONField(null=True, blank=True, verbose_name='История')
    subscriber = models.ForeignKey(
        Subscribers,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Подписчик'
    )
    mailing = models.ForeignKey(
        Mailings,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='mailing_status',
        verbose_name='Рассылка'
    )

    def save(self, *args, **kwargs):
        status_date = self.status_story or {}
        data = timezone.now()
        status_date[self.status] = data.strftime('%Y-%m-%d %H:%M')
        self.status_story = status_date
        super(MailingsStatus, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статусы отправки'
        verbose_name_plural = 'Статусы отправки'
