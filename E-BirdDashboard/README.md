# BusinessProcessAutomationProject

**#API key - 11tm0mmamal1** Replace this API key in the code while running this project code

# 🐦 E-Bird USA: Interactive Birdwatching Dashboard

## 📌 Overview

The **E-Bird USA Dashboard** is an interactive Python application that visualizes real-time birdwatching data across U.S. states using the eBird API. Built using **Dash and Plotly**, this project allows users to explore bird species diversity, sighting trends, and observation statistics in an intuitive and visual format. It’s designed to make birdwatching data accessible and engaging for conservationists, researchers, and enthusiasts alike.

---

## 🎯 Why This Project?

While platforms like [eBird](https://ebird.org/home) provide rich bird sighting data, accessing and analyzing it programmatically can be overwhelming. The motivation behind this project was to:

- Transform raw JSON-based API data into easy-to-use visualizations.
- Create a real-time dashboard for exploring bird observations in the U.S.
- Handle **API rate limits** gracefully by saving snapshots to CSV.
- Build a practical use case using **Dash, Plotly, and the eBird API**.

---
## Screenshots of Dashboard
<img width="1860" height="1021" alt="image" src="https://github.com/user-attachments/assets/dce82cb3-3240-4e6a-98f6-c8ded7880d72" />
<img width="1863" height="1016" alt="image" src="https://github.com/user-attachments/assets/5a759a96-b90b-4b91-b4f0-3e3fa9148399" />
<img width="1860" height="1011" alt="image" src="https://github.com/user-attachments/assets/3f5e7b3e-b0f5-43f8-bafb-2f36168b96e1" />
<img width="1857" height="1017" alt="image" src="https://github.com/user-attachments/assets/6c838ba5-add6-47e2-aa54-32a6f3ab7990" />



## 🛠 Tech Stack

| Component           | Purpose                                     |
|--------------------|---------------------------------------------|
| **Python**         | Core language for scripting and app logic   |
| **Dash**           | Web framework for creating interactive UI   |
| **Plotly**         | Rendering charts like bar, pie, and line    |
| **Pandas**         | Data cleaning, aggregation, and transformation |
| **eBird API**      | Real-time bird sighting data by region      |
| **CSV Storage**    | Caching data when API hits rate limits      |

---

## 🧠 Architecture & Code Design

### 1. **Data Acquisition via eBird API**
- The app fetches bird data dynamically using region codes like `US-NY`, `US-CA`, etc.
- A `maxResults` slider lets the user control how much data to pull.
- Data is fetched **on-demand** based on user input.

### 2. **CSV Caching Strategy**
- To avoid hitting the **eBird API’s rate limits**, the app:
  - Fetches data once per request
  - Saves the output to `bird_data.csv`
  - Reuses the local CSV for charting and KPIs
- This ensures **performance stability** and allows the app to function even when API quota is exhausted or temporarily unavailable.

### 3. **KPIs Computed from Data**
- Total unique bird species
- Average number of birds per observation
- Maximum and minimum bird counts in a single sighting

These KPIs are computed using `pandas` and shown at the top of the dashboard.

### 4. **Visualizations**
- 📊 **Bar Chart**: Displays total bird count by species
- 🥧 **Pie Chart**: Shows species percentage share, grouping rare sightings into "Others"
- 📈 **Line Chart**: Displays daily observation trends using timestamps

---

## 📂 Features

- 📍 Selectable region codes for 10 major U.S. states
- 🎚 Adjustable observation count slider (10–200)
- 📈 Visual trends of birdwatching activity
- 📊 Interactive bar and pie charts for species stats
- 🧾 Real-time KPIs for quick overview

---

## 🚀 Getting Started

### 🖥 Prerequisites
Make sure you have the following Python libraries installed:

```bash
pip install dash pandas plotly requests

