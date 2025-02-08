# Real-Time Stock Market Dashboard

## Overview

The **Real-Time Stock Market Dashboard** is an interactive web application that visualizes daily stock market trends using Python, Dash, and Plotly. This dashboard fetches historical stock data via the Twelve Data API, processes the data to compute key technical indicators, and presents interactive visualizations to help users gain insights into stock performance.

This project demonstrates:
- **Data Acquisition:** Integrating with a REST API to retrieve live stock market data.
- **Data Processing:** Utilizing Pandas for cleaning, transforming, and calculating technical metrics.
- **Data Visualization:** Building interactive charts with Plotly to effectively communicate data insights.
- **Dashboard Development:** Creating a dynamic dashboard using Dash, featuring real-time updates and user interactivity.

## Features

- **Stock Data Retrieval:**
  - Fetches one-year daily time series data for selected stocks using the Twelve Data API.
  - Supports multiple stock symbols (e.g., AAPL, TSLA, MSFT, AMZN, GOOGL).

- **Data Processing & Analysis:**
  - **Moving Averages:** Calculates 50-day and 200-day moving averages to identify trend directions.
  - **Daily Returns:** Computes daily percentage changes to monitor stock performance.
  - **Volatility:** Determines volatility using the 20-day rolling standard deviation of daily returns.

- **Interactive Visualizations:**
  - **Stock Price Chart:** A line chart showing closing prices alongside the moving averages.
  - **Daily Returns Chart:** A bar chart visualizing daily percentage returns.
  - **Volatility Chart:** A line chart tracking the volatility of the stock over time.

- **Real-Time Updates:**
  - Utilizes Dash's `dcc.Interval` component to auto-refresh the dashboard every 60 seconds.

- **User Controls:**
  - A dropdown menu for selecting different stock symbols.
  - The dashboard updates automatically based on user input and refresh intervals.

## Technologies Used

- **Programming Language:** Python 3.x
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
- **HTTP Requests:** [Requests](https://requests.readthedocs.io/)
- **Data Visualization:** [Plotly Graph Objects](https://plotly.com/python/graph-objects/)
- **Web Framework:** [Dash](https://dash.plotly.com/)
- **API:** [Twelve Data API](https://twelvedata.com/)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/YourUsername/Real-Time-Stock-Market-Dashboard.git
   cd Real-Time-Stock-Market-Dashboard
