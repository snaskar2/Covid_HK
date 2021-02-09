# COVID_HK

This project is about building a dashboard to monitor the current COVID-19 situation in Hong Kong for the Yuan Modeling Group at City University of Hong Kong. The scope of the project might be extended in the future.

The dashboard was deployed using Heroku and can be viewed <a href="https://ymgcovidhk.herokuapp.com/" target="_blank">here</a>.

## Data Sources
- [Centre for Health Protection, Hong Kong](https://www.chp.gov.hk/)
- [Coronavirus Source Data, Wikipedia](https://en.wikipedia.org/wiki/COVID-19_pandemic_cases)
- ___________ (for geospatial information on hong kong - HK Shapefiles)

## Technology Stack Used
- Python (numpy + pandas + requests : For data-preprocessing )
- Plotly Dash (For building dashboard )
- Heroku (For deploying dashboard )
- Mapbox (used as basemap )

## Instructions for deploying the app on heroku:
- Install the libraries as listed in the requirements.txt file
- Before installing geopandas you must install GDAL,pyproj,fiona and shapely manually in your 
- pip freeze >requirements.txt
- Remove Fiona GDAL,pyproj, Shapely,Fiona,pywin from requirements.txt as heroku has some problems in deploying them
- Initialize git and create runtime.txt, Procfile, .gitignore
- Link repository to remote heroku repository and deploy
