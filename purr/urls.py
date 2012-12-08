from django.conf.urls.defaults import *

from purr.views import Purr

urlpatterns = patterns('',
    
    url(
        r'^(?P<hierarchy>.+)/?',
        Purr.as_view(),
        name='purr_category_purr',
    ),
    
)