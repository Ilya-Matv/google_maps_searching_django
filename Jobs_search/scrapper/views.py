
from django.shortcuts import render, redirect
from .thread import CreateBusinessesThread
from django.contrib import messages
from .models import BusinessList
from django.core.paginator import Paginator
from .forms import ScrapForm
import time
from django.http import HttpResponse
from django.http import JsonResponse
from .thread import prog





def progress_bar(request, indicator):
    
    time.sleep(1)
        
    return render(request, 'scr/progress_bar.html',{'indicator':indicator})




def scrap(request):
    global prog
    form = ScrapForm()
    if request.method == "POST":
        form = ScrapForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['City']
            profession = form.cleaned_data['Profession']
            number = form.cleaned_data['Quantity']
            thread = CreateBusinessesThread(request, city, profession, number)
            thread.start()
            prog.set_value(0)
            indicator = 0
            if number == 'all':
                indicator = 1
            
            return redirect('progress_bar', indicator)
        else:
            messages.success(request,("Woops! there was a problem, try again"))
            return redirect('scrap')

    return render(request, 'scr/scrap_home.html',{'form':form})
        

def data_list(request):
    if request.method == "POST":
        id = request.POST['num_id']
        return redirect('business_card', id = id)

    p = Paginator(BusinessList.objects.filter(user=request.user).order_by('date'), 5)
    page = request.GET.get('page')
    data_list = p.get_page(page)
    return render(request, 'scr/navigation_data.html', {'data_list' : data_list})

def business_card(request, id):
    
    p = Paginator(BusinessList(user = request.user, id = id).businesses.all(), 9)
    page = request.GET.get('page')
    data_cards = p.get_page(page)
    return render(request, 'scr/business_cards.html', {'data_cards' : data_cards})
