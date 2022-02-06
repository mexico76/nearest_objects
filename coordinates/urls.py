from django.urls import path

from .views import GetSubjects, LoadCSV

urlpatterns = [
    path('csv', LoadCSV.as_view(), name="load_csv"),
    path('', GetSubjects.as_view(), name="map"),
]
