from django.test import TestCase
from django.utils import timezone

from maps.models import Motorcycle, Part


class PartTestCase(TestCase):
    def setUp(self):
        self.moto = Motorcycle.objects.create(model='harley davidson',
                                              year_start=timezone.now(),
                                              year_end=timezone.now())

    def test_part_creation(self):
        part = Part.objects.create(part='engine', unit=self.moto)
        self.assertEqual(list(Part.objects.all()), [part])
        self.assertEqual([part.unit], list(Motorcycle.objects.all()))
