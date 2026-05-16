from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'inicio/index.html')

def acercade(request):
    return render(request, 'inicio/acercade.html')
