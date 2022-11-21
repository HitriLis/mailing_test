# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import transaction
from rest_framework.serializers import ModelSerializer, SerializerMethodField, IntegerField, ListField, ValidationError
from mailing.models import TemplateMailing, Mailings, MailingsStatus
from subscribers.api.serializers import SubscribersSerializer


class TemplateMailingSerializer(ModelSerializer):
    class Meta:
        model = TemplateMailing
        fields = '__all__'


class MailingsStatusSerializer(ModelSerializer):
    subscriber = SubscribersSerializer()
class Meta:
        model = MailingsStatus
        fields = ('id', 'status', 'date_create', 'date_update', 'subscriber', 'mailing_id', 'status_story')

class MailingsListStatusSerializer(ModelSerializer):
    mailing_status = MailingsStatusSerializer(many=True, read_only=True)
    class Meta:
        model = Mailings
        fields = ('id', 'title', 'date_create', 'delayed_date', 'template_id', 'mailing_status')


class MailingsSerializer(ModelSerializer):
    subscribers = SubscribersSerializer(many=True, read_only=True)
    template = TemplateMailingSerializer(read_only=True)

    class Meta:
        model = Mailings
        fields = ('id', 'title', 'date_create', 'delayed_date', 'template', 'subscribers')


class MailingsListSerializer(ModelSerializer):
    subscribers_count = IntegerField(source='subscribers.count', read_only=True)

    class Meta:
        model = Mailings
        fields = ('id', 'title', 'date_create', 'delayed_date', 'template_id', 'subscribers_count')


class MailingsCreateSerializer(ModelSerializer):
    template = IntegerField(source='template.id')

    class Meta:
        model = Mailings
        fields = ('id', 'title', 'delayed_date', 'template', 'subscribers')

    def validate_template(self, value):
        try:
            self.context['template'] = TemplateMailing.objects.get(id=value)
        except TemplateMailing.DoesNotExist:
            raise ValidationError({"template": "Not found"})
        return value

    def validate_delayed_date(self, value):
        if value and  value <= timezone.now():
            raise ValidationError({"delayed_date": "Некорректная дата отсрочки"})
        return value

    def create(self, validated_data):
        with transaction.atomic():
            instance = Mailings.objects.create(
                title=validated_data['title'],
                delayed_date=validated_data['delayed_date'],
                template=self.context['template']
            )
            subscribers = validated_data['subscribers']
            instance.subscribers.add(*subscribers)
            return instance
