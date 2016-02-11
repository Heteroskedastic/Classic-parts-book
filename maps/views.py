import os
import PyPDF2
from maps.forms import *
from django.shortcuts import render
from django.views.generic import View
from django.views.generic import TemplateView
# from django.views.generic.edit import CreateView
from maps.models import *
from wand.image import Image
from datetime import datetime
from django.contrib import messages
from image_mapping import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class HomeView(TemplateView):
    template_name = "home.html"


class ImageMapView(View):
    # template_name = "index.htm"

    def get(self, request, *args, **kwargs):
        map_attrs = MapAttribute.objects.all()
        ctx = {
            'map_attrs': map_attrs,
        }
        return render(request, "index.htm", ctx)

    def post(self, request, *args, **kwargs):

        image_coords = request.POST['img_coords'].replace('\n', '')
        list_shp_coords = image_coords.split('\r')

        for shape_cord in list_shp_coords:
            if shape_cord.startswith('shape'):
                print(shape_cord.replace("shape- ", ""))
            else:
                print(shape_cord.replace("coords- ", ""))

        return render(request, "index.htm", {})


class ShowImageView(View):

    def get(self, request, *args, **kwargs):
        form = ImageForm()
        images = PartFile.objects.all()

        ctx = {
            "form": form,
            "images": images,
        }
        return render(request, "maps/show_images.html", ctx)

    def post(self, request, *args, **kwargs):

        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            part_file = PartFile.objects.get(file_images=None)

            file_name = request.FILES['file'].name
            current_timestamp = datetime.now().strftime('%d%m%Y_%H%M%S')
            file_ = current_timestamp + " " + file_name
            part_file.file_images = file_
            part_file.save()
            try:
                os.mkdir(os.path.join(
                    settings.MEDIA_ROOT, file_))
            except:
                pass

            full_filename = os.path.join(
                settings.MEDIA_ROOT, file_)

            try:
                os.mkdir(os.path.join(full_filename, "jpg"))
            except:
                pass

            get_file_ins = PartFile.objects.get(file="files/"+file_name)
            open_file = get_file_ins.file._get_path()
            inputpdf = PyPDF2.PdfFileReader(open(open_file, "rb"))

            # Separate pdf pages
            for i in range(inputpdf.numPages):
                output = PyPDF2.PdfFileWriter()
                output.addPage(inputpdf.getPage(i))
                file_write = full_filename + '/' + "%s-%s.pdf" % (file_name, i)
                with open(file_write, "wb") as outputStream:
                    output.write(outputStream)
                # Converting one page into JPG
                with Image(filename=file_write+"[0]") as img:
                    img.save(
                        filename=full_filename+"/jpg/"+"%s-%s.jpg" % (file_, i))

                try:
                    os.remove(file_write)
                except OSError:
                    pass

            return redirect(reverse('image_show'))
        else:
            messages.error(request, "Form is Invaid")

        images = PartFile.objects.all()
        ctx = {
            "form": form,
            "images": images,
        }
        return render(request, "maps/show_images.html", ctx)


class AddPartsView(View):

    def get(self, request, *args, **kwargs):

        pk = kwargs['id']
        image = PartFile.objects.get(pk=pk)
        parts = Part.objects.all()

        form_part = PartForm()
        ctx = {
            "image": image,
            "parts": parts,
            "form_part": form_part,
        }
        return render(request, "maps/add_parts.html", ctx)

    def post(self, request, *args, **kwargs):

        pk = kwargs['id']
        img = request.POST.get('image')
        parts = request.POST.getlist('parts[]')
        form_part = PartForm(request.POST)

        if parts:
            imgs = PartFile.objects.get(pk=img)
            for part in parts:
                img_part = Part.objects.get(pk=part)
                image_part = ImagePart(image=imgs, part=img_part)
                image_part.save()

        elif form_part.is_valid():
            form_part.save()
        else:
            messages.error(request, "Form is Invaid")

        return redirect(reverse('add_part', kwargs={'id': pk}))


class MapCreate(View):

    def get(self, request, *args, **kwargs):

        form = MapAttributeForm()
        map_attrs = MapAttribute.objects.all()

        ctx = {
            "form": form,
            "map_attrs": map_attrs,
        }
        return render(request, "maps/mapattribute_form.html", ctx)

    def post(self, request, *args, **kwargs):

        form = MapAttributeForm(request.POST)
        map_attrs = MapAttribute.objects.all()

        ctx = {
            "form": form,
            "map_attrs": map_attrs,
        }
        if form.is_valid():
            form.save()
            return render(request, "maps/mapattribute_form.html", ctx)
        else:
            messages.error(request, "Form is Invaid")

        return redirect(reverse('map_create'))


# class PartCreate(CreateView):
#     model = Part
#     fields = ['part']
#     success_url = '/images/'
