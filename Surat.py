# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 12:44:37 2022

@author: India
"""

import streamlit as st
import geemap
import ee

ee.Initialize()
ee.Authenticate()

#Drainage = ee.Image.loadGeoTIFF('Buffer_Drainage.tif')

Ward = "Surat Ward.geojson" 
CityFile = geemap.geojson_to_ee(Ward, geodesic=False, encoding='utf-8')

st.title('Identifying Potential Mosquito Breeding Sites Using Geospatial Technology')

add_selectbox1 = st.sidebar.selectbox( "Select City",("Surat","Other"))

add_selectbox2 = st.sidebar.selectbox( "Select Year",("2020","2019"))

add_selectbox3 = st.sidebar.select_slider(
     'Select Month', options=['January','February', 'March', 'April' ,'May' ,'June','July' ,'August' ,'September' ,'October','November' ,'December' ])


Map = geemap.Map(center=[21.1702,72.8311], zoom=11)
#Map.add_geojson(Ward, layer_name= "Ward Boundary")
Map.addLayer(CityFile, vis_params={}, name="Ward Boundary", shown=True, opacity=1.0)
Map.to_streamlit(width=600, height=600, responsive=True, scrolling=False)


#Mosq_site = Image.reduceToVectors(scale=30, geometryType = 'point',)
#Map.addLayer(Mosq_site, {}, 'Potential Mosquito Breeding Sites')




#st.download_button("Download", Mosq_site.to_csv(), file_name = "Potential Mosquito Breeding Sites.csv")


with st.expander("About Web App"):
     st.write("""The disordered urban growth that may favour the emergence of the mosquito in cities is a problem of increasing 
              magnitude in tropical part of the world. 
              Vector-Borne Diseases spreads rapidly, a major difficulty in controlling the proliferation of this diseases is associated with 
              identification of the breeding sites. This problem can be solved using Geospatial Technology""")
              
with st.expander("Web App Developer"):
     st.write("***Pranav Pandya***")
     st.write("M.Tech (Geoinformatics) B.Tech (Civil)")
     st.write("Email: pranav.pandya@flame.edu.in")
     st.write("[Linkedin] (https://www.linkedin.com/in/pranavspandya/)")
     st.write("***Chancy Shah***")
     st.write("M.Sc (Geoinformatics) B.Tech (Civil)")
     st.write("Email: shahchancy28@gmail.com")
     st.write("[Website] (https://sites.google.com/view/chancyshah/home) , [Linkedin](https://www.linkedin.com/in/chancy-shah-671787119/)")  
                
   
