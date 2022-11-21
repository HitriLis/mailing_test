from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from mailing.api.views import TemplateMailingViewSet, MailingsStatusViewSet, MailingsViewSet, TrackMailingsStatusView

router = DefaultRouter()
router.register('template', TemplateMailingViewSet)
router.register('status', MailingsStatusViewSet)
router.register('mailing', MailingsViewSet)

urlpatterns = [
    url(r'^message/track\/(?P<pk>.+)/OPENED/$', TrackMailingsStatusView.as_view(), name='example')
] + router.urls
