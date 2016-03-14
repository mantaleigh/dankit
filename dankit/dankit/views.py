from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token
import image_processing as proc
from django.template.loader import get_template
from django.template import Context
from django import forms
import uuid
from django.shortcuts import render

class UrlForm(forms.Form): 
    img_url = forms.CharField(label='Image Url', max_length=100)
    file = forms.FileField(label='Upload Image')

@requires_csrf_token
def home(request):
    context_dict = {'form': None, 'result_img': ''}
    if request.POST.get('img_url'): 
        result = proc.get_search_terms(request.POST['img_url'])
        context_dict['result_img'] = result
    elif request.FILES.get('file'): 
    
        extension = request.FILES['file'].name.split('.')[-1]
        filename = uuid.uuid4().hex + '.' + extension 
        
        with open('/var/www/dankit/static/' + filename, 'w') as f:
            f.write(request.FILES['file'].read())

        result = proc.get_search_terms('http://dankit.me/static/' + filename)
        context_dict['result_img'] = result
    form = UrlForm()


    context_dict['form'] = form

    # template = get_template("home.html") 
    # context = Context(context_dict)
    # return HttpResponse(template.render(context, request))
    return render(request, 'home.html', context_dict)




