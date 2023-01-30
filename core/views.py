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
    room = Room.objects.filter(authority_portfolio=portfolio).first()
    if room is None:
        room = Room.objects.create(
            room_name=portfolio.portfolio_name,
            authority_portfolio=portfolio,
            organization=portfolio.organization
        )
        return render(request, 'room.html')
    else:
        messages = Message.objects.filter(room=room)
        return render(request, 'room.html', {'portfolio': portfolio, 'messages': messages, 'room_pk': room.pk, 'author':room.authority_portfolio})

# GET and POST method for sending and receiving messages in room
#admin
def send_message(request, pk):
    portfolio = Portfolio.objects.filter(is_staff=True).first()
    
    room = Room.objects.get(pk=pk)
    messages = Message.objects.filter(room=room)

    if request.method == 'POST':
        message = request.POST.get('message')
        Message.objects.create(
            room=room,
            message=message,
            author=portfolio,
        )
    return render(
        request, 'room.html', 
        {'portfolio': portfolio, 'messages': messages, 'room_pk': room.pk, 'author':room.authority_portfolio},
        )

def my_room(request, portfolio_name):
    
    try:
        portfolio = Portfolio.objects.get(portfolio_name=portfolio_name)
        room = Room.objects.filter(authority_portfolio=portfolio).first()
        messages = Message.objects.filter(room=room)
        # messages = Message.objects.filter(author=portfolio)
    except Portfolio.DoesNotExist:
        return HttpResponse('Portfolio does not exist')

    if request.method == 'POST':
        message = request.POST.get('message')
        Message.objects.create(
            room=room,
            message=message,
            author=portfolio,
        )
    return render(request, 'my_room.html', {'portfolio': portfolio, 'messages': messages, 'room_pk': room.pk, 'author':room.authority_portfolio})
    