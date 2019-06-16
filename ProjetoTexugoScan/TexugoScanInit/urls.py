from django.urls import path  import IndexTemplateView

app_name ='TexugoScanInit'
urlpatterns = [
 path('', IndexTemplateView.as_view(), name='index'),

]