# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .serializers import SubscribersSerializer
from rest_framework import viewsets, mixins
from subscribers.models import Subscribers

class SubscribersViewSet(viewsets.ModelViewSet):
    queryset = Subscribers.objects.all()
    serializer_class = SubscribersSerializer
    http_method_names = ['get', 'post', 'delete', 'put']



