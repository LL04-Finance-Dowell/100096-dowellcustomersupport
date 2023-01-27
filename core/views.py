from django.shortcuts import render, redirect, HttpResponse

from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)

from .models import Portfolio, Room, Message

#import django csrf 
from django.views.decorators.csrf import csrf_exempt
def index(request):
    return render(request, 'index.html')


class HomeView(ListView):
    model = Portfolio
    template_name = 'homepage.html'
    context_object_name = 'portfolios'

#django post request
@csrf_exempt
def post(request):
    if request.method == 'POST':
        print(request.POST)
        return redirect('index')
    else:
        print('is a get request')
        return render(request, 'index.html')


def portfolio(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)
    try:
        room = Room.objects.filter(authority_portfolio=portfolio).first()
        messages = Message.objects.filter(room=room)
    except Room.DoesNotExist:
        Room.objects.create(
            room_name=portfolio.portfolio_name,
            authority_portfolio=portfolio,
            organization=portfolio.organization
        )

    return render(request, 'room.html', {'portfolio': portfolio, 'messages': messages, 'room_pk': room.pk})

# GET and POST method for sending and receiving messages in room
def send_message(request, pk):
    message = request.POST.get('message')
    room = Room.objects.get(pk=pk)
    Message.objects.create(
        room=room,
        message=message,
        author=room.authority_portfolio
    )
    messages = Message.objects.filter(author=room.authority_portfolio)
    return render(request, 'room.html', {'portfolio': portfolio, 'messages': messages, 'room_pk': room.pk})



def getMessages(request,  pk):
    room =Room.objects.get(pk=pk)
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room)
    return render(request, 'room.html', {'portfolio': portfolio, 'messages': messages, 'room_pk': room.pk})
    




