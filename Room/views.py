from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserInfo, Crypto, Orders, App
from .form import UserRegister, OrderRegister
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from random import randint
from Room.utils import send_mail_auth, calculate_indicators

# Create your views here.
api_key = ''
api_secret = ''
api_pass = ''
#client = Client(api_key, api_secret, api_pass)

def register(request):
    if request.method == 'POST':
        reg_form = UserRegister(request.POST)
        if reg_form.is_valid():
            name = reg_form.cleaned_data['name']
            family = reg_form.cleaned_data['family']
            email = reg_form.cleaned_data['email']
            user = reg_form.save()
            token = Token.objects.create(user=user)
            UserInfo(user=user, name=name, family_name=family, email=email, api_key=token).save()
            user.is_active = False
            user.save()
            number = randint(100000, 999999)
            request.session['auth_number'] = number
            request.session['user_id'] = user.id
            send_mail_auth(number, email)
            print(request.session['auth_number'])
            return redirect('auth_user')

    else:
        reg_form = UserRegister()

    context = {'form': reg_form}
    return render(request, 'register.html', context)

@login_required(login_url='/accounts/login/')
def room(request, crypto_name):
    crypto = Crypto.objects.get(name=crypto_name)
    symbol = crypto.crypto_type.replace('-', '') + 'T'
    calculate_indicators(crypto)
    order_form = OrderRegister()


    context = {'crypto': crypto, 'symbol': symbol, 'form': order_form}
    return render(request, 'room.html', context)


@login_required(login_url='/accounts/login')
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    context = {}

    if user_id == request.user.id:
        context['user'] = user
        context['orders'] = Orders.objects.filter(user=user)

    return render(request, 'userprofile.html', context)


def homepage(request):
    app = App.objects.get(version='1')
    context = {'app': app}
    return render(request, 'base.html', context)


def buy(request):
    pass

def sell(request):
    pass


def auth_user(request):
    mes = ''
    user = User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        number = int(request.POST['auth_number'])

        if number == request.session['auth_number']:
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('homepage')

        else:
            mes = 'Please Enter the right number.'

    context = {'mes': mes}
    return render(request, 'auth_user.html', context)


class ApiUserInfo(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = UserInfo.objects.get(api_key=request.headers['Authorization'].split(' ')[1])

        return Response({'email': user.email,
                         'clientoid': user.cliend_oid,
                         'money': user.money_amount,
                         })



class GetOrders(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = UserInfo.objects.get(api_key=request.headers['Authorization'].split(' ')[1])
        orders = Orders.objects.filter(user=user.user)
        ord = {}
        for order in range(len(orders)):
            if orders[order].complete:
                ord[order] = {'order_id': orders[order].order_id,
                                        'oder_amount': orders[order].order_amount,
                                        'order_type': orders[order].order_type,
                                        'order_size': orders[order].order_size,
                }

        print(ord)
        return Response({
         'orders': ord,
        })

