# Bird API Dashboard

A responsive dashboard built with [Dash](https://dash.plotly.com/) that fetches and visualizes bird observation data from the eBird API. This project displays key performance indicators (KPIs) and interactive charts (bar, pie, and line charts) to help users explore bird data by region.

## Overview

The Bird API Dashboard allows users to:
- **Fetch bird observation data** from the eBird API based on a selected region and a specified number of observations.
- **Display KPIs** such as the total number of unique bird species observed and statistics on counts per observation.
- **Visualize the data** using interactive charts:
  - **Bar Chart:** Displays total bird counts by species.
  - **Pie Chart:** Shows the percentage distribution of bird counts by species.
  - **Line Chart:** Illustrates the trend of bird observations over time.
  
This project demonstrates my below skills such as to 
-**Gather Data:** Connect to a live API (eBird) and handle data retrieval.
- **Data Processing:** Clean and manipulate data using [Pandas](https://pandas.pydata.org/).
- **Data Analysis:** Compute meaningful KPIs (e.g., unique species count, average counts).
- **Data Visualization:** Create insightful visualizations (bar, pie, and line charts) using Plotly.
- **Dashboard Development:** Build interactive dashboards that allow end-users to filter data dynamically.

## Features

- **Interactive User Inputs:**  
  - Dropdown to select a region (e.g., New York, California, Texas, etc.).
  - Slider to choose the number of observations to fetch.
- **Data Fetching and Processing:**  
  - Uses the eBird API to get recent bird observation data.
  - Saves fetched data to a CSV file and reads from it for analysis.
- **Dynamic Visualizations:**  
  - Bar, pie, and line charts generated with Plotly Express.
- **Dashboard Layout:**  
  - Built with Dash for a clean and responsive interface.

## Prerequisites

Make sure you have the following installed on your system:
- Python 3.6 or later
- [pip](https://pip.pypa.io/en/stable/installation/)


