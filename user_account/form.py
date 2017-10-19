from django import forms


class BallanceChangeForm(forms.Form):
    ballance_change = forms.FloatField()
