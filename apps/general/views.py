from django.utils.translation import ugettext as _
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Item, Survivor, Inventory
from .serializers import ItemSerializer, SurvivorSerializer, InventorySerializer

# Create your views here.


class ItemListCreateAPIView(ListCreateAPIView):
    """
    Lista e Cadastra itens. Todos os campos são obrigatórios.
    """
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsAdminUser]


class SurvivorListCreateAPIView(ListCreateAPIView):
    """
    Lista e Cadastra sobreviventes. Todos os campos, exceto o infected, são obrigatórios.
    """
    serializer_class = SurvivorSerializer
    queryset = Survivor.objects.all()


class InventoryListCreateAPIView(ListCreateAPIView):
    """
    Lista e Cadastra o inventário de cada sobrevivente. Todos os campos são obrigatórios.
    """
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    permission_classes = [IsAdminUser]


class SurvivorLocationUpdate(APIView):
    """
    Atualiza parcialmente as informações dos sobreviventes.
    """

    def patch(self, request, survivor_id):
        survivor = get_object_or_404(Survivor, pk=survivor_id)
        serializer = SurvivorSerializer(survivor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': _('Atualização não realizada.')})


@api_view(['POST'])
def transaction_between_survivors(request):
    """
    Realiza a transação de troca de itens entre sobreviventes.
    Dados necessários:
    Sobrevivente 1
    Sobrevivente 2
    Item que deseja trocar do sobrevivente 1
    Item que deseja trocar do sobrevivente 2
    Quantidade que deseja trocar do sobrevivente 1
    Quantidade que deseja trocar do sobrevivente 2
    """
    try:
        survivor1 = Survivor.objects.get(id=request.data.get('survivor1'), infected=False)
        survivor2 = Survivor.objects.get(id=request.data.get('survivor2'), infected=False)
        item_survivor1 = Item.objects.get(id=request.data.get('item_survivor1'))
        item_survivor2 = Item.objects.get(id=request.data.get('item_survivor2'))
        inventory_survivor1 = Inventory.objects.get(survivor=survivor1, item=item_survivor1)
        inventory_survivor2 = Inventory.objects.get(survivor=survivor2, item=item_survivor2)
    except Survivor.DoesNotExist:
        return Response({'message': _('Um dos sobreviventes não foi encontrado na base de dados ou está infectado.')})
    except Item.DoesNotExist:
        return Response({'message': _('Item não cadastrado no sistema.')})
    except Inventory.DoesNotExist:
        return Response({'message': _('Um dos sobreviventes não tem o item no seu inventário.')})
    item_survivor1_quantity = request.data.get('item_survivor1_quantity')
    item_survivor2_quantity = request.data.get('item_survivor2_quantity')
    if survivor1 != survivor2:
        points_quantity_survivor1 = item_survivor1.points * item_survivor1_quantity
        points_quantity_survivor2 = item_survivor2.points * item_survivor2_quantity
        if points_quantity_survivor1 == points_quantity_survivor2:
            inventory_survivor1.quantity -= item_survivor1_quantity
            inventory_survivor2.quantity -= item_survivor2_quantity
            add_item_survivor1 = Inventory.objects.get(survivor=survivor1, item=item_survivor2)
            add_item_survivor1.quantity += item_survivor2_quantity
            add_item_survivor1.save()
            add_item_survivor2 = Inventory.objects.get(survivor=survivor2, item=item_survivor1)
            add_item_survivor2.quantity += item_survivor2_quantity
            add_item_survivor2.save()
            if inventory_survivor1.quantity < 0:
                inventory_survivor1.quantity = 0
                inventory_survivor1.save()
            else:
                inventory_survivor1.save()
            if inventory_survivor2.quantity < 0:
                inventory_survivor2.quantity = 0
                inventory_survivor2.save()
            else:
                inventory_survivor2.save()
            return Response({'message': _('Transação realizada com sucesso.')})
        return Response({'message': _('Erro na transação. Verifique os dados fornecidos.')})
    return Response({'message': _("Sobrevivente não pode trocar item consigo mesmo.")})


@api_view(['POST'])
def mark_survivor_as_infected(request):
    """
    Marca um sobrevivente como infectado. É necessário fornecer a informação de 3 sobreviventes que confirmam a infecção e a informação do
    infectado.
    """
    try:
        survivor1 = Survivor.objects.get(id=request.data.get('survivor1'), infected=False)
        survivor2 = Survivor.objects.get(id=request.data.get('survivor2'), infected=False)
        survivor3 = Survivor.objects.get(id=request.data.get('survivor3'), infected=False)
        survivor_infected = Survivor.objects.get(id=request.data.get('survivor_infected'))
    except Survivor.DoesNotExist:
        return Response({'message': _('Confirme se todos os sobreviventes estão cadastrados no sistema e que não estão infectados.')})
    survivor_list = set([survivor1, survivor2, survivor3])
    if len(survivor_list) >= 3 and survivor_infected not in survivor_list:
        if survivor_infected.infected:
            return Response({'message': _('Sobrevivente já marcado como infectado.')})
        else:
            survivor_infected.infected = True
            survivor_infected.save()
        return Response({'message': _('Sobrevivente marcado como infectado.')})
    return Response({'message': _('Operação não realizada. É preciso três sobreviventes únicos e o suspeito de estar infectado não pode ser quem acusa.')})


@api_view(['GET'])
def survivors_percent_infected_report(request):
    """
    Retorna o percentual de sobreviventes infectados.
    """
    survivors = Survivor.objects.all()
    infected_survivors = survivors.filter(infected=True)
    percents = infected_survivors.count() / survivors.count() * 100
    return Response({'survivors_percent_infected': '{0:.2f}'.format(percents)})


@api_view(['GET'])
def survivors_percent_not_infected_report(request):
    """
    Retorna o percentual de sobreviventes não infectados.
    """
    survivors = Survivor.objects.all()
    not_infected_survivors = survivors.filter(infected=False)
    percents = not_infected_survivors.count() / survivors.count() * 100
    return Response({'survivors_percent_not_infected': '{0:.2f}'.format(percents)})


@api_view(['GET'])
def average_item_by_survivors_report(request):
    """
    Retorna a média de itens por sobreviventes.
    """
    survivors = Survivor.objects.count()
    inventory = Inventory.objects.values('item__name').order_by('item').annotate(total_items=Sum('quantity'))
    print('inventory.all', inventory.all())
    report_data = []
    for i in inventory:
        report_data.append(
            {
                'item': i.get('item__name'),
                'survivor_average': '{0:.2f}'.format(i.get('total_items') / survivors)
            }
        )
    return Response(report_data)


@api_view(['GET'])
def points_lost_by_infected_survivors_report(request):
    """
    Retorna a quantidade de pontos perdidos por conta dos sobreviventes infectados.
    """
    infected_survivors = Survivor.objects.filter(infected=True)
    infected_survivors_list = []
    total_points_lost = 0
    for s in infected_survivors:
        infected_survivors_list.append(s.name)
        inventory = Inventory.objects.filter(survivor=s)
        for i in inventory:
            total_points_lost += i.item.points
    report_data = {
        'total_points_lost': total_points_lost,
        'infected_survivors': infected_survivors_list
    }
    return Response(report_data)
