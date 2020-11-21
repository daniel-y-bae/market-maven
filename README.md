# Market Maven

Market Maven is YOUR real estate markets comparison tool!

> *Important: Check out a LIVE demo of Market Maven by pointing an internet browser to: https://www.mymarketmaven.com*

> *Important: The GitHub repository for this application is located at: https://github.com/keithdowd/market-maven*


## Description

Market Maven is a novel web application for users to explore and compare real estate markets. 

By leveraging advanced analytics and visualizations, users can use Market Maven to search a wide breadth of real estate market characteristics, including geography, demographics, environmental factors, price, and volume.

> *Important: In the context of Market Maven, a real estate market is defined at the level of a U.S. county.*

At a high-level, Market Maven is composed of three distinct components:

1. A **choropleth map** of the U.S. that visualizes several real estate market metrics, organized by topic (e.g., economy, geography, etc.), by county.
2. A **details** page that provides in-depth reporting of real estate market metrics and provides a feature to directly compare two different real estate markets (i.e. counties). 
3. A **clustering** page that leverages machine learning to allow users to input a real estate market and find similar markets (counties) throughout the U.S.

This tool is delivered as a web application accessible via a desktop or mobile internet browser. It was developed in Python 3.7 using the following open-source packages:
    
* __Dash__ (https://plotly.com/dash/): A open-source Python library for creating reactive, web-based application. Used to power the front-end and back-end processing of the tool, as well as provide the code infrastructure to serve it as a web application in the browser.
* __Leaflet__ (https://dash-leaflet.herokuapp.com): A Python wrapper for Leaflet, a leading open-source JavaScript library for creating mobile-friendly interactive maps. Used to power the choropleth map on the map (home) page.
* __Pandas__ (https://pandas.pydata.org): An open-source Python library for data analysis and manipulation. Used to prepare all data for the import into the back-end database, and manipulate data in real-time, where necessary, when the application is running.
* __Plotly__ (https://plotly.com): An open-source library for data visualization and UI tools for machine learning, data science, engineering and the sciences. (This application uses the Python wrapper for Plotly JS.) Used to power the visualization on the clustering page.
* __Scikit-Learn__ (https://scikit-learn.org): An open-source Python library for machine learning in Python. Used to train and run the clustering (k-nearest neighbors) model that is visualized on the clustering page.

Also, **SQLite3** (https://www.sqlite.org) powers the back-end database.

This application's directory structure and contents are described below for easy reference.

> *Important: Some of the data required to build the back-end database are available in this directory. The remaining data are pulled on-demand from API calls by the scripts in the "/scripts" directory.*

```
    /root: Root directory of the application. All commands on the command line (or terminal) should be executed from this directory.

        /assets: Assets (e.g., geoJSON files, back-end database, etc.) required for the application to successfully run.
            * fips-states.json: Simple dictionary that translates U.S. state FIPS codes to U.S. state names. Used by the map page for formatting purposes.
            * geojson-counties.json: GeoJSON that provides the U.S. county geometry for the choropleth map on the map page. Also includes some of the data in the SQLite database to visualize on the map.
            * geojson-states.json: GeoJSON that provides the U.S. state geometry for the choropleth map on the map page.
            * market_maven.sqlite: Back-end SQLite database that provides all of the data for the applications (sans those data provided by the geoJSON files).
            * styles.css: Cascading style sheet (CSS) that defines the styles for the application. Note that some styles are not included in this CSS and are instead embedded directly in the Python source.
        
        /data: Data files used to build the applications back-end database ("/assets/market_maven.sqlite") and geoJSON files.
	        * geojson-counties-template.json: U.S. county geoJSON template file for choropleth map.
            * list1_2020.xls: List of U.S. state and counties and identifier codes (e.g., CBSA, FIPS, etc.). Derived from U.S. Census.
            * PctUrbanRural_County.xls: Urban vs. rural population demographics by U.S. county. Derived from U.S. Census.
            * avg_annual_temp.csv: Average annual temperature data by U.S. state. Derived from https://www.currentresults.com.
            * avg_fall_temp.csv: Average Fall temperature data by U.S. state. Derived from https://www.currentresults.com.
            * avg_spring_temp.csv: Average Spring temperature data by U.S. state. Derived from https://www.currentresults.com.
            * avg_summer_temp.csv: Average Summer temperature data by U.S. state. Derived from https://www.currentresults.com.
            * avg_sunny_days.csv: Average number of sunny days by U.s. state. Derived from https://www.currentresults.com.
            * avg_winter_temp.csv: Average Winter temperature data by U.S. state. Derived from https://www.currentresults.com.
            * countypres_2000-2016.csv: Presidential election vote totals by political party ("political lean") by U.S. county. Derived from U.S. Census.
            * Data Dictionary - external.csv: List of all data used by Market Maven and their sources. Derived by the Market Maven project team.
            * neighbors.csv: Top 5 similar counties based on Market Maven's clustering algorithm. Derived by the "build_similar_counties_data.py" in the "scripts" directory.
            * all-geocodes-v2019.csv:  List of U.S. state and counties and identifier codes (e.g., CBSA, FIPS, etc.). Derived from U.S. Census.
            * state-geocodes-v2010.csv: List of U.S. state identifier codes (e.g., FIPS, Region, etc.). Derived from U.S. Census.
            * 2019_Gaz_counties_national.txt: Total land and water area (in square miles) by U.S. county. Derived from 2019 Gazetteer File.

        /scripts: Python scripts for compiling and building the back-end database.
            * build_market_maven_db.py: Builds the back-end database that is stores all of data required by the application.
            * build_geojson_counties.py: Builds the U.S. county geoJSON file that is required by the choropleth map displayed on the map page.
            * build_similar_counties_data.py: Compiles the similar counties data required by the clustering page that is also ingested and stored in the "/assets/market_maven.sqlite" database.
            * build_weather_data.py: Compiles the weather data required by the map and details pages that is also ingested and stored in the "/assets/market_maven.sqlite" database.

        * .gitignore: Defines the files and directories to ignore when commiting source to git version control.
        * app.py: Responsible for creating an instance of the application object. Necessary for mitigating a circular dependency with index.py.
        * CHANGELOG.md: Tracks the version releases of the application, as well as additions, edits, and other changes made to it over time.
        * CONTRIBUTING.md: Describes how to contribute to this project.
        * cluster.py: Layout, callbacks, and business logic for the cluster page of the application.
        * details.py: Layout, callbacks, and business logic for the details page of the application.
        * dictionary.py: Layout, callbacks, and business logic for the data dictionary page of the application.
        * index.py: Entry point for the application. Responsible for launching the application and managing URL routing.
        * LICENSE.md: Open-source (GNU GPLv3) software license for this application.
        * map.py: Layout, callbacks, and business logic for the choropleth map page of the application.
        * README.md: Markdown version of "README.txt" for the Github repository.
        * README.txt: The file you are reading right now.
        * requirements.txt: Defines the Python package requirements for this application. Used for installing the application.
```

## Installation

NO LOCAL INSTALLATION IS NECESSARY! Check out a LIVE demo of Market Maven by pointing an internet browser to: https://www.mymarketmaven.com

However, to deploy locally and run the application, just complete the following instructions.

> *Important: Market Maven was developed using Python 3.7. Please use version 3.7 of Python (or higher) to run Market Maven without error.*

### Set up the local environment

The purpose of the following instructions are to create and configure a local development environment.

> *Important: These instructions are absolutely necessary to execute Market Maven locally.*

From the computer's command line (or terminal) in the root directory:

1. (Optional) Pull Market Maven from it's GitHub repository:

```
    $ git pull https://github.com/keithdowd/market-maven.git
```

2. Navigate to Market Maven's root directory:

```
    $ cd market-maven
```

3. Create a Python virtual environment (inside Market Maven's root directory):

```
    $ python -m venv .venv
```

4. Activate the virtual environment:

On Windows: 
    
```
    $ .venv\Scripts\Activate
```

On Mac/Linux: 

```    
    $ source .venv/bin/activate
```

5. Install Market Maven's software dependencies:

```
    $ pip install --user -r requirements.txt
```

Congratulations! The local environment for Market Maven is configured.

### Build the back-end database

The purpose of the following instructions is to build the back-end database that stores the application's data and powers all of the metrics reported by the application.

> *Important: The database is provided prebuilt in the "/assets" directory as "market-maven.sqlite". ONLY EXECUTE THESE STEPS IF A REBUILD IS NECESSARY.*

From the computer's command line (or terminal) in the root directory:

1. Build the weather data:

> *Imporant: Open "/scripts/build_weather_data.py" in a code editor and review the comments before running the following command. There may be one or more manual steps necessary to complete before running the script.*

On Windows:

```
    $ python scripts\build_weather_data.py
```

On Mac/Linux:

```
    $ python scripts/build_weather_data.py
```

2. Build the similar counties data:

> *Important: Open "/scripts/build_similar_counties.py" in a code editor and review the comments before running the following command. There may be one or more manual steps necessary to complete before running the script.*

On Windows:

```
    $ python scripts\build_similar_counties.py
```

On Mac/Linux:

```
    $ python scripts/build_similar_counties.py
```

3. Build the back-end database:

> *Important: Open "/scripts/build_market_maven_db.py" in a code editor and review the comments before running the following command. There may be one or more manual steps necessary to complete before running the script.*

> *Important: This script requires the user to create a user account and obtain an API key from https://api.census.gov/data/key_signup.html. After obtaining an API key, paste the API key into the variable `api_key`.*

On Windows:

```
    $ python scripts\build_market_maven_db.py
```

On Mac/Linux:

```
    $ python scripts/build_market_maven_db.py
```

> *Important: Copy "market_maven.sqlite" from the "/data" directory to the "/assets" directory.*

Congratulations! The back-end database for Market Maven is built.

### Build the U.S. county geoJSON file

The purpose of the following instructions is to build the U.S. county geoJSON file that is necessary to power the choropleth map and visualizations displayed on the application's map page.

> *Important: The geoJSON file is provided prebuilt in the "/assets" directory as "geojson-counties.json". ONLY EXECUTE THESE STEPS IF A REBUILD IS NECESSARY.*

From the computer's command line (or terminal) in the root directory:

> *Important: Open "/scripts/build_geojson_counties.py" in a code editor and review the comments before running the following command. There may be one or more manual steps necessary to complete before running the script.*

1. Build the U.S. county geoJSON file:

On Windows:

```
    $ python scripts\build_geojson_counties.py
```

On Mac/Linux:

```
    $ python scripts/build_geojson_counties.py
```

> *Important: Copy "geojson_counties.json" from the "/data" directory to the "/assets" directory.*

Congratulations! The U.S. county geoJSON file is built. 

Assuming all other INSTALLATION instructions were succesfully completed, Market Maven is now ready to execute and run.

## Execution

Executing and running Market Maven is just as easy as its installation! Just follow these steps.

> *Important: The following instructions assume all of the INSTALLATION steps were completed successfully.*

From the computer's command line (or terminal) in the root directory:

1. Launch Market Maven:

```
    $ python index.py
```

2. View Market Maven in an internet browser by visiting the following URL:

```
    http://127.0.0.1:8050
```

> *Important: The command line (or terminal) used to launch Market Maven must remain open during its execution.*

Enjoy! :)
