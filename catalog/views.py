from django.http import HttpResponse, HttpResponseNotFound

def my_view(request):
    return HttpResponse('<h1>Django Project</h1>')