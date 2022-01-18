# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 12:44:37 2022

@author: India
"""

import streamlit as st
import geemap
import ee
#import os
#import subprocess
#import sys
#import geopandas as gpd
#import pandas as pd
from geemap import geojson_to_ee, ee_to_geojson
#from ipyleaflet import GeoJSON

#Drainage = ee.Image.loadGeoTIFF('Buffer_Drainage.tif')

CityFile = geemap.geojson_to_ee("Surat Ward.geojson" , geodesic=False, encoding='utf-8')

st.title('Identifying Potential Mosquito Breeding Sites Using Geospatial Technology')

add_selectbox1 = st.sidebar.selectbox( "Select City",("Surat","Other"))

add_selectbox2 = st.sidebar.selectbox( "Select Year",("2022","2021","2020"))

add_selectbox3 = st.sidebar.select_slider(
     'Select Month', options=['January','February', 'March', 'April' ,'May' ,'June','July' ,'August' ,'September' ,'October','November' ,'December' ])

if st.button("Dispaly Potential Mosquito Breeding Sites"):
    Mosquito(1,2022,'Month')
    
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
           
def Mosquito(month,year,describe):
  ###Data Collection
  year=2020
  dataset = ee.ImageCollection("LANDSAT/LE07/C01/T1_32DAY_NDVI").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  z=NDVI = dataset.mosaic().clip(CityFile);
  
  dataset = ee.ImageCollection("LANDSAT/LE07/C01/T1_32DAY_NDWI").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  z=NDWI = dataset.mosaic().clip(CityFile);

  NDBI_data= ee.ImageCollection("LANDSAT/LE07/C01/T2_SR").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  def ndbiComp(NDBI_data):
      return NDBI_data.expression('(swir-nir)/(swir+nir)',
                                  {'swir':NDBI_data.select('B5'),'nir':NDBI_data.select('B4')});
  z=NDBI=NDBI_data.map(ndbiComp).mosaic().clip(CityFile)

  FAPAR=ee.ImageCollection("NOAA/CDR/AVHRR/LAI_FAPAR/V5").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month')).select('FAPAR').mosaic().clip(CityFile);
  # FAPAR_minmax=geemap.image_stats(FAPAR, CityFile, scale=30).getInfo()
  # FAPAR_min,FAPAR_max=FAPAR_minmax['min']['FAPAR'],FAPAR_minmax['max']['FAPAR']
  # FAPAR=FAPARmm=FAPAR.expression('(FAPAR-FAPAR_min)/(FAPAR_max-FAPAR_min)', {'FAPAR':FAPAR,'FAPAR_min':FAPAR_min,"FAPAR_max":FAPAR_max})  

  # Map.addLayer(FAPAR)
  # # FAPAR=FAPAR_data.expression('(B4‐B2)/(B4+B2)*(1.25‐0.025)',{'B4':})

  Precipitation_data=ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  z=Precipitation=Precipitation_data.select('pr').mosaic().clip(CityFile)
  # print(geemap.image_stats(Precipitation, CityFile, scale=30).getInfo(),'prep')

  WindSpeed_data=ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  Wind=z=WindSpeed=WindSpeed_data.select('vs').mosaic().clip(CityFile)
  # Wind_minmax=geemap.image_stats(Wind, CityFile, scale=30).getInfo()
  # Wind_min,Wind_max=Wind_minmax['min']['vs'],Wind_minmax['max']['vs']
  # WinsSpeed=Windmm=Wind.expression('(Wind-Wind_min)/(Wind_max-Wind_min)', {'Wind':Wind,'Wind_min':Wind_min,"Wind_max":Wind_max})  

  Soil_data=ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  z=Soil=Soil_data.select('soil').mosaic().clip(CityFile)
  # print(geemap.image_stats(Soil, CityFile, scale=30).getInfo(),'soil')
  # Soil_minmax=geemap.image_stats(Soil, CityFile, scale=30).getInfo()
  # Soil_min,Soil_max=Soil_minmax['min']['soil'],Soil_minmax['max']['soil']
  # Soilmm=Soil.expression('(Soil-Soil_min)/(Soil_max-Soil_min)', {'Soil':Soil,'Soil_min':Soil_min,"Soil_max":Soil_max})  


  LST_data=ee.ImageCollection("MODIS/006/MOD11A2").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  LST=LST_data.select('LST_Day_1km').mosaic().clip(CityFile)
  LST_minmax=geemap.image_stats(LST, CityFile, scale=30).getInfo()
  LST_min,LST_max=LST_minmax['min']['LST_Day_1km'],LST_minmax['max']['LST_Day_1km']
  LST=LSTmm=LST.expression('(LST-LST_min)/(LST_max-LST_min)', {'LST':LST,'LST_min':LST_min,"LST_max":LST_max})

  x=Humidity_data=ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+3, 'month'));
  z=Humidity=Humidity_data.select('Qair_f_inst').mosaic().clip(CityFile)
  # print(geemap.image_stats(Humidity, CityFile, scale=30).getInfo(),'Humidity')

  ###Map Algebra - Weighted Overlay
  y=completeImage = NDVI.addBands(NDWI).addBands(NDVI).addBands(FAPAR,).addBands(Precipitation).addBands(WindSpeed).addBands(Soil).addBands(Humidity).addBands(LST)
  
  # y=overlay = completeImage.expression('(NDWI)+(NDVI)',#+(NDBI)+(FAPAR)',
  # {'NDVI': completeImage.select("NDVI"), 'NDWI': completeImage.select("NDWI"), 'NDBI': completeImage.select("NDBI"), 'FAPAR': completeImage.select("FAPAR")});
  
  # y=overlay = completeImage.expression('(NDWI-0.1)(NDVI-0.2)(FAPAR-1.1)(NDBI-0.5)(Precipitation-5)(LST-7500)(Humidity-0.05)*(WindSpeed)',
  # {'NDVI': completeImage.select("NDVI"), 'NDWI': completeImage.select("NDWI"), 'NDBI': completeImage.select("NDVI"), 'FAPAR': completeImage.select("FAPAR"), 
  #  'Precipitation': completeImage.select("pr"),    'WindSpeed': completeImage.select("vs"), 'Soil': completeImage.select("soil"), 
  #  'Humidity': completeImage.select("Qair_f_inst"), 'LST': completeImage.select("LST_Day_1km")})

  y=overlay = completeImage.expression('((NDWI-0.1)*(NDVI-0.2)*(WindSpeed))*(LST)*(Soil)*(Humidity-0.05)',#(Precipitation)(Humidity-0.05)+',#',#(FAPAR)(LST)',#+(NDBI-0.5)',
  {'NDVI': completeImage.select("NDVI"), 'NDWI': completeImage.select("NDWI"), 'NDBI': completeImage.select("NDVI"), 'FAPAR': completeImage.select("FAPAR"), 
   'Precipitation': completeImage.select("pr"), 'WindSpeed': completeImage.select("vs"), 'Soil': completeImage.select("soil"), 
   'Humidity': completeImage.select("Qair_f_inst"), 'LST': completeImage.select("LST_Day_1km")})

  y_minmax=geemap.image_stats(y, CityFile, scale=30).getInfo()
  # print(y_minmax)
  y_min,y_max=y_minmax['min']['NDWI'],y_minmax['max']['NDWI']
  y=ymm=y.expression('(y-y_min)/(y_max-y_min)', {'y':y,'y_min':y_min,"y_max":y_max})  
  y_final=geemap.image_stats(y, CityFile, scale=30).getInfo()
  print(y_final['mean']['NDWI'])
  y = y.gt(y_final['mean']['NDWI']*1.1).selfMask()
  
  # print(y.getInfo())#['bands'])
  # print(y.bandNames())
  Map = geemap.Map(center=[21.1702,72.8311], zoom=11)
  Map.addLayer(y,{'palette': ['red', 'black']},'Potential Site') 
  Map.addLayer(CityFile, {}, 'Cities')
  Map.to_streamlit(width=600, height=600, responsive=True, scrolling=False)
