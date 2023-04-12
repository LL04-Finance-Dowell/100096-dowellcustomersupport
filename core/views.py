from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Portfolio, Room, Message
from django.contrib.auth import REDIRECT_FIELD_NAME
from functools import wraps
import json
import requests

from django.views.decorators.clickjacking import xframe_options_exempt







# You can write your views below here



ADMIN_PRODUCT = ["Login", "Extension", "Living-Lab-Admin", "Sales-Agent"]

PRODUCT_LIST = ["Workflow-AI", "Wifi-QR-Code", "User-Experience-Live", "Social-Media-Automation", "Living-Lab-Scales", "Logo-Scan", "Team-Management", "Living-Lab-Monitoring", "Permutation-Calculator", "Secure-Repositories", "Secure-Data", "Customer-Experience", "DoWell-CSC", "Living-Lab-Chat"]


def product_list(request):
    return JsonResponse({"product_list": [*ADMIN_PRODUCT, *PRODUCT_LIST]})


def product_list_object():
    return [*ADMIN_PRODUCT, *PRODUCT_LIST]

def product_list1():
    return ADMIN_PRODUCT





def user_passes_test(test_func, login_url='https://100014.pythonanywhere.com/?code=100096', redirect_field_name=REDIRECT_FIELD_NAME):
    def decorator(view_func):
        @wraps(view_func)
        def rt_wrapper(request, *args, **kwargs):
            session_id = request.GET.get("session_id", None)
            if session_id:
                url = 'https://100093.pythonanywhere.com/api/userinfo/'
                response = requests.post(url, data={'session_id': session_id})
                try:
                    response=response.json()
                except:
                    return JsonResponse({'error': 'Wrong session_id'})
                #   print("response : ", response)
                if test_func(response["userinfo"]["username"]):
                    request.session["session_id"] = session_id
                    request.session["dowell_user"] = response
                    return view_func(request, *args, **kwargs)
            else:
                if request.session["session_id"]:
                    return view_func(request, *args, **kwargs)
        return rt_wrapper
    return decorator



