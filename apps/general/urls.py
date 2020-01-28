from django.urls import path

app_name = 'general'

from . import views

urlpatterns = [
    path('items/', views.ItemListCreateAPIView.as_view(), name='items'),
    path('survivors/', views.SurvivorListCreateAPIView.as_view(), name='survivors'),
    path('inventories/', views.InventoryListCreateAPIView.as_view(), name='inventories'),
    path('survivor-location-update/<int:survivor_id>/', views.SurvivorLocationUpdate.as_view(), name='survivor_location_update'),
    path('transactions/', views.transaction_between_survivors, name='transactions'),
    path('mark-survivor-infected/', views.mark_survivor_as_infected, name='mark_survivor_as_infected'),
    path('infected-survivors/', views.survivors_percent_infected_report, name='survivors_percent_infected_report'),
    path('not-infected-survivors/', views.survivors_percent_not_infected_report, name='survivors_percent_not_infected_report'),
    path('average-item-survivors/', views.average_item_by_survivors_report, name='average_item_by_survivors_report'),
    path('points-lost-infected-survivors/', views.points_lost_by_infected_survivors_report, name='points_lost_by_infected_survivors_report'),
]
