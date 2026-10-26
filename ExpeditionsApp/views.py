from django.shortcuts import render
from ExpeditionsApp.models import Expedition
# Create your views here.
from django.http import HttpResponse, request

def listExpeditions(request):
    list=Expedition.objects.all()
    return render(request, 'ExpeditionApp/list.html', {'list': list})
def home(request):
    return HttpResponse("Hello, world. You're at the ExpeditionsApp home.")
def afficher(request,name):
    # return HttpResponse(f"Hello, {name}!")
    return render(request, 'ExpeditionApp/afficher.html', {'name': name})
def detailExpedition(request,pk):
    expedition=Expedition.objects.get(pk=pk)
    return render(request, 'ExpeditionApp/detail.html', {'expedition': expedition})