'''
This is a python script that requires you have python installed, or in a cloud environment.

This script scrapes the CVS website looking for vaccine appointments in the cities you list.
To update for your area, update the locations marked with ### below.

If you receive an error that says something is not install, type

pip install beepy

in your terminal.
'''

import requests
import time
import beepy

APPOINTMENT_STATUSES = {
    "BOOKED": "Fully Booked"
}
# Update with your cities nearby
cities = ['EL MONTE', 'WEST COVINA', 'SAN GABRIEL',
          'ALHAMBRA', 'PASADENA', 'ARCADIA', "MONTEREY PARK",
          "TEMPLE CITY", "LA PUENTE", "MONTEBELLO", "BALDWIN PARK",
          "MONROVIA"]

priorities = {
    "EL MONTE": 10,
    "ARCADIA": 9,
    "TEMPLE CITY": 8,
    "ALHAMBRA": 7,
}

state = 'CA'  # Update with your state abbreviation. Be sure to use all CAPS, e.g. RI
secToNextRun = 60
# Update this to set the number of hours you want the script to run.
hoursToRun = 3
soundToMake = 'success'

def findAVaccine():
    max_time = time.time() + hoursToRun*60*60
    while time.time() < max_time:

        vaccineInfoUrl = "https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{}.json?vaccineinfo"
        response = requests.get(vaccineInfoUrl.format(state.lower()), headers={
                                "Referer": "https://www.cvs.com/immunizations/covid-19-vaccine"})
        payload = response.json()

        mappings = {}
        for item in payload["responsePayloadData"]["data"][state]:
            mappings[item.get('city')] = item.get('status')

        print(time.ctime())
        for city in cities:
            print(city, mappings[city])

        available = []
        for key in mappings.keys():
            if (key in cities) and (mappings[key] != APPOINTMENT_STATUSES["BOOKED"]):
                available.append(key)
                pass
            else:
                pass

        if (len(available) > 0):
            available.sort(reverse=True, key=prioritySort)
            print("\n")
            print("Appointments Available at:")
            print(available)
            print("Go to the link to book: https://www.cvs.com/immunizations/covid-19-vaccine")
            print("More Specific Site: https://www.cvs.com/vaccine/intake/store/cvd-schedule?icid=coronavirus-lp-vaccine-sd-statetool")
            beepy.beep(sound=soundToMake)
        # This runs every 60 seconds. Update here if you'd like it to go every 10min (600sec)
        time.sleep(secToNextRun)
        print('\n')


def prioritySort(city):
    return priorities.get(city, 0)


findAVaccine()  # this final line runs the function. Your terminal will output the cities every 60seconds
