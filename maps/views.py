import os
import PyPDF2

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView
# from django.views.generic.edit import CreateView
from wand.image import Image

from maps.forms import BookForm, MapAttributeForm, PartForm
from maps.models import MapAttribute, ImagePart, Part, PartFile


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


class UploadBook(View):

    def get(self, request, *args, **kwargs):
        form = BookForm()
        images = PartFile.objects.all()

        ctx = {
            "form": form,
            "images": images,
        }
        return render(request, "maps/show_images.html", ctx)

    def post(self, request, *args, **kwargs):

        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()

            full_filepath = os.path.join(settings.MEDIA_ROOT, "books", str(book.pk))
            full_filepath_jpg = os.path.join(full_filepath, "jpg")

            os.makedirs(full_filepath_jpg, exist_ok=True)

            # TODO: move to celery task
            inputpdf = PyPDF2.PdfFileReader(open(book.file.file.name, "rb"))

            # Separate pdf pages
            for i in range(inputpdf.numPages):
                # TODO: rewrite with in-memory files
                output = PyPDF2.PdfFileWriter()
                output.addPage(inputpdf.getPage(i))
                file_write = os.path.join(full_filepath, "%s-%s.pdf" % (str(book.pk), i))
                with open(file_write, "wb") as outputStream:
                    output.write(outputStream)
                # Converting one page into JPG
                with Image(filename=file_write+"[0]", resolution=600) as img:
                    img.save(
                        filename=os.path.join(full_filepath_jpg, "%s-%s.jpg" % (str(book.pk), i)))

                try:
                    os.remove(file_write)
                except OSError:
                    pass

            return redirect(reverse('upload_book'))
        else:
            messages.error(request, "Form is invalid")

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
