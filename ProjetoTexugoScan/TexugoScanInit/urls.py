from django.urls import path
from TexugoScanInit.views import IndexTemplateView
app_name ='TexugoScanInit'
urlpatterns = [
 path('', IndexTemplateView.as_view(), name='index'),
]