# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from smtplib import SMTPException
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from crm.celery_tasks import app
from celery.utils.log import get_task_logger
from .models import Mailings, MailingsStatus


logger = get_task_logger(__name__)

@app.task(name='send_email')
def send_email(mailing_id, host):
    mailings = Mailings.objects.filter(id=mailing_id).prefetch_related('subscribers').select_related(
        'template'
    ).all()
    if mailings.exists():
        mailing = mailings.first()
        subscribers = mailing.subscribers.all()
        for subscriber in subscribers:
            mailings_status = MailingsStatus.objects.create(
                subscriber=subscriber,
                mailing=mailing
            )
            try:
               str_template = mailing.template.template.format(name=subscriber.name, email=subscriber.email,
                                                               surname=subscriber.surname, birthday=subscriber.birthday)
               msg = render_to_string('email.html', {
                   'content': str_template,
                   'key': mailings_status.id,
                   'host': host})
               send_mail(mailing.title, msg, settings.EMAIL_HOST_USER, [subscriber.email], html_message=msg)
               mailings_status.status = 'send'
               mailings_status.save(update_fields=['status', 'status_story'])
            except SMTPException as e:
                    mailing.error_send = True
                    mailings_status.status = 'error'
                    mailings_status.save(update_fields=['status', 'status_story'])
            finally:
                mailing.save(update_fields=['error_send'])