def dowell_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='https://100014.pythonanywhere.com/?code=100096'):
    actual_decorator = user_passes_test(
        lambda is_True: is_True,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



@dowell_login_required
def test(request):
    print("Logged in as: ", request.session["user_name"])
    return JsonResponse({"status":"it is working"})



def jsonify_message_object(mess_obj):
    return (
        {
            'id': mess_obj.id,
            'timestamp' : mess_obj.timestamp.isoformat(timespec='minutes') ,
            'room_id' : mess_obj.room_id,
            'read': mess_obj.read,
            'message': mess_obj.message,
            'side': mess_obj.side,
            'author' : {
                'id': mess_obj.author.id,
                'session_id':mess_obj.author.session_id
            }
        }
    )





#   Extension sender side handling
@xframe_options_exempt
@dowell_login_required
def extension_chat_box_view(request, *args, **kwargs):
    if kwargs['product'] == 'Extension':
        print("Product get args: ", request.GET.get('prdct'), request.session["dowell_user"])
        try:
            portfolio = Portfolio.objects.filter(userID=request.session["dowell_user"]["userinfo"]["userID"]).first()
        except Portfolio.DoesNotExist:
            portfolio = Portfolio.objects.create(
                portfolio_name=request.session["dowell_user"]["userinfo"]["username"],
                session_id=request.session["session_id"],
                username = request.session["dowell_user"]["userinfo"]["username"],
                email = request.session["dowell_user"]["userinfo"]["email"],
                phone = request.session["dowell_user"]["userinfo"]["phone"],
                userID = request.session["dowell_user"]["userinfo"]["userID"],
                organization = request.session["dowell_user"]["portfolio_info"][0]["orgID"],
                dowell_logged_in = True
            )


        room = Room.objects.filter(authority_portfolio__id=portfolio.id, product=kwargs['product'].lower(), sub_product=request.GET.get('prdct').lower()).first()
        if not room :
            room = Room.objects.create(
                room_name=portfolio.portfolio_name,
                room_id= portfolio.session_id,
                authority_portfolio=portfolio,
                product=kwargs['product'].lower(),
                sub_product=request.GET.get('prdct').lower()
            )
            room.save()

        messages = Message.objects.filter(room=room)
        return render(request, 'chat_box.html', {'session_id': request.GET['session_id'], 'product': kwargs['product'], 'portfolio': portfolio, 'messages': messages, 'room_pk': room.id})
    else:
        return HttpResponse('<h1>Request not accepted.<h1>')


# mobile API view handle
@dowell_login_required
def createRoomAPI(request, *args, **kwargs):
    #   print(product, session_id)

    if kwargs['product'] != 'Sales-Agent':
        return JsonResponse({'error': 'Unauthorized access prohibitted.'})

    if len(request.GET['session_id']) < 8:
        return JsonResponse({'error': 'session_id length must be more then 8 characters.'})

    try:
        portfolio = Portfolio.objects.filter(userID=request.session["dowell_user"]["userinfo"]["userID"]).first()
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(
            portfolio_name=request.session["dowell_user"]["userinfo"]["username"],
            session_id=request.session["session_id"],
            username = request.session["dowell_user"]["userinfo"]["username"],
            email = request.session["dowell_user"]["userinfo"]["email"],
            phone = request.session["dowell_user"]["userinfo"]["phone"],
            userID = request.session["dowell_user"]["userinfo"]["userID"],
            organization = request.session["dowell_user"]["portfolio_info"][0]["orgID"],
            dowell_logged_in = True
        )
    room = Room.objects.filter(authority_portfolio__id=portfolio.id, product=kwargs['product'].lower()).first()
    if not room :
        room = Room.objects.create(
            room_name=portfolio.portfolio_name,
            room_id= portfolio.session_id,
            authority_portfolio=portfolio,
            product=kwargs['product'].lower()
        )
        room.save()

    messages = Message.objects.filter(room=room)
    message_list = [jsonify_message_object(message) for message in messages]
    return JsonResponse({'session_id': request.GET['session_id'], 'product': kwargs['product'], 'portfolio': portfolio.id, 'messages': message_list, 'room_pk': room.id})



#   Before login chat sender view
@xframe_options_exempt
def chat_box_view(request, *args, **kwargs):
    try:
        portfolio = Portfolio.objects.get(session_id=request.GET['session_id'])
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(
            portfolio_name=request.GET['session_id'],
            session_id=request.GET['session_id']
        )

    room = Room.objects.filter(authority_portfolio__id=portfolio.id, product=kwargs['product'].lower()).first()
    if not room :
        room = Room.objects.create(
            room_name=portfolio.portfolio_name,
            room_id= portfolio.session_id,
            authority_portfolio=portfolio,
            product=kwargs['product'].lower()
        )
        room.save()

    messages = Message.objects.filter(room=room)
    return render(request, 'chat_box.html', {'session_id': request.GET['session_id'], 'product': kwargs['product'], 'portfolio': portfolio, 'messages': messages, 'room_pk': room.id})




# GET and POST API method for sending and receiving messages in room
@csrf_exempt
def send_message_api(request, pk):
    message = str()
    session_id = str()
    print("PK :", pk)
    room = Room.objects.get(pk=int(pk))
    if request.POST :
        message = request.POST.get('message')
        session_id = request.POST.get('session_id')
    else:
        try:
            body = request.body.decode('utf8').replace("'", '"')
            message = json.loads(body)['message']
            session_id = json.loads(body)['session_id']
        except:
            pass
        print("Session_id :", session_id , ", message : ", message, request.POST)
    if message :
        try:
            portfolio = Portfolio.objects.filter(session_id=session_id).last()
            msg = Message.objects.create(
                room=room,
                message=message,
                author=portfolio,
                read=False,
                side=False if room.room_name == session_id else True
            )
            msg.save()
        except Portfolio.DoesNotExist:
            return JsonResponse({'Error': '404', 'messages': 'portfolio Not found.'})

    messages = Message.objects.filter(room=room)
    message_list = [jsonify_message_object(message) for message in messages]
    return JsonResponse({'portfolio': session_id, 'messages': message_list, 'room_pk': room.id})




@xframe_options_exempt
def pop_up_api(request, *args, **kwargs):
    return render(request, 'index.html', {'product': kwargs['product'], 'session_id': request.GET['session_id']})


from django.urls import reverse

@dowell_login_required
def admin_support_page_view(request, *args, **kwargs):
    return redirect(reverse('customer_support:main-support-page'))

def main_support_page(request, *args, **kwargs):
    try:
        portfolio = Portfolio.objects.filter(userID=request.session["dowell_user"]["userinfo"]["userID"]).first()
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(
            portfolio_name=request.session["dowell_user"]["userinfo"]["username"],
            session_id=request.session["dowell_user"]["userinfo"]["session_id"],
            username = request.session["dowell_user"]["userinfo"]["username"],
            email = request.session["dowell_user"]["userinfo"]["email"],
            phone = request.session["dowell_user"]["userinfo"]["phone"],
            userID = request.session["dowell_user"]["userinfo"]["userID"],
            organization = request.session["dowell_user"]["portfolio_info"][0]["orgID"],
            dowell_logged_in = True
        )
        portfolio.save()
    rooms = Room.objects.all()
    for room in rooms:
        messages = Message.objects.filter(room=room)
        if len(messages) == 0:
            room.delete()
    rooms = Room.objects.filter(product=product_list_object()[0].lower()).order_by("-id")
    try:
        messages = Message.objects.filter(room=rooms[0].id)
    except:
        messages = Message.objects.none()
    return render(request, 'rt_chat_response.html', {'product_list': product_list1(), 'firstroom': rooms.first(), 'portfolio': portfolio, 'rooms': rooms, 'messages': messages, 'session_id': request.session["session_id"]})




@dowell_login_required
def living_lab_support_view(request, *args, **kwargs):
    return redirect(reverse('customer_support:main-living-lab-support-page'))

def main_living_lab_support_page(request, *args, **kwargs):
    try:
        portfolio = Portfolio.objects.filter(userID=request.session["dowell_user"]["userinfo"]["userID"]).first()
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(
            portfolio_name=request.session["dowell_user"]["userinfo"]["username"],
            session_id=request.session["dowell_user"]["userinfo"]["session_id"],
            username = request.session["dowell_user"]["userinfo"]["username"],
            email = request.session["dowell_user"]["userinfo"]["email"],
            phone = request.session["dowell_user"]["userinfo"]["phone"],
            userID = request.session["dowell_user"]["userinfo"]["userID"],
            organization = request.session["dowell_user"]["portfolio_info"][0]["orgID"],
            dowell_logged_in = True
        )

    rooms = Room.objects.all()
    for room in rooms:
        messages = Message.objects.filter(room=room)
        if len(messages) == 0:
            room.delete()

    rooms = Room.objects.filter(product=product_list1()[0].lower()).order_by("-id")
    try:
        messages = Message.objects.filter(room=rooms[0].id)
    except:
        messages = Message.objects.none()
    return render(request, 'rt_chat_response1.html', {'product_list': product_list1(), 'firstroom': rooms.first(), 'portfolio': portfolio, 'rooms': rooms, 'messages': messages, 'session_id': request.session['session_id']})




#   @dowell_login_required
def room_list(request, *agrs, **kwargs):
    firstroom = None
    rooms = None
    rm_list = []
    try:
        rooms = Room.objects.filter(product=kwargs['product'].lower()).order_by("-id")
        if rooms:
            for r in rooms:
                if r.active :
                    rm_list.append({'room_id': r.id, 'room_name': r.room_name, 'company': r.company})
            try:
                firstroom = rm_list[0]
            except:
                firstroom = {'room_id': None, 'room_name': '', 'company': ''}
        frm_id = firstroom['room_id'] if firstroom else None
        return JsonResponse({'rooms': rm_list, 'firstroom': firstroom, 'messages': [jsonify_message_object(message) for message in Message.objects.filter(room_id=frm_id)]})
    except Room.DoesNotExist:
        return JsonResponse({'rooms': []})




@xframe_options_exempt
def chat_box_userinfo_view(request, *args, **kwargs):
    context = {}
    session_id = request.GET.get('session_id')
    url = 'https://100093.pythonanywhere.com/api/userinfo/'
    response = requests.post(url, data={'session_id': session_id})
    response=response.json()
    print("login :", response)
    try:
        portfolio = Portfolio.objects.get(user_id=response['userinfo']['username'])
    except:
        portfolio = Portfolio.objects.create(
            portfolio_name=response["userinfo"]["username"],
            session_id=request.GET.get('session_id'),
            username = response["userinfo"]["username"],
            email = response["userinfo"]["email"],
            phone = response["userinfo"]["phone"],
            userID = response["userinfo"]["userID"],
            organization = response["portfolio_info"][0]["org_id"]
        )

    room = Room.objects.filter(authority_portfolio__id=portfolio.id, product=kwargs['product'].lower(), company=response["portfolio_info"][0]["org_id"]).first()
    if not room :
        room = Room.objects.create(
            room_name=portfolio.portfolio_name,
            room_id= portfolio.userID,
            product=kwargs['product'].lower(),
            authority_portfolio = portfolio,
            company=response["portfolio_info"][0]["org_id"],
        )
        room.save()
        messages = Message.objects.filter(room=room)
        context = {'session_id': request.GET['session_id'], 'product': kwargs['product'], 'portfolio': portfolio, 'messages': messages, 'room_pk': room.id}
    return render(request, 'chat_box.html', context)



def room_details(request, room_id, **kwargs):
    ##  portfolio = Portfolio.objects.get(id=room_id)
    try:
        room = Room.objects.get(id=room_id)
        messages = Message.objects.filter(room=room)
    except Room.DoesNotExist:
        return JsonResponse({'message': 'room does not exist.'})
    return render(request, 'room.html', { 'messages': messages, 'room_': room.jsonify_room})



@xframe_options_exempt
def index(request):
    return render(request, 'index.html')





'''

@dowell_login_required
def support_page_view(request, *agrs, **kwargs):
    try:
        portfolio = Portfolio.objects.get(session_id=kwargs['session_id'])
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(
            portfolio_name=kwargs['session_id'],
            session_id=kwargs['session_id']
        )

    #   room = Room.objects.filter(authority_portfolio__id=portfolio.id).first()

    rooms = Room.objects.all()
    for room in rooms:
        messages = Message.objects.filter(room=room)
        if len(messages) == 0:
            room.delete()


    rooms = Room.objects.all()
    firstroom = Room.objects.all().first()
    messages = Message.objects.all()


    return render(request, 'support_chat_box.html', {'firstroom': firstroom, 'portfolio': portfolio, 'rooms': rooms, 'messages': messages, 'session_id': kwargs['session_id']})



def user_room_list(request, *args, **kwargs):
    prdct = kwargs['product']
    try:
        rooms = Room.objects.filter(product=prdct.lower())
    except Room.DoesNotExist:
        return JsonResponse({'rooms': None})
    rm = []
    for r in rooms:
        if r.active :
            rm.append({'room_id': r.id, 'room_name': r.room_name, 'company': r.company})
    return JsonResponse({'rooms': rm })


@csrf_exempt
def main(request):
    session_id = request.GET.get("session_id", None)
    if session_id:
        field = {"SessionID": session_id}
        response = dowellconnection(*SESSION_ARGS, "fetch", field, "nil")
        res = json.loads(response)
        if res["isSuccess"]:
            request.session["session_id"] = res["data"][0]["SessionID"]
            print("Res------------- \n",res["data"])
        fields = {"Username": res["data"][0]["Username"]}
        response = dowellconnection(*REGISTRATION_ARGS, "fetch", fields, "nil")
        usrdic = json.loads(response)
        if usrdic["isSuccess"]:
            print("User Role :", usrdic["data"][0]["Role"])
            request.session["Role"] = usrdic["data"][0]["Role"]
            try:
                request.session["company_id"] = usrdic["data"][0]["company_id"]
            except:
                request.session["company_id"] = None
            request.session["user_name"] = usrdic["data"][0]["Username"]
            print("LoggedIn as : ", usrdic["data"][0])
            return redirect("documentation:home")  #   HttpResponse("hello")
        else:
            return (
                redirect_to_login()
            )  #   return redirect("https://100014.pythonanywhere.com/?code=100084")
    else:
        return redirect_to_login()



def support_chat_view(request, *args, **kwargs):
    try:
        portfolio = Portfolio.objects.get(session_id=kwargs['session_id'])
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(
            portfolio_name=kwargs['session_id'],
            session_id=kwargs['session_id']
        )

    #   room = Room.objects.filter(authority_portfolio__id=portfolio.id).first()

    rooms = Room.objects.all()
    for room in rooms:
        messages = Message.objects.filter(room=room)
        if len(messages) == 0:
            room.delete()


    rooms = Room.objects.all()
    firstroom = Room.objects.all().first()
    messages = Message.objects.all()
    return JsonResponse({'status': 200, 'room': room, 'messages': messages})




class HomeView(ListView):
    model = Portfolio
    template_name = 'home_page.html'


#django post request
@csrf_exempt
def post(request):
    if request.method == 'POST':
        print(request.POST)
        return redirect('index')
    else:
        print('is a get request')
        return render(request, 'index.html')




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

'''