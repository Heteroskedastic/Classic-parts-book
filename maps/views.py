import json
import os
import PyPDF2

from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, TemplateView
# from django.views.generic.edit import CreateView
from wand.image import Image

from maps.forms import BookForm, MapAttributeForm, PartForm
from maps.models import MapAttribute, ImagePart, Part, PartFile, Motorcycle


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
                media_url = os.path.join("books", str(book.pk), "jpg", "%s-%s.jpg" % (str(book.pk), i + 1))
                with open(file_write, "wb") as outputStream:
                    output.write(outputStream)
                # Converting one page into JPG
                img_path = os.path.join(full_filepath_jpg, "%s-%s.jpg" % (str(book.pk), i + 1))
                with Image(filename=file_write+"[0]", resolution=600) as img:
                    img.save(filename=img_path)
                    image_part = ImagePart.objects.create(part_file=book, page=i+1)
                    image_part.image.name = media_url
                    image_part.save()

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

class BookPageView(JSONResponseMixin, AjaxResponseMixin, View):
    def process_pages(self, book_id, page_id):
        image = ImagePart.objects.filter(part_file__pk=book_id, page=page_id).first()
        prev = ImagePart.objects.filter(part_file__pk=book_id, page=page_id-1).first()
        next_ = ImagePart.objects.filter(part_file__pk=book_id, page=page_id+1).first()
        res = {'image': image, 'page': page_id, 'next': None, 'prev': None}
        if prev:
            res['prev'] = prev
        if next_:
            res['next'] = next_
        return res

    def get(self, request, *args, **kwargs):
        book = PartFile.objects.get(pk=kwargs['book_id'])
        page_id = int(kwargs.get('page_id', 1))
        ctx = {'book': book}
        ctx.update(self.process_pages(kwargs['book_id'], page_id=page_id))

        return render(request, "maps/book.html", ctx)

    def post_ajax(self, request, *args, **kwargs):
        res = self.process_pages(kwargs.get('book_id'), int(kwargs.get('page_id')))
        ctx = {
            'image': res['image'].image.url,
            'prev': res['prev'].image.url if res['prev'] else None,
            'next': res['next'].image.url if res['next'] else None,
            'page': res['page']
        }
        return HttpResponse(json.dumps(ctx), content_type="application/json")


class MotorcycleView(View):
    def get(self, request, *args, **kwargs):
        moto = get_object_or_404(Motorcycle, pk=kwargs['moto_id'])
        ctx = {"motorcycle": moto}
        return render(request, "maps/motorcycle.html", ctx)
