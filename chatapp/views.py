from django.shortcuts import render
from .models import Room,Message
from django.conf import settings
from django.views.generic import ListView
from django.contrib.auth import get_user_model  # Import the user model class
from django.db.models import Q


# Create your views here.

User=get_user_model()

def index(request):
    return render(request, "chatapp/index.html")


def room(request, room_name):
    room_named=int(room_name)
    uid=room_named
    second_username=User.objects.get(pk=room_named)
    if Room.objects.get(uid=uid) :
            roomi=Room.objects.get(uid=uid)
            message=Message.objects.filter(room=roomi)
            print(message)
            return render(request, "chatapp/room.html", {"room_name": uid,
                                                         "request_user": request.user,
                                                         "message":message,
                                                         'roomi':roomi,
                                                         'second_username' : second_username
                                                         })

    
    else :
        room_created=Room.objects.create(name=room_name,first_user=request.user,second_user=second_username,uid=room_name)
        
        return render(request, "chatapp/room.html", {"room_name": room_created,
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
    
    def get(self,request):
        requested_user = User.objects.get(pk=request.user.pk)
        
        related_room = Room.objects.filter (Q(first_user=requested_user) | Q(second_user=requested_user))
        
        context = {
            'request_user' : requested_user,
            'room' : related_room
        }
        
        return render(request,'chatapp/room_list.html',context)