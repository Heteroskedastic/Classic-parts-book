from django.contrib import admin

from .models import *

admin.site.register(Part)
admin.site.register(ImagePart)
admin.site.register(PartFile)
