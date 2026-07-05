from django import forms
from MyApp.models import ymodel, emodel

# A3 FIX: Removed duplicate imports (was imported 3 times)
# A3 FIX: yform and eform now explicitly declare ALL fields they use.
# Previously only YNAME/YPIC and ENAME/EVIDEO were declared — the Meta
# block was silently ignored because forms.Form doesn't use Meta.

class yform(forms.Form):
    YNAME = forms.CharField(max_length=100)
    YTYPE = forms.CharField(max_length=50, required=False)
    YDESC = forms.CharField(max_length=6000, widget=forms.Textarea, required=False)
    YPIC  = forms.FileField()

class eform(forms.Form):
    ENAME  = forms.CharField(max_length=100)
    ETYPE  = forms.CharField(max_length=50, required=False)
    EDESC  = forms.CharField(max_length=6000, widget=forms.Textarea, required=False)
    EVIDEO = forms.FileField()

class BMRForm(forms.Form):
    weight = forms.IntegerField(label='Weight (kg)')
    height = forms.IntegerField(label='Height (cm)')
    age = forms.IntegerField(label='Age')
    gender = forms.ChoiceField(
        label='Gender',
        choices=[('Male', 'Male'), ('Female', 'Female')]
    )
    other_conditions = forms.CharField(
        label='Medical Conditions (if any)',
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True  # force the user to type "None" if no conditions
    )
    activity = forms.ChoiceField(
        label='Activity Level',
        choices=[
            ('Sedentary (little or no exercise)', 'Sedentary (little or no exercise)'),
            ('Lightly active (1-3 days/week)', 'Lightly active (1-3 days/week)'),
            ('Moderately active (3-5 days/week)', 'Moderately active (3-5 days/week)'),
            ('Very active (6-7 days/week)', 'Very active (6-7 days/week)'),
            ('Super active (twice/day)', 'Super active (twice/day)')
        ]
    )
