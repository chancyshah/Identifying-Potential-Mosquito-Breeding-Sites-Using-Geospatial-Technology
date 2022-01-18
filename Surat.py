# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 12:44:37 2022

@author: India
"""

import streamlit as st
import geemap
import ee

ee.Initialize()

#Drainage = ee.Image.loadGeoTIFF('https://github.com/chancyshah/Identifying-Potential-Mosquito-Breeding-Sites-Using-Geospatial-Technology/blob/7be95bb2b7a2aa0afebafca1a8e8f7cdcc764cc2/Buffer_Drainage.tif')

Month = ['January','February', 'March', 'April' ,'May' ,'June','July' ,'August' ,'September' ,'October','November' ,'December' ]

st.title('Identifying Potential Mosquito Breeding Sites Using Geospatial Technology')

add_selectbox1 = st.sidebar.selectbox( "Select City",("Surat"," "))

add_selectbox2 = st.sidebar.selectbox( "Select Year",("2020", " "))
year = int(add_selectbox2)
add_selectbox3 = st.sidebar.select_slider(
     'Select Month', options= Month)
index = Month.index(add_selectbox3)
index = index + 1

if st.button("Dispaly Potential Mosquito Breeding Sites"):
    Mosquito(index,year,'Map')
else:
    Map = geemap.Map(center=[21.1702,72.8311], zoom=11)
    #Map.addLayer(CityFile, {}, 'Cities')
    Map.to_streamlit(width=600, height=600, responsive=True, scrolling=False)
    
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(	255,235,205);
}</style>""", unsafe_allow_html=True)


