from database import get_all
from skyfield.api import load
from main import *
import datetime

users = get_all()

if not users:
    exit()

ts, satellite = load_satellite_data('stations.json')
eph = load_ephemeris('de421.bsp')
earth = eph['earth']
sun = eph['sun']

t = ts.now()
minutes_step = range(0, 1440, 1)
time = ts.tt_jd(t.tt + [m / 1440.0 for m in minutes_step])

iss_sunlit = satellite.at(time).is_sunlit(eph)
sun_state = earth.at(time).observe(sun).apparent()
sun_alt, sun_az, sun_distance = sun_state.altaz()


for email, lat, lon in users:

    observer = wgs84.latlon(lat, lon)

    topo_iss = (satellite-observer).at(time)
    alt_array, az_array, distance_array = topo_iss.altaz()

    pass_f = False

    for i in range(len(time)):
        if alt_array.degrees[i] > 30 and iss_sunlit[i] and sun_alt.degrees[i] < -6:
            pass_time = time[i].utc_datetime()
            pass_f = True

            """
            email code
            """

            break

        if not pass_f:
            print(f"no pass for {email} in the next 24 hours.")


