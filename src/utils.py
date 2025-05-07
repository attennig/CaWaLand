
import src.tokens as tokens
import os
from datetime import datetime, timedelta
import json, sys
import requests
import numpy as np

str_to_date = lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')
date_to_str = lambda d: d.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
seconds_to_timedelta = lambda s: timedelta(seconds=s)

def get_timestamps(init_time: datetime, final_time: datetime, step_duration: timedelta) -> list[datetime]:
    timestamps = []
    t = init_time
    while t <= final_time:
        timestamps.append(t)
        t += step_duration
    return timestamps

def json_default(value):
    if isinstance(value, datetime):
        return date_to_str(value)
    else:
        return value.__dict__
    
"""
    Functions to process the weather data and compute the wet bulb temperature
"""

# REF: https://www.weather.gov/media/epz/wxcalc/vaporPressure.pdf
# REF: https://web.archive.org/web/20200212215746im_/https://www.vaisala.com/en/system/files?file=documents/Humidity_Conversion_Formulas_B210973EN.pdf
vapor_pressure = lambda T: 10**(7.5*T/(237.3+T)) # 6.11 *
relative_humidity = lambda T, T_d: 100 * vapor_pressure(T_d) / vapor_pressure(T) 
# REF: https://journals.ametsoc.org/view/journals/apme/50/11/jamc-d-11-0143.1.xml
wetbulb_temperature = lambda T, RH: T * np.arctan(0.151977 * (RH + 8.313659)**0.5) + np.arctan(T + RH) - np.arctan(RH - 1.676331) + 0.00391838 * (RH)**(3/2) * np.arctan(0.023101 * RH) - 4.686035
C2F = lambda num: (num*9/5)+32 # celsius_to_farhenheit
wue = lambda cycle, tw: max(.0,cycle/(cycle-1)*(6e-5* C2F(tw)**3 - 0.01 * C2F(tw)**2 + 0.61 * C2F(tw) - 10.4))


def wetbulb_temperature_processing(
        city: str, state: str,
        date_time_start: datetime , 
        date_time_finish: datetime,
        path: str,
        include: str = "hours"
        ):
    
    
    date_start = str(date_time_start.date())
    date_finish = str(date_time_finish.date())
    
    data = get_weather(city, state, date_start, date_finish, path, include = include)
    #data = load(f"{path}/{date_to_str(date_time_start)}-{date_to_str(date_time_finish)}/", city)
    wetbulb_temperature_dict = {}
    for day in data:
        day_str = day["datetime"]
        for hour in day["hours"]:
            hour_str = hour["datetime"]
            date_time = datetime.strptime(f'{day_str}T{hour_str}', '%Y-%m-%dT%H:%M:%S')
            if date_time < date_time_start or date_time > date_time_finish:
                continue
            #print(date_to_str(date_time))
            wetbulb_temperature_dict[date_time] = wetbulb_temperature(float(hour["temp"]), relative_humidity(float(hour["temp"]), float(hour["dew"])))
    return wetbulb_temperature_dict




"""
    API functions to get the historical energy mix for reginal grids and weather data for cities
"""
# electricity maps API to get the historical energy mix for 

def get_zones():
    url = "https://api.electricitymap.org/v3/zones"
    response = requests.get(url)
    data = response.json()
    return data

def get_feature_last24h(feature: str, zone_key: str):
    url = "https://api.electricitymap.org/v3/{}/history?zone={}".format(feature,zone_key)
    print(url)
    headers = {
        "auth-token": tokens.ELECTRICITYMAPS_API_TOKEN
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        #print("Carbon Intensity Data:", data)
        return data
    else:
        print("Error:", response.status_code, response.text)
    return None

def get_weather(city: str, state: str, date1: str, date2: str, path: str, include = "hours") -> dict:
    import urllib.request
    """
    API documentation: https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/
    Metric units:
    Weather Variable                        Measurement Unit
    Temperature, Heat Index & Wind Chill	Degrees Celcius
    Precipitation	                        Millimeters
    Snow	                                Centimeters
    Wind & Wind Gust	                    Kilometers Per Hour
    Visibility	                            Kilometers
    Pressure	                            Millibars (Hectopascals)
    Solar Radiation	                        W/m2
    Solar Energy	                        MJ/m2
    Soil Moisture	                        Millimeters
    """   
    city = city.replace(" ", "%20")  
    format = "json"
    query = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{date1}/{date2}?unitGroup=metric&include={include}&key={tokens.VISUALCROSSING_API_TOKEN}&contentType={format}&timezone=Z"
    #print(query)
    #if os.path.isfile(f'{path}{city}_weather.json'):
    #   return load(path, city)
    # else
    try:
        #sys.exit() 
        ResultBytes = urllib.request.urlopen(query)
        dt = json.load(ResultBytes)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f'{path}api.json', 'w', newline='') as f:
            f.write(json.dumps(dt))
            
    except urllib.error.HTTPError  as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except  urllib.error.URLError as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code,ErrorInfo)
        sys.exit()
    
    return dt["days"]  

