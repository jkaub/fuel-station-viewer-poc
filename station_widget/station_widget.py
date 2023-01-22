import pandas as pd

from ipywidgets import Text, Dropdown, VBox, HBox
from IPython.display import display

from station_widget.utils.data_filtering import filter_dataset_from_source_point, filter_dataset_by_gas_type
from station_widget.utils.data_parsing import load_from_url_in_memory, parse_xml
from station_widget.utils.graphs import init_chart
from station_widget.consts import INIT_POST_CODE, INIT_FUEL, INIT_DIST, CITY_PATH, URL

class StationWidget:
    
    def __init__(self):
        z = load_from_url_in_memory(URL)
        self._stations_df , self._gas_types_df = parse_xml(z)
        self._cities_df = pd.read_csv(CITY_PATH, index_col=0, dtype={"postal_code":str})
        self._distance = INIT_DIST
        self._fuel = INIT_FUEL
        self._post_code = INIT_POST_CODE
        self._filter_by_postal_code(self._post_code, self._distance, self._fuel)
        self._init_layout()
        
    def _update_fig(self):
        new_fig = init_chart(self._sub_station_with_prices, self._lat_pos, self._lon_pos, self._distance)
        with self._fig.batch_update():
            #Update all the lat longs for our 5 traces
            for k in range(5):
                self._fig.data[k].lat = new_fig.data[k].lat
                self._fig.data[k].lon = new_fig.data[k].lon

            #Update the color markers of the prices
            self._fig.data[2].marker = new_fig.data[2].marker
            
            #Update the overlayed text
            for k in [1,2,3]:
                self._fig.data[k].text = new_fig.data[k].text

            #Update new center of the map
            center = {"lat":self._lat_pos, "lon":self._lon_pos}
            self._fig.layout.mapbox.center = center     
        
    def _filter_by_postal_code(self, postal_code, distance_km, gas_type):

        sub_cities = self._cities_df.loc[self._cities_df.postal_code==postal_code]

        #If the postal code is not value, raise a value error
        if len(sub_cities)==0:
            return 0

        self._lat_pos, self._lon_pos = sub_cities.iloc[0][["lat","lon"]]
        sub_station_df = filter_dataset_from_source_point(self._stations_df, self._lat_pos, self._lon_pos, distance_km)
       
        self._sub_station_with_prices = filter_dataset_by_gas_type(sub_station_df, self._gas_types_df, gas_type)[["latitude" ,"longitude" ,"cp" ,"city","nom", "valeur"]]
        return 1
    
    def _init_layout(self):
        '''This function initiate the widget layout and the different callbacks'''
        #Select fuel dropdown
        fuel_type_dropdown = Dropdown(options  = self._gas_types_df.nom.unique(), 
                                      value = INIT_FUEL, 
                                      description = "Fuel type")
        fuel_type_dropdown.observe(self._on_fuel_change, names='value')
        
        #Select max distance dropdown
        distance_dropdrown = Dropdown(options  = [*range(1,30)], 
                                      value = INIT_DIST, 
                                      description = "distance (km)")
        distance_dropdrown.observe(self._on_distance, names='value')
        
        #Select postal code from text
        postal_code_text= Text(placeholder="Postal Code")
        postal_code_text.observe(self._on_change_text, names='value')
        
        #Create the figure based on initial value
        self._fig = init_chart(self._sub_station_with_prices, 
                               self._lat_pos, 
                               self._lon_pos, 
                               self._distance)
        
        #Create the widget 
        self._widget = VBox([postal_code_text,
                            HBox([fuel_type_dropdown, 
                                  distance_dropdrown]), 
                            self._fig])
        
    def _on_change_text(self,change):
        
        new_pc = str(change["new"])
        done = self._filter_by_postal_code(new_pc, self._distance, self._fuel)
        if done:
            self._post_code = new_pc
            self._update_fig()

    def _on_fuel_change(self, change):
        self._fuel = change["new"]
        done = self._filter_by_postal_code(self._post_code, self._distance, self._fuel)
        if done:
            self._update_fig()    

    def _on_distance(self, change):
        self._distance = change["new"]
        done = self._filter_by_postal_code(self._post_code, self._distance, self._fuel)
        if done:
            self._update_fig()
            
    def display(self):
        display(self._widget)