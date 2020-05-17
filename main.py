import requests
import json
import folium
import os


res = requests.get('https://api.thevirustracker.com/free-api?countryTotals=ALL')
covid_current = res.json()


fob=open('data/countriesLatLongCircle.json','r+')
data=fob.read()
jsData=json.loads(data)


covidData={}
covidChoroplethData=[]
for j in range(1,len(covid_current['countryitems'][0])):
    covidChoroplethData.append([covid_current['countryitems'][0]['{}'.format(j)]['title'],covid_current['countryitems'][0]['{}'.format(j)]['total_cases']])
    covidData[covid_current['countryitems'][0]['{}'.format(j)]['title']]=covid_current['countryitems'][0]['{}'.format(j)]




folium_map = folium.Map(location=[19.01441, 72.8479385], zoom_start=5, tiles="openstreetmap")

countriesBorderJson = os.path.join('data', 'countriesBorderJson.json')

folium.Choropleth(
    geo_data = countriesBorderJson,
    name = 'Corona Data',
    data=covidChoroplethData,
    columns = ['Region' , 'Infected'],
    key_on = 'feature.properties.name',
    fill_color = 'OrRd',
    fill_opacity = 0.51,
    line_opacity = 0.51,
    nan_fill_color = '#f2efe9',   #for countries which could not be found in data
    line_color = 'white',
    legend_name='Infected Cases',
    highlight=True,
    #smooth_factor=1
).add_to(folium_map)


rangeList=[999,9999,39999,79999,199999,999999,3999999,9999999]
colorDict={999:'#E1FF2F',9999:'#F9A602',39999:'#FD6A02',79999:'#FD6A02',199999:'#FF2400',999999:'#D30000',3999999:'#960019',9999999:'#420D09'}

for key,value in covidData.items():
    country=key
    totalCases=value['total_cases']
    data=str(value).replace(',','<br>').replace("'",'').replace('_',' ').replace('{','').replace('}','')
    
    
    for j in jsData:
        if country==j['country']:
            color=colorDict[min(rangeList, key=lambda x:abs(x-totalCases))]
            marker = folium.CircleMarker(location=[j['latitude'],j['longitude']],popup=data,color=color,fill=True).add_to(folium_map)

            
folium_map.save("covidmap.html")




