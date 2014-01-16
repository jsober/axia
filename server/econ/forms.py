from django import forms


class FactionForm(forms.Form):
    faction_id = forms.IntegerField(min_value=0, required=True)
    faction_name = forms.CharField(min_length=1, max_length=50, required=True)


class StationForm(forms.Form):
    station_id = forms.IntegerField(min_value=0, required=True)
    station_name = forms.CharField(min_length=1, max_length=50, required=True)
    x = forms.IntegerField(min_value=0, required=True)
    y = forms.IntegerField(min_value=0, required=True)
    sid = forms.IntegerField(min_value=0, required=True)


class ItemForm(forms.Form):
    item_id = forms.IntegerField(min_value=0, required=True)
    item_name = forms.CharField(min_length=1, max_length=50, required=True)
    volume = forms.IntegerField(min_value=1, required=True)


class SaleItemForm(forms.Form):
    price = forms.IntegerField(min_value=0, required=True)