"""def load(path, city):
    city = city.replace(" ", "%20")
    with open(f'{path}api.json', 'r') as f:
        data = json.load(f)
    return data["days"]"""




def average_power(provider: str, min_watts: float = None, max_watts: float = None, util: float = None):
    """
    Compute the expected energy consumption using Cloud Carbon Footprint methodology
    source: https://www.cloudcarbonfootprint.org/docs/methodology/
    """
    Util = 0.5
    MinWatts = {
        "aws": 0.74,
        "gcp": 0.71,
        "azure": 0.78,
    }
    MaxWatts = {
        "aws": 3.5,
        "gcp": 4.26,
        "azure": 3.76,
    }
    if min_watts is not None and max_watts is not None and util is not None:
        AverageWatts = min_watts + util * (max_watts - min_watts)
    else: 
        AverageWatts = MinWatts[provider] + Util * (MaxWatts[provider] - MinWatts[provider])
    return AverageWatts, 0.357 # Watt, Watt/GB


expected_runtime = {
    ('join', 'c3.2xlarge') : lambda n_nodes, input_size_bytes: -0.0*n_nodes -9.074884096169962e-09 * input_size_bytes + 236.2804976276901,
    ('join', 'c3.large') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 8.931803599421581e-08 * input_size_bytes + 144.35414351149973,
    ('join', 'c3.xlarge') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 1.806255509473032e-07 * input_size_bytes -398.2552213798336,
    ('join', 'c4.2xlarge') : lambda n_nodes, input_size_bytes: -0.1338760427523339*n_nodes + 1.2429253881864068e-09 * input_size_bytes + 153.2165269752729,
    ('join', 'c4.large') : lambda n_nodes, input_size_bytes: -14.18261277602865*n_nodes + 3.3373340014750782e-09 * input_size_bytes + 447.6383047962939,
    ('join', 'c4.xlarge') : lambda n_nodes, input_size_bytes: -11.273199127053193*n_nodes + 2.073317152603518e-09 * input_size_bytes + 258.3312747029825,
    ('join', 'm3.2xlarge') : lambda n_nodes, input_size_bytes: -0.0*n_nodes -1.2188316199358183e-07 * input_size_bytes + 668.6609751211529,
    ('join', 'm3.large') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 1.1503628800454146e-06 * input_size_bytes -3846.2188582258873,
    ('join', 'm3.xlarge') : lambda n_nodes, input_size_bytes: -0.0*n_nodes -1.6923995020229093e-06 * input_size_bytes + 6732.940459249714,
    ('join', 'm4.2xlarge') : lambda n_nodes, input_size_bytes: -1.1433053053522135*n_nodes + 1.3856262988900832e-09 * input_size_bytes + 197.2323423321151,
    ('join', 'm4.large') : lambda n_nodes, input_size_bytes: -14.755494973062905*n_nodes + 3.514181457030085e-09 * input_size_bytes + 525.3325040758316,
    ('join', 'm4.xlarge') : lambda n_nodes, input_size_bytes: -11.728196012829923*n_nodes + 2.2197496861640764e-09 * input_size_bytes + 301.5746368620984,
    ('join', 'n2-highcpu-8') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 2.994212276813535e-09 * input_size_bytes -3.9302106328860305,
    ('join', 'n2-standard-4') : lambda n_nodes, input_size_bytes: -64.616875*n_nodes + 6.330969503319729e-09 * input_size_bytes + 712.5457672735639,
    ('join', 'n2_highcpu-32') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 1.9749135318406577e-08 * input_size_bytes -1334.0808713190786,
    ('join', 'n2_highcpu-8') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 1.053073967806903e-08 * input_size_bytes -500.03840455565296,
    ('join', 'n2_highmem-4') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 1.4451831953956601e-08 * input_size_bytes -102.41570100223726,
    ('join', 'n2_highmem-8') : lambda n_nodes, input_size_bytes: -279.9075*n_nodes + 1.2888704732650426e-08 * input_size_bytes + 954.3012075449506,
    ('join', 'n2_standard-8') : lambda n_nodes, input_size_bytes: -142.32875*n_nodes + 6.729680839198426e-09 * input_size_bytes + 723.2231073058314,
    ('join', 'r3.2xlarge') : lambda n_nodes, input_size_bytes: -0.0*n_nodes -7.391066498940179e-07 * input_size_bytes + 2995.7281456126134,
    ('join', 'r3.large') : lambda n_nodes, input_size_bytes: -0.0*n_nodes -5.47194195443932e-07 * input_size_bytes + 2562.7182293922115,
    ('join', 'r3.xlarge') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 8.194942643914767e-07 * input_size_bytes -2812.8322802820912,
    ('join', 'r4.2xlarge') : lambda n_nodes, input_size_bytes: -6.218009211413162*n_nodes + 1.4555527464012852e-09 * input_size_bytes + 199.77357405222313,
    ('join', 'r4.large') : lambda n_nodes, input_size_bytes: -18.0552873473685*n_nodes + 4.010311365153493e-09 * input_size_bytes + 491.1611835944843,
    ('join', 'r4.xlarge') : lambda n_nodes, input_size_bytes: -14.95894966949446*n_nodes + 2.4690988070706585e-09 * input_size_bytes + 298.8286798978198,
    ('sort', 'c3.2xlarge') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 1.4510870227890462e-08 * input_size_bytes + 263.6758791232747,
    ('sort', 'c3.large') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 3.139982267166793e-08 * input_size_bytes + 485.06285855822216,
    ('sort', 'c3.xlarge') : lambda n_nodes, input_size_bytes: -0.0*n_nodes -3.99869647693203e-09 * input_size_bytes + 733.2165759172774,
    ('sort', 'c4.2xlarge') : lambda n_nodes, input_size_bytes: -0.0*n_nodes -1.867826856565889e-08 * input_size_bytes + 605.7384385739682,
    ('sort', 'c4.large') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 1.4468703378034767e-08 * input_size_bytes + 764.5257067021315,
    ('sort', 'c4.xlarge') : lambda n_nodes, input_size_bytes: -0.0*n_nodes -2.0783815624023836e-08 * input_size_bytes + 804.7268363212244,
    ('sort', 'm3.2xlarge') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 5.025198244675414e-10 * input_size_bytes + 320.36114150158386,
    ('sort', 'm3.large') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 3.959548325448151e-08 * input_size_bytes + 472.48838352610244,
    ('sort', 'm3.xlarge') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 1.8281307074219054e-08 * input_size_bytes + 308.3804970242357,
    ('sort', 'm4.2xlarge') : lambda n_nodes, input_size_bytes: -0.0*n_nodes -5.630338927258201e-09 * input_size_bytes + 475.3667331052457,
    ('sort', 'm4.large') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 3.554006233785121e-08 * input_size_bytes + 511.0365398374372,
    ('sort', 'm4.xlarge') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 3.3105609156961923e-09 * input_size_bytes + 454.74497044654396,
    ('sort', 'n2-highcpu-8') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 4.7100990099009886e-09 * input_size_bytes -140.31999999999982,
    ('sort', 'n2-standard-4') : lambda n_nodes, input_size_bytes: -32.965625*n_nodes + 3.413811881188119e-09 * input_size_bytes + 294.13250000000005,
    ('sort', 'n2_highcpu-32') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 4.2097722772277216e-08 * input_size_bytes -2956.3099999999986,
    ('sort', 'n2_highcpu-8') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 1.3628910891089105e-08 * input_size_bytes -669.9099999999992,
    ('sort', 'n2_highmem-4') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 9.983465346534649e-09 * input_size_bytes -496.0399999999993,
    ('sort', 'n2_highmem-8') : lambda n_nodes, input_size_bytes: -366.1*n_nodes + 1.8777821782178222e-08 * input_size_bytes + 316.5699999999995,
    ('sort', 'n2_standard-8') : lambda n_nodes, input_size_bytes: -190.82375*n_nodes + 1.0790247524752475e-08 * input_size_bytes + 368.1524999999999,
    ('sort', 'r3.2xlarge') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 2.022506363533817e-08 * input_size_bytes + 147.0102908550282,
    ('sort', 'r3.large') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 7.643873256249153e-08 * input_size_bytes + 79.84888670370856,
    ('sort', 'r3.xlarge') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 3.39367103609883e-08 * input_size_bytes + 114.0166530019471,
    ('sort', 'r4.2xlarge') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 3.885049091009159e-08 * input_size_bytes -23.928914647384545,
    ('sort', 'r4.large') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 5.1505470875736056e-08 * input_size_bytes + 323.3586333036722,
    ('sort', 'r4.xlarge') : lambda n_nodes, input_size_bytes: 0.0*n_nodes + 3.652578706670375e-08 * input_size_bytes + 94.81090070507605
}




def save_output(out_path, footprints, algo_name):

    json_out_dict = {
        str(key): [] for key in footprints.keys()
    }
    for dc, list_traces_fp in footprints.items():
        json_out_dict[str(dc)] = [
            {
                date_to_str(t): values_fp 
                for t, values_fp in trace_fp.items()
            }
            for trace_fp in list_traces_fp
            ]
    

    with open(f"{out_path}/{algo_name}.json", "w") as f:
        json.dump(json_out_dict, f, indent=4)


def save_output_1h(out_path, footprints, algo_name):

    json_out_dict = {
        str(key): [] for key in footprints.keys()
    }
    for dc, footprint_serie in footprints.items():
        json_out_dict[str(dc)] = {
            date_to_str(t): values_fp 
            for t, values_fp in footprint_serie.items()
        }
    

    with open(f"{out_path}/{algo_name}.json", "w") as f:
        json.dump(json_out_dict, f, indent=4)