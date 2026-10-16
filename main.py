from datetime import datetime
import json
from skyfield.api import EarthSatellite, load, wgs84

def load_satellite_data(json_path='stations.json'):
    with load.open(json_path) as f:
        data = json.load(f)
    ts = load.timescale()
    sats = [EarthSatellite.from_omm(ts, fields) for fields in data]
    by_name = {sat.name: sat for sat in sats}
    return ts, by_name['ISS (ZARYA)']

def load_ephemeris(bsp_path='de421.bsp'):
    return load(bsp_path)

# ts, satellite = load_satellite_data()
# eph = load_ephemeris()

# t = ts.now()
# observer = wgs84.latlon(lat, lon)
# difference = satellite - observer
# topocentric = difference.at(t)

# alt, az, distance = topocentric.altaz()

# earth = eph['earth']
# sun = eph['sun']
# sun_topocentric = (earth + observer).at(t).observe(sun).apparent()
# sun_alt, sun_az, sun_distance = sun_topocentric.altaz()

# sunlit = satellite.at(t).is_sunlit(eph)

# if alt.degrees > 30 and sunlit and sun_alt.degrees < -6:
#     return True
# return False