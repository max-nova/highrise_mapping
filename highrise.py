import os

from pyrise import Highrise, Person, Company
from geopy import geocoders

def run():
    """
    Pulls down all people and companies in the highrise account specified
    by the HIGHRISE_SERVER and HIGHRISE_AUTH_TOKEN env vars
    and returns a dictionary in the format:
    {
        <id>: {
            'name': <name>
            'lat': <lat>,
            'lng': <lng>
        },
        ...
    }
    """
    HIGHRISE_SERVER = os.environ.get('HIGHRISE_SERVER')
    HIGHRISE_AUTH_TOKEN = os.environ.get('HIGHRISE_AUTH_TOKEN')

    if not HIGHRISE_SERVER and HIGHRISE_AUTH_TOKEN:
        raise Exception(
            'HIGHRISE_SERVER and HIGHRISE_AUTH_TOKEN are required env vars'
        )

    Highrise.set_server(HIGHRISE_SERVER)
    Highrise.auth(HIGHRISE_AUTH_TOKEN)

    gn = geocoders.GeoNames()

    data = {}
    for x in Person.all() + Company.all():
        cd = x.contact_data
        zipcode = None
        if cd.addresses:
            a = cd.addresses[0]
            zipcode = a.zip
            if zipcode:
                if type(x) == Person:
                    name = '%s %s (%s)' % (x.first_name, x.last_name, x.company_name)
                elif type(x) == Company:
                    name = x.name
                try:
                    print 'Finding lat/lng for %s' % name
                    place, (lat,lng) = gn.geocode(zipcode)
                    data[x.id] = {'name': name, 'lat': lat, 'lng': lng}
                except Exception:
                    pass
    return data

