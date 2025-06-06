import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import pandas as pd
import plotly.express as px

# Constants
API_KEY = "api-key"  # Replace with your actual API key
BASE_URL = "https://api.ebird.org/v2/data/obs/"


# Function to fetch bird observation data and save to a CSV file
def fetch_and_save_bird_data(api_key, region_code, max_results, filename='bird_data.csv'):
    """
            Grabs bird data from the eBird API for the given region and saves it to a CSV file.

            - `api_key`: EBird API token.
            - `region_code`: Which region are we looking at? (e.g., 'US-NY' for New York)
            - `max_results`: How many observations do you want to fetch?
            - `filename`: Where should we save the results? Default is 'bird_data.csv'.

            Returns:
                A pandas DataFrame with the fetched bird observation data, or an empty one if there was an issue.
            """
    headers = {"X-eBirdApiToken": api_key}
    params = {"maxResults": max_results}
    url = f"{BASE_URL}{region_code}/recent"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            return df
        else:
            print("No data found for the selected region.")
            return pd.DataFrame()
    else:
        print(f"Error: Unable to fetch data ({response.status_code})")
        return pd.DataFrame()

help(fetch_and_save_bird_data)
# Function to read bird observation data from a CSV file
def read_bird_data_from_file(filename='bird_data.csv'):
    """
           Reads bird data from a CSV file.

           - `filename`: The name of the file that want to be loaded. Default is 'bird_data.csv'.

           Returns:
               A pandas DataFrame with the loaded bird data.
           """
    return pd.read_csv(filename)
help(read_bird_data_from_file)

# Function to calculate KPIs
def calculate_kpis(df):
    """
            Analyzes bird data to give an overview of the birds.

            - `df`: The bird data as a pandas DataFrame.

            Returns:
                A dictionary with some stats like:
                - Total species observed
                - Average, max, and min counts per observation
            """
    total_species = df["comName"].nunique() if "comName" in df.columns else 0
    avg_count = df["howMany"].mean() if "howMany" in df.columns else 0
    max_count = df["howMany"].max() if "howMany" in df.columns else 0
    min_count = df["howMany"].min() if "howMany" in df.columns else 0
    return {
        "Total Unique Species": total_species,
        "Average Count per Observation": avg_count,
        "Max Count per Observation": max_count,
        "Min Count per Observation": min_count,
    }
help(calculate_kpis)

# Create a bar chart to visualize the bird count by species
def create_bar_chart(df):
    """
            Builds a bar chart to show the total bird count by species.

            - `df`: The bird data as a DataFrame.

            Returns:
                A Plotly bar chart showing bird counts by species.
            """
    species_count = df.groupby('comName')['howMany'].sum().fillna(0).reset_index(name='Total Count')
    # Rename 'comName' to 'Common Name' for display purposes
    species_count.rename(columns={'comName': 'Common Name of Birds'}, inplace=True)
    return px.bar(species_count, x='Common Name of Birds', y='Total Count', title="Bird Count by Species")
help(create_bar_chart)

# Create a pie chart to visualize the percentage distribution of bird counts by species
def create_pie_chart(df):
    """
           Creates a pie chart to visualize what percentage of birds each species represents.

           - `df`: The bird data as a pandas DataFrame.

           Returns:
               A Plotly pie chart with bird count percentages.
           """
    # Group data by species name and sum their counts
    species_count = df.groupby('comName')['howMany'].sum().reset_index(name='Total Count')

    # Calculate the total count for all species
    total_count = species_count['Total Count'].sum()

    # Calculate the percentage for each species
    species_count['Percentage'] = (species_count['Total Count'] / total_count) * 100

    # Apply threshold for "Others" category
    species_count['comName'] = species_count.apply(
        lambda row: row['comName'] if row['Percentage'] >= 5 else 'Others',
        axis=1
    )

    # Re-aggregate the data after grouping small percentages into "Others"
    species_count = species_count.groupby('comName', as_index=False)['Total Count'].sum()

    # Create and return the pie chart with customized text info
    return px.pie(species_count, names='comName', values='Total Count', title="Bird Count Distribution by Species")
help(create_pie_chart)

