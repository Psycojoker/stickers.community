from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from tastypie.api import Api

from .api import ImageResource, ThumbnailResource, PinResource, UserResource
from .feeds import LatestPins, LatestUserPins, LatestTagPins
from .views import CreateImage
from .models import LICENCES


class PinTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PinTemplateView, self).get_context_data(**kwargs)
        context['licences'] = LICENCES
        return context


v1_api = Api(api_name='v1')
v1_api.register(ImageResource())
v1_api.register(ThumbnailResource())
v1_api.register(PinResource())
v1_api.register(UserResource())


urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls, namespace='api')),

    url(r'feeds/latest-pins/tag/(?P<tag>(\w|-)+)/', LatestTagPins()),
    url(r'feeds/latest-pins/user/(?P<user>(\w|-)+)/', LatestUserPins()),
    url(r'feeds/latest-pins/', LatestPins()),

    url(r'^pins/pin-form/$', PinTemplateView.as_view(template_name='core/pin_form.html'),
        name='pin-form'),
    url(r'^pins/create-image/$', CreateImage.as_view(), name='create-image'),

    url(r'^pins/tag/(?P<tag>(\w|-)+)/$', PinTemplateView.as_view(template_name='core/pins.html'),
        name='tag-pins'),
    url(r'^pins/user/(?P<user>(\w|-)+)/$', PinTemplateView.as_view(template_name='core/pins.html'),
        name='user-pins'),
    url(r'^(?P<pin>[0-9]+)/$', PinTemplateView.as_view(template_name='core/pins.html'),
        name='recent-pins'),
    url(r'^$', PinTemplateView.as_view(template_name='core/pins.html'),
        name='recent-pins'),
)
