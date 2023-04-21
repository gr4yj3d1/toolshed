from django.urls import path, include

from . import views
from .api import router
from .forms import InventoryItemUpdateView, InventoryItemCreateView

urlpatterns = [
    #path('', views.index, name='index'),
    #path('settings', views.settings, name='settings'),
    #path('inventory', views.inventory, name='inventory'),
    #path('profile/<str:username>', views.profile, name='profile'),
    #path('item/new', InventoryItemCreateView, name='item_new'),
    #path('item/<str:itemid>/edit', InventoryItemUpdateView, name='item_edit'),
    # path('item/<str:itemid>/delete', views.item_delete, name='item_delete'),
    path('api/', include(router.urls)),
]
