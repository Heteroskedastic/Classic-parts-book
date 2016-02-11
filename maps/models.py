from django.db import models


class PartFile(models.Model):
    file = models.FileField(upload_to='files')
    # create_date = models.DateTimeField(auto_now=True)
    file_images = models.CharField(
        'all images', blank=True, null=True, max_length=255)

    def __str__(self):
        return self.file.name


class Part(models.Model):

    part = models.CharField('Part', max_length=255)

    def __str__(self):
        return self.part


class ImagePart(models.Model):

    image = models.ForeignKey(
        PartFile, related_name="image_part")
    part = models.ForeignKey(
        Part, related_name="part_image")

    def __str__(self):
        return self.part.part


class MapAttribute(models.Model):

    attribute = models.CharField('Attribute', max_length=255)

    def __str__(self):
        return self.attribute


class ImageCoords(models.Model):

    image = models.ForeignKey(PartFile, related_name="coord_img")
    shape = models.CharField('Shape', max_length=255)
    map_coords = models.CharField('coordinates', max_length=255)

    def __str__(self):
        return self.shape


# class MapAttributes(models.Model):

#     image_coords = models.ForeignKey(ImageCoords, related_name="map_attrs")
#     shape = models.CharField('Shape', max_length=255)

#     def __str__(self):
#         return self.shape
