import requests
from django.shortcuts import render

def home(request):
    response = requests.get('https://data.police.uk/api/crimes-street/all-crime?lat=52.629729&lng=-1.131592&date=2013-01')
    entries = response.json()[:]
    return render(request, 'home.html', {'entries': entries})
