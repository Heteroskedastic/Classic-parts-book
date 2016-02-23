from django.db import models


class PartFile(models.Model):
    part = models.ForeignKey('Part')
    file = models.FileField(upload_to='books')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Part(models.Model):
    part = models.CharField('Part', max_length=255)
    unit = models.ForeignKey('Motorcycle')

    def __str__(self):
        return self.part


class ImagePart(models.Model):

    part_file = models.ForeignKey(PartFile, related_name='image_part')
    image = models.FileField(verbose_name='Book page')

    def __str__(self):
        return self.part_file.part


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

class Motorcycle(models.Model):
    image = models.ImageField(verbose_name='Motorcycle preview')
    model = models.CharField(verbose_name='Motorcycle model name', max_length=1024)
    year_start = models.DateTimeField(verbose_name='Year of start production')
    year_end = models.DateTimeField(verbose_name='Year of end production', blank=True, null=True)

    def __str__(self):
        return '{} - year: {}'.format(self.model, self.year_start)
