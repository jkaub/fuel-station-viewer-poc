import numpy as np
from station_widget.consts import R

def filter_dataset_from_source_point(stations_df, lat_point, lon_point, distance = 20):
    
    return stations_df.loc[haversine_distance(stations_df.latitude, stations_df.longitude, lat_point, lon_point)<=distance]
    
def filter_dataset_by_gas_type(sub_station_df, gas_types_df, gas_type):
    
    joined_df = sub_station_df.set_index("station_id") \
          .join(
              gas_types_df.set_index("station_id"), how = 'left'
          )
    return joined_df.loc[joined_df.nom==gas_type]
  
def haversine_distance(lat1, lon1, lat2, lon2):
    '''Calculate the distance between two points (lat1,lon1) and (lat2, lon2) in km'''
    
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = R * c
    return distance