from django.shortcuts import render
from .models import Room,Message
from django.conf import settings
from django.views.generic import ListView
from django.contrib.auth import get_user_model  # Import the user model class

# Create your views here.

User=get_user_model()

def index(request):
    return render(request, "chatapp/index.html")


def room(request, room_name):
    uid=room_name
    
    
    second_user_pk=str(request.user.pk)
    
    index=uid.find(second_user_pk)
    if index != -1:
        result = uid [:index + len(second_user_pk) -1 ]
    secondie=int(result)
    
    second_username=User.objects.get(pk=secondie)
    
    message=Message.objects.all()
    if Room.objects.filter(uid=room_name).exists() :
            return render(request, "chatapp/room.html", {"room_name": room_name,
                                                         "request_user": request.user,
                                                         "message":message
                                                         })

    
    else :
        room_named=Room.objects.create(name=room_name,first_user=request.user,second_user=second_username,uid=room_name)
        
        return render(request, "chatapp/room.html", {"room_name": room_named,
                                                     "request_user": request.user,
                                                     "message":message})

def room_page(request):
    rooms=Room.objects.all()
    users=User.objects.all()
    
    context = {
        'rooms': rooms,
        'users': users
    }
    return render(request,'chatapp/admins.html',context)

class DirectMessage(ListView):
    model=Room
    

