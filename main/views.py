from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
#from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Cliente
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password'] == request.POST['confirmP']:
            try:
                #registrando un usuario
                user = User.objects.create_user(username=request.POST['usuario'],password=request.POST['password'])
                user.save()
                login(request,user)
                return redirect('inicio')
            except IntegrityError:
                return render(request,'signup.html',{
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request,'signup.html',{
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })


def signin(request):

    if request.method =='GET':    
        return render(request,'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,username=request.POST['usuario'],password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request,user)
            return redirect('inicio')

def grafico(request):
    # print("hola")
    # usuario = User.objects.last()
    # print(usuario.EsDeudor() )
    if request.user.is_authenticated:
        volAgua = [500,100,10,50,200]
        
        return render(request,'grafico.html',{'volAgua': volAgua})
    else:
        return redirect('signin')
    
def inicio(request):
    if request.user.is_authenticated:
        if(request.user.EsDeudor()):
            usuario = User.objects.last()
            print('Hola')
            print(usuario.Deuda())
            return render(request,"inicio.html")
        else:
            return render(request,"inicio.html",{'deuda': 0})
    else:
        return redirect('signin') 

def signout(request):
    logout(request)
    return redirect('signin')