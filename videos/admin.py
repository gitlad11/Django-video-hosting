from django.contrib import admin
from .models import *

admin.site.register([Video, Comment, Channel, Profile])
