from django.forms import ModelForm
from django.shortcuts import render
from django.views.generic import UpdateView

from toolshed.models import InventoryItem


class InventoryItemForm(ModelForm):
    class Meta:
        model = InventoryItem
        # fields = ('name', 'email', 'job_title', 'bio')
        fields = '__all__'


# class InventoryItemUpdateView(UpdateView):
#    model = InventoryItem
#    form_class = InventoryItemForm
#    template_name = 'form.html'


def InventoryItemUpdateView(request, itemid):
    item = InventoryItem.objects.get(id=itemid)
    form = InventoryItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
    return render(request, 'form.html', {'form': form})


def InventoryItemCreateView(request):
    form = InventoryItemForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, 'form.html', {'form': form})
