from django.views.generic.base import TemplateView 

class IndexTemplateView(TemplateView):
    template_name = "Templates/index.html"
def collect(self,request):
   if request.method == 'POST':
        print(request.POST.get('url')) 
