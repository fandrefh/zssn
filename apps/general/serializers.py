from rest_framework import serializers

from .models import Survivor, Item, Inventory


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class SurvivorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Survivor
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = '__all__'
