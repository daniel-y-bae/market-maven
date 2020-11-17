# Market Maven

> Check out a live demo of Market Maven by pointing an internet browser to: https://www.mymarketmaven.com

## Description

**Market Maven** is a novel web application for users to explore and compare real estate markets. By leveraging advanced analytics and visualizations, users can use Market Maven to search a wide breadth of real estate market characteristics, including geography, demographics, environmental factors, price, and volume.

> Note: Within the context of Market Maven, a real estate market is defined at the level of a U.S. county.

At a high level, Market Maven is composed of three distinct components:

1. A choropleth map of the U.S. that visualizes several real estate market metrics, organized by topic (e.g., economy, geography, etc.), by county.

2. A details page that provides in-depth reporting of real estate market metrics and provides a feature to directly compare two different real estate markets (i.e. counties).

3. A clustering page that leverages machine learning to allow users to input a real estate market and find similar markets (counties) throughout the U.S.

This tool is delivered as a web application accessible via a desktop or mobile internet browser. 

It was developed in Python 3.7 using the following open-source packages:
    
* Dash
* Leaflet
* Pandas
* Plotly
* Scikit-Learn

Also, the backend is powered by a SQLite database.

Remember, Market Maven is YOUR real estate markets comparison tool!

## Installation

Setting up Market Maven locally for running and experimentation is easy! Just follow these steps.

> Important: Market Maven was developed using Python 3.7. Please use Python 3.7 (or higher) to run Market Maven without error.

From the computer's command line or terminal:

1. _(Optional)_ Pull Market Maven from it's GitHub repository:

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

*On Windows:* 

```
$ .venv\Scripts\Activate
```

*On Mac/Linux:* 

```
$ source .venv/bin/activate
```

5. Install Market Maven's software dependencies:

```
$ pip install --user -r requirements.txt
```

Congratulations! Market Maven is now set up and ready for execution.


## Execution

Executing and running Market Maven is just as easy as its installation! Just follow these steps.

> Important: The following instructions assume all of the INSTALLATION steps were completed successfully.

From the computer's command line or terminal:

1. Launch Market Maven:

```
$ python index.py
```

2. View Market Maven in an internet browser by visiting the following URL: http://127.0.0.1:8050

> Important: The command line or terminal used to launch Market Maven must remain open during its execution.
