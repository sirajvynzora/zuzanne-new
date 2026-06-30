# from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import include, path

# urlpatterns = [
#     path('', include('zuzanne_app.urls')),
# ]

# handler404 = 'zuzanne_app.views.custom_404_view'

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("", include("zuzanne_app.urls")),
]

handler404 = "zuzanne_app.views.custom_404_view"

# Always serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)