with st.expander("About Web App"):
     st.write("""In recent years, vector-borne diseases (VBD) have emerged as a serious public health problem in most of the countries including India. India aims to develop 100 smart cities, and therefore planning the health infrastructure while limiting human-to-human interactions, preserving vulnerable populations, and managing infrastructure while honing capacity to leverage smart technology for healing masses, is the cornerstone of a smart city.
              The disordered urban growth that may favor the emergence of the mosquito in cities is a problem of increasing magnitude. 
              Vector borne diseases constitute a major public health problem in the list of communicable diseases. The most important are malaria, dengue fever, chikungunya fever. Geospatail Technology is a powerful tool to analyse the distribution of mosquitoes and their relationship to different environmental factors, and can substantially improve our ability to quantify the impacts of demographic, climatic and ecological changes in vector distribution.""")
              
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
  
  CityFile = geemap.geojson_to_ee("https://github.com/chancyshah/Identifying-Potential-Mosquito-Breeding-Sites-Using-Geospatial-Technology/blob/7be95bb2b7a2aa0afebafca1a8e8f7cdcc764cc2/Surat%20Ward.geojson" , geodesic=False, encoding='utf-8')
  
  dataset = ee.ImageCollection("LANDSAT/LE07/C01/T1_32DAY_NDVI").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  NDVI = dataset.mosaic().clip(CityFile);
  
  dataset = ee.ImageCollection("LANDSAT/LE07/C01/T1_32DAY_NDWI").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  NDWI = dataset.mosaic().clip(CityFile);

  NDBI_data= ee.ImageCollection("LANDSAT/LE07/C01/T2_SR").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  def ndbiComp(NDBI_data):
      return NDBI_data.expression('(swir-nir)/(swir+nir)',
                                  {'swir':NDBI_data.select('B5'),'nir':NDBI_data.select('B4')});
  NDBI_data.map(ndbiComp).mosaic().clip(CityFile)

  FAPAR=ee.ImageCollection("NOAA/CDR/AVHRR/LAI_FAPAR/V5").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month')).select('FAPAR').mosaic().clip(CityFile);
  # FAPAR_minmax=geemap.image_stats(FAPAR, CityFile, scale=30).getInfo()
  # FAPAR_min,FAPAR_max=FAPAR_minmax['min']['FAPAR'],FAPAR_minmax['max']['FAPAR']
  # FAPAR=FAPARmm=FAPAR.expression('(FAPAR-FAPAR_min)/(FAPAR_max-FAPAR_min)', {'FAPAR':FAPAR,'FAPAR_min':FAPAR_min,"FAPAR_max":FAPAR_max})  

  # Map.addLayer(FAPAR)
  # # FAPAR=FAPAR_data.expression('(B4‐B2)/(B4+B2)*(1.25‐0.025)',{'B4':})

  Precipitation_data=ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  Precipitation=Precipitation_data.select('pr').mosaic().clip(CityFile)
  # print(geemap.image_stats(Precipitation, CityFile, scale=30).getInfo(),'prep')

  WindSpeed_data=ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  WindSpeed=WindSpeed_data.select('vs').mosaic().clip(CityFile)
  # Wind_minmax=geemap.image_stats(Wind, CityFile, scale=30).getInfo()
  # Wind_min,Wind_max=Wind_minmax['min']['vs'],Wind_minmax['max']['vs']
  # WinsSpeed=Windmm=Wind.expression('(Wind-Wind_min)/(Wind_max-Wind_min)', {'Wind':Wind,'Wind_min':Wind_min,"Wind_max":Wind_max})  

  Soil_data=ee.ImageCollection("IDAHO_EPSCOR/TERRACLIMATE").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  Soil=Soil_data.select('soil').mosaic().clip(CityFile)
  # print(geemap.image_stats(Soil, CityFile, scale=30).getInfo(),'soil')
  # Soil_minmax=geemap.image_stats(Soil, CityFile, scale=30).getInfo()
  # Soil_min,Soil_max=Soil_minmax['min']['soil'],Soil_minmax['max']['soil']
  # Soilmm=Soil.expression('(Soil-Soil_min)/(Soil_max-Soil_min)', {'Soil':Soil,'Soil_min':Soil_min,"Soil_max":Soil_max})  

  LST_data=ee.ImageCollection("MODIS/006/MOD11A2").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+1, 'month'));
  LST=LST_data.select('LST_Day_1km').mosaic().clip(CityFile)
  LST_minmax=geemap.image_stats(LST, CityFile, scale=30).getInfo()
  LST_min,LST_max=LST_minmax['min']['LST_Day_1km'],LST_minmax['max']['LST_Day_1km']
  LST=LST.expression('(LST-LST_min)/(LST_max-LST_min)', {'LST':LST,'LST_min':LST_min,"LST_max":LST_max})

  Humidity_data=ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H").filterBounds(CityFile).filter(ee.Filter.calendarRange (year,year, 'year')).filter(ee.Filter.calendarRange (month,month+3, 'month'));
  Humidity=Humidity_data.select('Qair_f_inst').mosaic().clip(CityFile)
  # print(geemap.image_stats(Humidity, CityFile, scale=30).getInfo(),'Humidity')

  ###Map Algebra - Weighted Overlay
  y=completeImage = NDVI.addBands(NDWI).addBands(NDVI).addBands(FAPAR,).addBands(Precipitation).addBands(WindSpeed).addBands(Soil).addBands(Humidity).addBands(LST)
  
  # y=overlay = completeImage.expression('(NDWI)+(NDVI)',#+(NDBI)+(FAPAR)',
  # {'NDVI': completeImage.select("NDVI"), 'NDWI': completeImage.select("NDWI"), 'NDBI': completeImage.select("NDBI"), 'FAPAR': completeImage.select("FAPAR")});
  
  # y=overlay = completeImage.expression('(NDWI-0.1)(NDVI-0.2)(FAPAR-1.1)(NDBI-0.5)(Precipitation-5)(LST-7500)(Humidity-0.05)*(WindSpeed)',
  # {'NDVI': completeImage.select("NDVI"), 'NDWI': completeImage.select("NDWI"), 'NDBI': completeImage.select("NDVI"), 'FAPAR': completeImage.select("FAPAR"), 
  #  'Precipitation': completeImage.select("pr"),    'WindSpeed': completeImage.select("vs"), 'Soil': completeImage.select("soil"), 
  #  'Humidity': completeImage.select("Qair_f_inst"), 'LST': completeImage.select("LST_Day_1km")})

  y= completeImage.expression('((NDWI-0.1)*(NDVI-0.2)*(WindSpeed))*(LST)*(Soil)*(Humidity-0.05)',#(Precipitation)(Humidity-0.05)+',#',#(FAPAR)(LST)',#+(NDBI-0.5)',
  {'NDVI': completeImage.select("NDVI"), 'NDWI': completeImage.select("NDWI"), 'NDBI': completeImage.select("NDVI"), 'FAPAR': completeImage.select("FAPAR"), 
   'Precipitation': completeImage.select("pr"), 'WindSpeed': completeImage.select("vs"), 'Soil': completeImage.select("soil"), 
   'Humidity': completeImage.select("Qair_f_inst"), 'LST': completeImage.select("LST_Day_1km")})

  y_minmax=geemap.image_stats(y, CityFile, scale=30).getInfo()
  # print(y_minmax)
  y_min,y_max=y_minmax['min']['NDWI'],y_minmax['max']['NDWI']
  y=y.expression('(y-y_min)/(y_max-y_min)', {'y':y,'y_min':y_min,"y_max":y_max})  
  y_final=geemap.image_stats(y, CityFile, scale=30).getInfo()
  print(y_final['mean']['NDWI'])
  y = y.gt(y_final['mean']['NDWI']*1.1).selfMask()
  
  # print(y.getInfo())#['bands'])
  # print(y.bandNames())
  Map = geemap.Map(center=[21.1702,72.8311], zoom=11)
  Map.addLayer(y,{'palette': ['red']},'Potential Site')
  Map.addLayer(CityFile, {'color': 'black', 'fillColor': '00000000'}, 'Ward Boundary', opacity = 0.4)
  Map.to_streamlit(width=600, height=600, responsive=True, scrolling=False)
       
