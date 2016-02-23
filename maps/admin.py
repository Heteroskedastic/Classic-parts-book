from django.contrib import admin

from .models import ImagePart, Motorcycle, Part, PartFile

admin.site.register(Part)
admin.site.register(ImagePart)
admin.site.register(PartFile)
admin.site.register(Motorcycle)
