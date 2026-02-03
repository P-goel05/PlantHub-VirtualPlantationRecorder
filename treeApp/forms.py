from .models import PlantTree
from django import forms

# used for plant.html 
class PlantTreeForm(forms.ModelForm):
    class Meta:
        model = PlantTree
        fields = ['tree_name', 'location', 'planted_date', 'height', 'tree_type', 'notes']
        widgets = {
            'planted_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

# used for weather.html
class TreeSelectForm(forms.Form):
    tree = forms.ModelChoiceField(
        queryset=PlantTree.objects.all(),
        # weather label
        empty_label="Select a tree" 
    )

TREE_CHOICES = [
    ('Neem', 'Neem'),
    ('Peepal', 'Peepal'),
    ('Mango', 'Mango'),
    ('Banyan', 'Banyan'),
]

# used for growth prediction
class TreeGrowthForm(forms.Form):
    tree_type = forms.ChoiceField(choices=TREE_CHOICES, label="Tree Type")
    avg_temp = forms.FloatField(label="Average Temperature (°C)", min_value=-10, max_value=50)
    water_freq = forms.IntegerField(label="Watering Frequency (per week)", min_value=0)
