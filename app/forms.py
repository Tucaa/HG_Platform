from django.forms import ModelForm
from django import forms
from  .models import Location, User, Data, Graph
from . import utils


# Form of the location
class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = '__all__'
        exclude = ['host', 'participants']
        
# Form for user registration
class UserForm(ModelForm):
  
    class Meta:
        model = User
        fields = ['username', 'email']

    

#Choices for graph 
CHART_CHOICES = (
    ('#1', 'Bar chart'),
    ('#1', 'Line chart'),
)

#Data choices
#DATA_CHOICES = 

# Seach form for selecting desired date for graph
# class DataForm(forms.Form):
#     # Kod datuma moras da namestis da iterira kroz datome iz fajla
#     date_from = forms.ChoiceField()
#     date_to = forms.ChoiceField()
#     chart_type = forms.ChoiceField(choices=CHART_CHOICES)


# Form for uploading file
class UploadForm(ModelForm):
    class Meta:
        model = Data
        fields = '__all__'
        exclude = ['host', 'location']


class GraphForm(ModelForm):
    description = forms.TextInput()
    dir = forms.ImageField()
    class Meta:
        model = Graph
        fields = ['description', 'dir']
    
