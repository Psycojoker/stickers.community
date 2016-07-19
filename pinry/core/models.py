import requests
from cStringIO import StringIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from django_images.models import Image as BaseImage, Thumbnail
from taggit.managers import TaggableManager

from ..users.models import User


class ImageManager(models.Manager):
    # FIXME: Move this into an asynchronous task
    def create_for_url(self, url):
        file_name = url.split("/")[-1].split('#')[0].split('?')[0]
        buf = StringIO()
        response = requests.get(url)
        buf.write(response.content)
        obj = InMemoryUploadedFile(buf, 'image', file_name,
                                   None, buf.tell(), None)
        # create the image and its thumbnails in one transaction, removing
        # a chance of getting Database into a inconsistent state when we
        # try to create thumbnails one by one later
        image = self.create(image=obj)
        for size in settings.IMAGE_SIZES.keys():
            Thumbnail.objects.get_or_create_at_size(image.pk, size)
        return image


class Image(BaseImage):
    objects = ImageManager()

    class Meta:
        proxy = True

LICENCES = (
    ('cc-by', 'CC-BY'),
    ('cc-by-sa', 'CC-BY-SA'),
    ('cc-by-nc', 'CC-BY-NC'),
    ('cc-by-nc-sa', 'CC-BY-NC-SA'),
    ('cc-by-nd', 'CC-BY-ND'),
    ('cc-by-nc-nd', 'CC-BY-NC-ND'),
    ('cc0', 'Public Domain (CC0)'),
    ('free-art', 'Free Art Licence'),
    ('wtfpl', 'WTFpl'),
    ('other', 'Other (put it in the description)'),
)

class Pin(models.Model):
    submitter = models.ForeignKey(User)
    url = models.URLField(null=True)
    origin = models.URLField(null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ForeignKey(Image, related_name='pin')
    published = models.DateTimeField(auto_now_add=True)
    licence = models.CharField(null=True, choices=LICENCES, max_length=255)
    tags = TaggableManager()

    def __unicode__(self):
        return self.url if self.url else unicode(self.id)
