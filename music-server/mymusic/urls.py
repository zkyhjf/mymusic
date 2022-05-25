from django.urls import path, include, re_path
from django.views import static
from django.conf import settings
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('song/', include('song.urls')),
    path('user/', include('user.urls')),
    re_path('static/(?P<path>.*)', static.serve, {'document_root': settings.STATIC_ROOT})
]

handler404 = TemplateView.as_view(template_name='index.html')