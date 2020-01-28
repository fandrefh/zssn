from django.test import TestCase

from ..models import Inventory, Item, Survivor

# Create your tests here.


class ItemTestCase(TestCase):

    def setUp(self):
        Item.objects.create(name='Água', points=4)
        Item.objects.create(name='Alimentação', points=1)

    def test_return_str_method(self):
        item1 = Item.objects.get(name='Água')
        item2 = Item.objects.get(name='Alimentação')
        self.assertEquals(item1.__str__(), "Água")
        self.assertEquals(item2.__str__(), "Alimentação")


class InventoryTestCase(TestCase):

    def setUp(self):
        survivor = Survivor.objects.create(
            name="Francisco André",
            age=38,
            gender="M",
            longitude=123,
            latitude=321
        )
        item = Item.objects.create(name='Água', points=4)
        Inventory.objects.create(survivor=survivor, item=item, quantity=2)

    def test_return_str_method(self):
        inventory = Inventory.objects.get(id=1)
        self.assertEquals(inventory.__str__(), "Francisco André")


class SurvivorTestCase(TestCase):

    def setUp(self):
        Survivor.objects.create(
            name="Francisco André",
            age=38,
            gender="M",
            longitude=123,
            latitude=321
        )

    def test_return_str_method(self):
        survivor = Survivor.objects.get(name="Francisco André")
        self.assertEquals(survivor.__str__(), "Francisco André")