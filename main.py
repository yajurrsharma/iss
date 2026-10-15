from datetime import datetime
import json
from skyfield.api import EarthSatellite, load, wgs84

with load.open('stations.json') as f:
    data = json.load(f)


ts = load.timescale()
sats = [EarthSatellite.from_omm(ts, fields) for fields in data]
# print("loaded", len(sats), "satellites")

by_name = {sat.name: sat for sat in sats}
satellite = by_name['ISS (ZARYA)']


t = ts.now()

patiala = wgs84.latlon(30.3260, 76.4019)
difference = satellite - patiala

topocentric = difference.at(t)
# print(topocentric.xyz.km) #relative to patiala in gcrs

alt, az, distance = topocentric.altaz()

# print(alt)
# print(az)
# print("Distance: {:.1f} km".format(distance.km))

eph = load('de421.bsp')

earth = eph['earth']
sun = eph['sun']

sun_topocentric = (earth + patiala).at(t).observe(sun).apparent()
sun_alt, sun_az, sun_distance = sun_topocentric.altaz()

sunlit = satellite.at(t).is_sunlit(eph)

if alt.degrees > 30 and sunlit and sun_alt.degrees < -6:
    print("The ISS is visible from Patiala right now!")