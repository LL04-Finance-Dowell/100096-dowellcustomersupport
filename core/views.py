from django.shortcuts import render, redirect
from django.http import JsonResponse
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




SESSION_ARGS = ["login", "bangalore", "login", "login", "login", "6752828281", "ABCDE"]
REGISTRATION_ARGS = [
    "login",
    "bangalore",
    "login",
    "registration",
    "registration",
    "10004545",
    "ABCDE",
]



def dowellconnection(cluster,database,collection,document,team_member_ID,function_ID,command,field,update_field):
    url = "http://100002.pythonanywhere.com/"
        #searchstring="ObjectId"+"("+"'"+"6139bd4969b0c91866e40551"+"'"+")"
    payload = json.dumps({
        "cluster": cluster,
        "database": database,
        "collection": collection,
        "document": document,
        "team_member_ID": team_member_ID,
        "function_ID": function_ID,
        "command": command,
        "field": field,
        "update_field": update_field,
        "platform": "bangalore"
        })
    headers = {
        'Content-Type': 'application/json'
        }

    response = requests.request("POST", url, headers=headers, data=payload)
    res= json.loads(response.text)

    return res


def user_passes_test(test_func, login_url='https://100014.pythonanywhere.com/?code=100096', redirect_field_name=REDIRECT_FIELD_NAME):
    def decorator(view_func):
        @wraps(view_func)
        def rt_wrapper(request, *args, **kwargs):
            session_id = request.GET.get("session_id", None)
            if session_id:
                res = json.loads(dowellconnection(*SESSION_ARGS, "fetch", {"SessionID": session_id}, "nil"))
                if res["isSuccess"]:
                    request.session["session_id"] = res["data"][0]["SessionID"]
                    print("Res------------- \n",res["data"])

                usrdic = json.loads(dowellconnection(*REGISTRATION_ARGS, "fetch", {"Username": res["data"][0]["Username"]}, "nil"))
                if test_func(usrdic["isSuccess"]):
                    request.user.is_authenticated = usrdic["isSuccess"]

                    print("User Role :", usrdic["data"][0]["Role"])
                    request.session["Role"] = usrdic["data"][0]["Role"]
                    try:
                        request.session["company_id"] = usrdic["data"][0]["company_id"]
                    except:
                        request.session["company_id"] = None
                    request.session["user_name"] = usrdic["data"][0]["Username"]
                    print("LoggedIn as : ", usrdic["data"][0])
                    return view_func(request, *args, **kwargs)  #   HttpResponse("hello")
                else:
                    return redirect(login_url)                                                                                           #   return redirect("https://100014.pythonanywhere.com/?code=100084")
            else:
                return redirect(login_url)


        return rt_wrapper
    return decorator



def dowell_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='https://100014.pythonanywhere.com/?code=100096'):
    actual_decorator = user_passes_test(
        lambda is_authenticated: is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator





def jsonify_message_object(mess_obj):
    return ({
        'id': mess_obj.id,
        'timestamp' : mess_obj.timestamp,
        'room_id' : mess_obj.room_id,
        'read': mess_obj.read,
        'message': mess_obj.message,
        'author' : { 'id': mess_obj.author.id, 'session_id':mess_obj.author.session_id }
    })








@xframe_options_exempt
def chat_box_view(request, *args, **kwargs):
    try:
        portfolio = Portfolio.objects.get(session_id=request.GET['session_id'])
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(
            portfolio_name=request.GET['session_id'],
            session_id=request.GET['session_id']
        )

    room = Room.objects.filter(authority_portfolio__id=portfolio.id).first()
    if not room :
        room = Room.objects.create(
            room_name=portfolio.portfolio_name,
            room_id= portfolio.session_id,
            product=kwargs['product']
        )
        room.authority_portfolio.add(portfolio)
    messages = Message.objects.filter(room=room)
    return render(request, 'chat_box.html', {'session_id': request.GET['session_id'], 'product': kwargs['product'], 'portfolio': portfolio, 'messages': messages, 'room_pk': room.id})




# GET and POST API method for sending and receiving messages in room
@csrf_exempt
def send_message_api(request, pk):
    message = request.POST.get('message')
    session_id = request.POST.get('session_id')
    room = Room.objects.get(pk=pk)

    print("Session_id :", session_id , ", message : ", message)

    if message :
        try:
            portfolio = Portfolio.objects.get(session_id=session_id)
        except Portfolio.DoesNotExist:
            return JsonResponse({'Error': '404', 'messages': 'portfolio Not found.'})
        Message.objects.create(
            room=room,
            message=message,
            author=portfolio,
            read=True
        )
    messages = Message.objects.filter(room=room)
    message_list = [jsonify_message_object(message) for message in messages]

    return JsonResponse({'portfolio': session_id, 'messages': message_list, 'room_pk': room.id})




#   @dowell_login_required
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



@xframe_options_exempt
def test(request):
    return JsonResponse({"status":"it is working"})


























'''

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



def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator



def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator










'''















def index(request):
    return render(request, 'index.html')



'''

def support_chat_view(request, *args, **kwargs):
    try:
        portfolio = Portfolio.objects.get(session_id=request.GET['session_id'])
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(
            portfolio_name=request.GET['session_id'],
            session_id=request.GET['session_id']
        )


    room = Room.objects.filter(authority_portfolio__id=portfolio.id).first()
    if not room :
        room = Room.objects.create(
            room_name=portfolio.portfolio_name,
            room_id= portfolio.session_id,
            product=kwargs['product']
        )
        room.authority_portfolio.add(portfolio)
    messages = Message.objects.filter(room=room)
    return JsonResponse({'status': 200, 'room': room, 'messages': messages})

'''


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