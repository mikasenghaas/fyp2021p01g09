import random
import numpy as np
import folium                                         
from folium.plugins import HeatMap, MarkerCluster

def plot_marker(_map, _location, _popup, _color, _fill=True):
    """
    For a given map, the function plots a folium.CircleMaker at the specified location, with specified popup information and a specified color.

    Parameters:
        _map        : folium.Map object
        _location   : tuple (A tuple representing the 'Latitude' and 'Longitude')
        _popup      : list (List of information that should be given in the popup)
        _color      : str (Color Code)
        _fill       : boolean ('True' if the circle should be filled with color, else 'False')
    """
    folium.CircleMarker(
            radius=5,
            location=[_location[0], _location[1]],
            tooltip='Check this Accident',
            popup="<br>".join(_popup),
            color=_color,
            fill=_fill).add_to(_map)

def random_color():
    """
    Function to generate a random color.
    """
    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    return '#'+ hex_number[2:]

def map_accidents(data, summary, centroid, colors='random', heat_map=True, marker_cluster=True, focus='Accident_Severity'):
    """
    Function to generate a `folium.Map` that maps all accidents (color coded for a specified variable `focus`) on a map around the centroid. Depending on the paramters `heat_map` and `marker_cluster`, the map has addional layers that can be hidden and shown through a layer control menu. Through this menu, the appearance of the map can also be adjusted interactively.

    Parameters:
        data            : pd.DataFrame
        summary         : dict (Central data structure)
        centroid        : list (containing [Latitude, Longitude] that indicate the starting position of the map)
        heat_map        : boolean (Displays Layer 'Heat Map' if True, else not)
        marker_cluster  : boolean (Clusters Accidents automatically if True, else not)
        focus           : str (represent the name of the column in 'data' for which the color code should apply)

    Return:
        _map            : folium.Map
    """
    # general map settings
    _map = folium.Map(location=centroid, initial_zoom = 5)
    folium.TileLayer('openstreetmap').add_to(_map)
    folium.TileLayer('Stamen Terrain').add_to(_map)
    folium.TileLayer('Stamen Toner').add_to(_map)
    folium.TileLayer('Stamen Water Color').add_to(_map)
    folium.TileLayer('cartodbpositron').add_to(_map)
    folium.TileLayer('cartodbdark_matter').add_to(_map)

    # plotting accidents
    uniques = np.unique(data[focus])
    no_uniques = len(uniques)
    
    if colors=='random':
        colors = [random_color() for _ in range(no_uniques)]
    
    if marker_cluster:
        marker_cluster = MarkerCluster().add_to(folium.FeatureGroup(name='Clusters').add_to(_map))

        for i in range(data.shape[0]):
            labels = []
            for x in range(data.shape[1]):
                if x == list(data).index(focus):
                    col_name = f"<strong>{list(data)[x]}</strong>"
                else: col_name = list(data)[x]
                try: mapping = summary[x]['Map'][data.iloc[i,x]]
                except: mapping = data.iloc[i,x]
                labels.append(": ".join([col_name, str(mapping)]))

            for j in range(no_uniques):
                if data[focus].iloc[i] == uniques[j]:
                    plot_marker(
                        marker_cluster, 
                        _location=(data['Latitude'].iloc[i], data['Longitude'].iloc[i]), 
                        _popup = labels,
                        _color=colors[j], 
                        _fill=False)

    else:
        accidents = folium.FeatureGroup(name='Accidents').add_to(_map)
        for i in range(data.shape[0]):
            labels = []
            for x in range(data.shape[1]):
                if x == list(data).index(focus):
                    col_name = f"<strong>{list(data)[x]}</strong>"
                else: col_name = list(data)[x]
                try: mapping = summary[x]['Map'][data.iloc[i,x]]
                except: mapping = data.iloc[i,x]
                labels.append(": ".join([col_name, str(mapping)]))

            for j in range(no_uniques):
                if data[focus].iloc[i] == uniques[j]:
                    plot_marker(
                        accidents, 
                        _location=(data['Latitude'].iloc[i], data['Longitude'].iloc[i]), 
                        _popup = labels,
                        _color=colors[j], 
                        _fill=False)

    if heat_map:
        latlons = np.array(data[['Latitude', 'Longitude']])

        # plot heatmap to map
        HeatMap(latlons).add_to(folium.FeatureGroup(name='Heat Map').add_to(_map))
    
    folium.LayerControl().add_to(_map)

    return _map