from django.contrib.gis.geos import GEOSGeometry 
from buildings2.models import Buildings
from scripts.p1.myLib import p1Settings

def run():
    #create the geometry with geos
    g=GEOSGeometry('POLYGON((0 0, 10 0, 10 10, 0 11, 0 0))', srid=p1Settings.EPSG_CODE)
    #print the representation of the object
    if g.valid:
        print("Geometría válida")

    print(g)
    #create a building object, from the model Buildings
    b=Buildings(description='Edificio 1', area=g.area, perimeter=g.length, height=100, geom=g)
    #saves it into the database
    b.save()
    #prints the asigned id of the object in the database
    print(b.id)
    #another way to create the object with a dictionary
    d_of_values= {
        'description':'Edificio 1', 
        'area':g.area,
        'perimeter':g.length, 
        'height':100, 
        'geom':g
    }

    #b2=Buildings(d_of_values)
    #b2.save()
    #print(b2.id)

