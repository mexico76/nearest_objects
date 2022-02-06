import csv
import io

from dadata import Dadata
from geopy import distance

from nearest_objects.settings import DADA_SECRET, DADA_TOKEN

from .models import Subjects


def handle_uploaded_file(file):
    csv_file = file.read().decode('utf-8')
    io_string = io.StringIO(csv_file)
    spamreader = csv.reader(io_string, delimiter=',')
    for row in spamreader:
        if row[0] != 'address':
            Subjects.objects.create(address=row[0], postal_code=row[1],
                                    country=row[2], federal_district=row[3],
                                    region_type=row[4], region=row[5],
                                    area_type=row[6], area=row[7],
                                    city_type=row[8], city=row[9],
                                    settlement_type=row[10],
                                    settlement=row[11],
                                    kladr_id=row[12],
                                    fias_id=row[13], fias_level=row[14],
                                    capital_marker=row[15],
                                    okato=row[16], oktmo=row[17],
                                    tax_office=row[18],
                                    timezone=row[19],
                                    geo_lat=row[20], geo_lon=row[21],
                                    population=row[22],
                                    foundation_year=row[23])


def handle_address(request):
    dadata = Dadata(DADA_TOKEN, DADA_SECRET)
    result = dadata.clean("address", request['address'])
    return result, request['radius']


def get_nearest_objects(coordinates: dict, radius: int):
    center_point = (float(coordinates.get("geo_lat")),
                    float(coordinates.get("geo_lon")))
    radius = int(radius)
    confirm_subjects = []
    subjects = Subjects.objects.all()
    for subject in subjects:
        dis = distance.distance(center_point,
                                (subject.geo_lat, subject.geo_lon)).km
        if dis <= radius:
            confirm_subjects.append(subject)
    return confirm_subjects