# Create a line chart to show the trend of bird observations over time
def create_line_chart(df):
    """
            Draws a line chart to show bird observations in a day.

            - `df`: The bird data as a pandas DataFrame.

            Returns:
                A Plotly line chart showing trends over day, or an empty chart if there's no date data.
            """
    if 'obsDt' in df.columns:
        df['obsDt'] = pd.to_datetime(df['obsDt'])
        df_grouped = df.groupby('obsDt').size().reset_index(name='Count')
        df_grouped.rename(columns={'obsDt': 'Observation Date'}, inplace=True)
        return px.line(df_grouped, x='Observation Date', y='Count', title="Trend of Bird Observations Over Time")
    return px.line()  # Return an empty line chart if no date data
help(create_line_chart)

# Function to update KPIs and charts based on user input
def update_dashboard(region, max_results):
    """
            Refreshes the dashboard based on user inputs (region and number of observations).

            - `region`: The region code (like 'US-NY') selected by the user.
            - `max_results`: The number of observations to fetch.

            Returns:
                A bunch of updated data for the dashboard, including:
                - Text for KPIs
                - Updated figures for the charts
            """
    # Fetch data based on selected region and number of observations (save to file)
    fetch_and_save_bird_data(API_KEY, region, max_results)

    # Read data from file
    df = read_bird_data_from_file()

    # Calculate KPIs
    kpis = calculate_kpis(df)

    # Update KPI values
    total_species_text = f"Total Unique Species: {kpis['Total Unique Species']}"
    avg_count_text = f"Average Count per Observation: {kpis['Average Count per Observation']:.2f}"
    max_count_text = f"Max Count per Observation: {kpis['Max Count per Observation']}"
    min_count_text = f"Min Count per Observation: {kpis['Min Count per Observation']}"

    # Create visualizations
    bar_chart = create_bar_chart(df)
    pie_chart = create_pie_chart(df)
    line_chart = create_line_chart(df)

    return total_species_text, avg_count_text, max_count_text, min_count_text, bar_chart, pie_chart, line_chart
help(update_dashboard)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the Dash app
app.layout = html.Div(children=[
    html.H1("E-Bird USA"),

    # Dropdown for selecting region
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[
                {'label': 'New York (US-NY)', 'value': 'US-NY'},
                {'label': 'California (US-CA)', 'value': 'US-CA'},
                {'label': 'Texas (US-TX)', 'value': 'US-TX'},
                {'label': 'Florida (US-FL)', 'value': 'US-FL'},
                {'label': 'Pennsylvania (US-PA)', 'value': 'US-PA'},
                {'label': 'Massachusetts (US-MA)', 'value': 'US-MA'},
                {'label': 'Washington (US-WA)', 'value': 'US-WA'},
                {'label': 'Ohio (US-OH)', 'value': 'US-OH'},
                {'label': 'Colorado (US-CO)', 'value': 'US-CO'},
                {'label': 'Virginia (US-VA)', 'value': 'US-VA'}
            ],
            value='US-NY',  # Default value
            style={'width': '50%'}
        ),
    ], style={'padding': '10px'}),

    # Slider for selecting number of observations
    html.Div([
        html.Label("Select Number of Observations:"),
        dcc.Slider(
            id='observation-slider',
            min=10,
            max=200,
            step=10,
            value=60,  # Default value
            marks={i: str(i) for i in range(10, 201, 10)}
        ),
    ], style={'padding': '10px'}),

    # Display KPIs
    html.Div([
        html.H3("Key Performance Indicators (KPIs):"),
        html.P(id="total-species"),
        html.P(id="avg-count"),
        html.P(id="max-count"),
        html.P(id="min-count")
    ]),

    # Display Bird Count by Species as a Bar Chart
    html.Div([
        html.H3("Bird Count by Species"),
        dcc.Graph(id="bar-chart")
    ]),

    # Display Bird Count Distribution as a Pie Chart
    html.Div([
        html.H3("Bird Count Distribution by Species"),
        dcc.Graph(id="pie-chart")
    ]),

    # Display Bird Observation Trend as a Line Chart
    html.Div([
        html.H3("Bird Observation Trend Over Time"),
        dcc.Graph(id="line-chart")
    ])
])


# Define callback to update KPIs and charts based on user input
@app.callback(
    [Output('total-species', 'children'),
     Output('avg-count', 'children'),
     Output('max-count', 'children'),
     Output('min-count', 'children'),
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('line-chart', 'figure')],
    [Input('region-dropdown', 'value'),
     Input('observation-slider', 'value')]
)
def update_dashboard_callback(region, max_results):
    return update_dashboard(region, max_results)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)