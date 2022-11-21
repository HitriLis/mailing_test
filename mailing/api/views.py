# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from .serializers import TemplateMailingSerializer, MailingsStatusSerializer, MailingsSerializer, MailingsListSerializer, MailingsCreateSerializer, \
    MailingsListStatusSerializer
from rest_framework import viewsets, mixins, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from mailing.custom_renderers import JPEGRenderer
from mailing.models import TemplateMailing, Mailings, MailingsStatus
from mailing.tasks import send_email


class TemplateMailingViewSet(viewsets.ModelViewSet):
    queryset = TemplateMailing.objects.all()
    serializer_class = TemplateMailingSerializer
    http_method_names = ['get', 'post', 'delete', 'put']


class MailingsViewSet(viewsets.ModelViewSet):
    queryset = Mailings.objects.prefetch_related('mailing_status', 'subscribers').select_related(
        'template'
    ).all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MailingsListSerializer
        if self.action == 'create':
            return MailingsCreateSerializer
        if self.action == 'retrieve':
            return MailingsSerializer
        if self.action == 'status':
            return MailingsListStatusSerializer

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        mailings = Mailings.objects.filter(id=pk).prefetch_related('mailing_status', 'subscribers'). \
            select_related('template').all()
        if not mailings.exists():
            raise Http404
        serializer = MailingsListStatusSerializer(mailings.first())
        return Response(serializer.data, status=200)

    @action(detail=True, methods=['put'])
    def send(self, request, pk=None):
        mailings = Mailings.objects.filter(id=pk)
        if not mailings.exists():
            raise Http404

        mailing = mailings.first()

        if mailing.send:
            return Response(data={'detail': 'Рассылка отправлена'}, status=status.HTTP_400_BAD_REQUEST)

        host_name = '{scheme}://{host}'.format(scheme=request.scheme, host=request.get_host())
        if mailing.delayed_date:
            send_email.apply_async(
                kwargs={
                    'mailing_id': pk,
                    'host': host_name
                }, eta=mailing.delayed_date)
        else:
            send_email.delay(pk, host_name)

        mailing.send = True
        mailing.save(update_fields=['send'])
        return Response(data={'send': 'success'}, status=status.HTTP_200_OK)

    http_method_names = ['get', 'post', 'delete', 'put']


class MailingsStatusViewSet(viewsets.ModelViewSet):
    queryset = MailingsStatus.objects.select_related(
        'mailing',
        'subscriber'
    ).all()
    serializer_class = MailingsStatusSerializer
    http_method_names = ['get']


class TrackMailingsStatusView(views.APIView):
    renderer_classes = [JPEGRenderer]

    @property
    def pixel(self):
        return open('static/pixel.jpg', 'rb')

    def get(self, request, *args, **kwargs):
        unique_id = self.kwargs['pk']
        messages = MailingsStatus.objects.filter(pk=unique_id)
        if messages.exists():
            message = messages.first()
            message.status = 'opened'
            message.save(update_fields=['status', 'status_story'])
            return Response(self.pixel.read(), status=201)
        return Response(status=404)
