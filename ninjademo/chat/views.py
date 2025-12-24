from django.shortcuts import render

# Create your views here.

def ChatView(request):
    return render(request,'chat/chat.html')