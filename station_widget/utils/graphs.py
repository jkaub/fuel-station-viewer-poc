import plotly.graph_objects as go
import numpy as np

from station_widget.consts import TOKEN

def points_on_circle(lat, lon, radius, num_points):
    '''This function return a list of coordinates as lat/lon of size num_points forming a circle of a certain radius centered on a 
       a point of coordinate lat,lon
    '''
    points = []
    R = 6371
    for i in range(num_points):
        bearing = 360/num_points*i
        lat2 = np.arcsin(np.sin(np.radians(lat))*np.cos(radius/R) +
                    np.cos(np.radians(lat))*np.sin(radius/R)*np.cos(np.radians(bearing)))
        lon2 = np.radians(lon) + np.arctan2(np.sin(np.radians(bearing))*np.sin(radius/R)*np.cos(np.radians(lat)),
                                   np.cos(radius/R)-np.sin(np.radians(lat))*np.sin(lat2))
        points.append((np.degrees(lat2), np.degrees(lon2)))
    points = np.array(points)
    points = np.vstack([points, points[0]])
    
    return points[:,0], points[:,1] 

def init_chart(sub_df, init_lat, init_lon, distance):

    stations = go.Scattermapbox(
        lat= sub_df.latitude,
        lon= sub_df.longitude,
        mode='markers',
        marker=dict(
            size=14,
            color='white',
            symbol = 'fuel',
        ),
        text=sub_df.valeur+' €/L',
        showlegend = False,
    )

    prices = go.Scattermapbox(
        lat= sub_df.latitude,
        lon= sub_df.longitude,
        mode='markers',
        marker=dict(
            size=40,
            color=sub_df.valeur.astype(float),
            colorscale ='PiYG_r',
        ),
        opacity = 0.7,
        text=sub_df.valeur+' €/L',
        showlegend = False,
    )

    solid_price_border = go.Scattermapbox(
        lat= sub_df.latitude,
        lon= sub_df.longitude,
        mode='markers',
        marker=dict(
            size=45,
            color='black',
        ),
        opacity = 0.8,
        text=sub_df.valeur+' €/L',
        showlegend = False,
    )

    lats, longs = points_on_circle(init_lat,init_lon, distance, 50)
    research_zone = go.Scattermapbox(
        lat= lats,
        lon= longs,
        mode='lines',
        fill='toself',
        fillcolor = "rgba(1,1,1,0.2)",
        marker=dict(
            size=45,
            color='black',
        ),
        opacity = 0.8,
        showlegend = False,
    )

    user_position = go.Scattermapbox(
        lat= [init_lat],
        lon= [init_lon],
        mode='markers',
        marker=dict(
            size=10,
            color='red',
        ),
        opacity = 1,
        showlegend = False,
    )

    #create the layout
    layout = go.Layout(
        height = 600,
        width = 600,
        mapbox=dict(
            accesstoken=TOKEN,
            style='streets',
            center=dict(
                lat=init_lat,
                lon=init_lon
            ),
            zoom=11,
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return go.FigureWidget(data=[research_zone, solid_price_border,prices, stations, user_position], layout=layout)