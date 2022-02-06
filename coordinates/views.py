from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View

from .forms import AdressAndRadiusForm, UploadFileForm
from .services import get_nearest_objects, handle_address, handle_uploaded_file
from nearest_objects.settings import YANDEX_API_TOKEN


class LoadCSV(View):
    def get(self, request):
        csv_form = UploadFileForm()
        return render(request, 'coordinates/load_csv.html',
                      {'csv_form': csv_form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/')
        else:
            form = UploadFileForm()
            return render(request, 'coordinates/load_csv.html', {'form': form})


class GetSubjects(View):
    def get(self, request):
        map_form = AdressAndRadiusForm()
        return render(request, 'coordinates/map.html', {'map_form': map_form})

    def post(self, request):
        form = AdressAndRadiusForm(request.POST)
        if form.is_valid():
            address, radius = handle_address(request.POST)
            coordinates = {'geo_lat': address['geo_lat'],
                           'geo_lon': address['geo_lon']}
            nearest_objects = get_nearest_objects(coordinates=coordinates,
                                                  radius=radius)
            map_form = AdressAndRadiusForm()
            return render(request, 'coordinates/render_map.html',
                          {"address": address, 'radius': radius,
                           'nearest_objects': nearest_objects,
                           'yandex_token': YANDEX_API_TOKEN,
                           'map_form': map_form},)
        else:
            form = AdressAndRadiusForm()
            return render(request, 'coordinates/map.html', {'form': form})
