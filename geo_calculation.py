###########Part 5 : Geo Data#########################
#Get data - building from CHP
import pandas as pd
import numpy as np
import io
import requests
url="http://www.chp.gov.hk/files/misc/building_list_eng.csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('utf-8')))
df=df.replace("Kowloon city","Kowloon City")
df=df.replace("Central & Western","Central and Western")
df=df.replace("Tsuen wan","Tsuen Wan")
df=df.groupby(["District"]).count()
sample_list = np.arange(1,len(df)+1)
df["ID"]=sample_list

#Get geographical data
import geopandas as gpd
geo_df = gpd.read_file("./HKG_adm/HKG_adm1.shp")

geo_df = geo_df.rename(columns={"NAME_1":"District"})

#Merge
geo_merged = pd.merge(geo_df,df,left_on='ID_1', right_on='ID', how='left')
geo_merged = geo_merged.set_index("ID")

#Convert to geojson
geo_merged = geo_merged.to_crs(epsg=4326) # convert the coordinate reference system to lat/long
geo_merged_json = geo_merged.__geo_interface__ #covert to geoJSON



