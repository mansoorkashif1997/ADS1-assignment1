# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Change the column names
content = """Date
Location_ISO_Code
Location
New_Cases
New_Deaths
New_Recovered
New_Active_Cases
Total_Cases
Total_Deaths
Total_Recovered
Total_Active_Cases
Location_Level
City_or_Regency
Province
Country
Continent
Island
Time_Zone
Special_Status
Total_Regencies
Total_Cities
Total_Districts
Total_Urban_Villages
Total_Rural_Villages
Area_(km2)
Population
Population_Density
Longitude
Latitude"""

columns_list = content.split("\n")
columns_list

# Read the csv file
covid_data = pd.read_csv("covid_19_indonesia_time_series_all.csv",
                         names=columns_list, header=0, index_col=False)
print(covid_data)

# convert the date
covid_data['Date'] = pd.to_datetime(covid_data['Date'], format='%m/%d/%Y')
covid_data['month'] = covid_data['Date'].dt.month
covid_data['year'] = covid_data['Date'].dt.year


# Function to plot new cases and new deaths on a single figure
def plot_new_cases_deaths(data):
    plt.figure(figsize=(10, 6))

    # get indonesia data only
    covid_data_indonesia = data[data['Location_ISO_Code'] == 'IDN']

    new_cases_IDN = covid_data_indonesia.groupby(
        ['month', 'year']).agg({'New_Cases': ['sum']})
    new_deaths_IDN = covid_data_indonesia.groupby(
        ['month', 'year']).agg({'New_Deaths': ['sum']})

    new_cases_IDN.plot(label='New cases')
    new_deaths_IDN.plot(ax=plt.gca(), label='New deaths')

    plt.title('New COVID-19 Cases and New Deaths Over Time')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.legend()
    plt.show()


# Plotting new cases and new deaths on a single figure
plot_new_cases_deaths(covid_data)


# Function to plot the top seven cities with the highest new COVID-19 cases
def top_five_cities_new_cases_plot(data):

    # Grouping the data by 'location' and summing up the 'New Cases'
    city_data = data[data['Location_ISO_Code'] != 'IDN']
    city_new_cases = city_data.groupby(
        'Location')['New_Cases'].sum().nlargest(7)

    plt.figure(figsize=(12, 8))
    city_new_cases.plot(kind='bar', color=[
                        'red', 'blue', 'green', 'orange', 'purple', 'yellow', 'brown'])
    plt.title('Top Seven Cities with Highest New COVID-19 Cases')
    plt.xlabel('Cities')
    plt.ylabel('New Cases')
    plt.show()


# Plotting the top five cities with the highest new cases
top_five_cities_new_cases_plot(covid_data)


# Function to plot for total cases, deaths, and recovered cases (2020 to 2023)
def total_cases_deaths_recovered_plot(data):

    # Filtering data for the years 2020 to 2023
    filtered_data = data[(data['Date'].dt.year >= 2020) &
                         (data['Date'].dt.year <= 2023)]

    # Calculate total cases, deaths, and recovered
    total_cases = filtered_data['Total_Cases'].sum()
    total_deaths = filtered_data['Total_Deaths'].sum()
    total_recovered = filtered_data['Total_Recovered'].sum()

    # Creating labels and values for plot
    labels = ['Total Cases', 'Total Deaths', 'Total Recovered']
    values = [total_cases, total_deaths, total_recovered]

    plt.figure(figsize=(6, 9))
    plt.pie(values, labels=labels, colors=[
            'orange', 'yellow', 'blue'], autopct='%1.1f%%')
    plt.title('Total Cases, Deaths, and Recovered (2020-2023)')
    plt.show()


# Plotting pie plot for total cases, deaths, and recovered (2020-2023)
total_cases_deaths_recovered_plot(covid_data)
