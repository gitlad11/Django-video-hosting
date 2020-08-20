from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import View, HttpResponse
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login, logout
import os
from django.conf import settings
from wsgiref.util import FileWrapper
from .models import *
from .forms import *
from django.shortcuts import redirect

class RegistrationView(View):
    template_name = 'reqistration.html'
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
            print(request.user)
        form = SignUpForm()
        return render(request, self.template_name,{'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            p1 = form.cleaned_data['password1']
            p2 = form.cleaned_data['password2']
            if p1 == p2 :
                user = User(first_name=first_name,last_name=last_name,email=email)
                user.set_password(p1)
                user.save()
                return redirect('home')
            return HttpResponse('form is not valid')
            
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, self.tamplate_name, {'form' : form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('login')
        return HttpResponse('form is not valid')


class UploadVideoView(View):
    template_name = 'upload_video.html'
     
    def get(self, request):
        if request.user.is_authenticated == False:
            return redirect('login')
        form = VideoForm()
        return render(request, self.template_name, {'form' : form})


class HomeView(ListView):
    template_name = 'home.html'
    model = Video
    paginate_by = 20
    context_object_name = 'Video'
    def get(self, request):
        recent_videos = Video.objects.order_by('created_on')
        channels = Channel.objects.all()
        user = get_user_model()
        has_channel = False
        if request.user.is_authenticated:
            try:
                channel = Channel.objects.filter(owner__username = request.user)
                channel = channel.get()
            except Channel.DoesNotExist:
                has_channel = False
        context = {'recent_videos' : recent_videos, 'channels' : channels, 'user': user}
        return render(request, self.template_name, context)

class CreateChannelView(View):
    template_name = 'create_channel.html'

    def get(self, request):
        if request.user.is_authenticated:
            try:
                if Channel.objects.filter(owner__username = request.user).get().channel_name != "":
                    return redirect('home')
            except Channel.DoesNotExist:
                form = ChannelForm()
                has_channel = False
                return render(request, self.template_name, {'form': form, 'has_channel': has_channel})

    def post(self, request):
        form = ChannelForm(request.POST)
        if form.is_valid:
            channel_name = form.cleaned_data['channel_name']
            image = form.cleaned_data['image']
            new_channel = Channel(channel_name=channel_name, image=image)
            return redirect('home')

class ChannelView(View):
    template_name = 'channel.html'

    def get(self, request, user):
        if request.user.is_authenticated:
            videos = Video.objects.filter(user__username = user).order_by("created_on")
            subscribers = Channel.subscribers
            context = {'channel':Channel.objects.filter(user__username = user).get(), 'videos': videos}
            return render(request, self.template_name, context)

class VideoDetail(View):
    template_name = 'detail_video.html'

    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        video_url = settings.MEDIA_URL+video.name

        if request.user.is_authenticated:
            comment_form = CommentForm()

        comments = Comment.objects.filter(video__id = video_id)
        
        try:
            channel = Channel.objects.filter(owner__username = request.user).get().channel_name !=""
        except Channel.DoesNotExist:
            has_channel = False
        context = {'video' : video, 'video_url' : video_url, 'comments' : comments, 'channel' : channel}
        return render(request, self.template_name, context)
        