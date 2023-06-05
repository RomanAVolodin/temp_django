from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('v1/', include('movies.api.v1.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]