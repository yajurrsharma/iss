import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from skyfield.api import wgs84
from dotenv import load_dotenv, find_dotenv
from main import load_satellite_data, load_ephemeris

RENDER_WORKER_URL = "https://iss-worker.onrender.com/api/schedule-alert"
env_file = find_dotenv()
has_env =  bool(env_file and os.path.exists(env_file))
load_dotenv(env_file)

print("loading ephemeris data.")
ts, satellite = load_satellite_data('stations.json')
eph = load_ephemeris('de421.bsp')
earth = eph['earth']
sun = eph['sun']
print("Ephemeris loaded.")

def send_email(email, pass_t, pass_f):
    pass_time_str = pass_t.utc_datetime().strftime("%Y-%m-%d %H:%M:%S")
    
    payload = {
        "email": email,
        "pass_time_utc": pass_time_str,
        "pass_info": pass_f
    }
    
    try:
        response = requests.post(RENDER_WORKER_URL, json=payload, timeout=10)
        response.raise_for_status()
        print("dispatched alert to render worker:", response.json())
        return True
    except Exception as e:
        print(f"failed: {e}")
        return False

def process(email, lat, lon):   
    t_start = ts.now()
    observer = wgs84.latlon(lat, lon)
    
    for day_offset in range(14):
        start_ = t_start.tt + day_offset
        time = ts.tt_jd(start_ + [m / 1440.0 for m in range(0, 1440, 1)])

        iss_sunlit = satellite.at(time).is_sunlit(eph)
        sun_alt, sun_az, sun_distance = (earth + observer).at(time).observe(sun).apparent().altaz()
        topo_iss = (satellite - observer).at(time)
        alt_array, az_array, range_array = topo_iss.altaz()

        in_pass = False
        peak_alt = 0
        pass_peak_time = None

        for i in range(len(time)):
            is_visible = alt_array.degrees[i] > 30 and iss_sunlit[i] and sun_alt.degrees[i] < -6

            if is_visible:
                if not in_pass:
                    in_pass = True
                    peak_alt = alt_array.degrees[i]
                    pass_peak_time = time[i]
                else:
                    if alt_array.degrees[i] > peak_alt:
                        peak_alt = alt_array.degrees[i]
                        pass_peak_time = time[i]
            else:
                if in_pass:
                    pass_str = pass_peak_time.utc_datetime().strftime("%Y-%m-%d %H:%M:%S")
                    msg = f"Next visible night pass: {pass_str} UTC (Peak Altitude: {round(peak_alt, 1)}°)"
                    send_email(email, msg)
                    return True, msg
        
        if in_pass and pass_peak_time:
            pass_str = pass_peak_time.utc_datetime().strftime("%Y-%m-%d %H:%M:%S")
            msg = f"Next visible night pass: {pass_str} UTC (Peak Altitude: {round(peak_alt, 1)}°)"
            send_email(email, msg)
            return True, msg

    for day_offset in range(3):
        start_ = t_start.tt + day_offset
        time = ts.tt_jd(start_ + [m / 1440.0 for m in range(0, 1440, 1)])

        topo_iss = (satellite - observer).at(time)
        alt_array, az_array, range_array = topo_iss.altaz()

        
        sun_alt_array = (earth + observer).at(time).observe(eph['sun']).apparent().altaz()[0]

        in_pass = False
        peak_alt = 0
        pass_peak_time = None

        for i in range(len(time)):
            is_visible = alt_array.degrees[i] > 15 and sun_alt_array.degrees[i] < -6
            if is_visible:
                if not in_pass:
                    in_pass = True
                    peak_alt = alt_array.degrees[i]
                    pass_peak_time = time[i]
                else:
                    if alt_array.degrees[i] > peak_alt:
                        peak_alt = alt_array.degrees[i]
                        pass_peak_time = time[i]
            else:
                if in_pass:
                    pass_str = pass_peak_time.utc_datetime().strftime("%Y-%m-%d %H:%M:%S")
                    msg = f"Next visible pass (Night-time): {pass_str} UTC (Peak Altitude: {round(peak_alt, 1)}°)"
                    send_email(email, pass_peak_time, msg)
                    return True, msg

                in_pass = False
                peak_alt = 0
                peak_pass_time = None

    return False, "failed to compute"
