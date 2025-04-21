import pandas as pd 
import numpy as np 
import streamlit as st
import sklearn 
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.impute import SimpleImputer



st.header("Data Cleaning and Visualization App")

st.subheader("This is a app designed to clean data and also visualize the information.")

st.write("First, we load the data.")

data = pd.read_csv("https://raw.githubusercontent.com/Ogunberry99/csv-file/refs/heads/main/athlete_events.csv")

st.write(data)

st.write("Now lets clean the dataset, first look for missing values:")

original_shape = data.shape

def check_data_quality(data):
    quality_report = {
        'missing_values': data.isnull().sum().to_dict(),
        'duplicates': data.duplicated().sum(),
        'total_rows': len(data)
        }
    return quality_report


def standardize_datatypes(data):
	for column in data.columns:
		if data[column].dtype == 'object':
			try:
				data[column] = pd.to_datetime(data[column])
				st.write(f"Converted {column} to datetime")
			except ValueError:
				try:
					data[column] = pd.to_numeric(data[column].str.replace('$', "").str.replace(',', ''))
					st.write(f"Converted {column} to numeric")
				except:
					pass 
	return data 

#This is a function to impute missing values:
def handle_missing_values(data):
	#Handle numerc columns
	numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns 
	if len(numeric_columns) > 0:
		num_imputer = SimpleImputer(strategy='median')
		data[numeric_columns] = num_imputer.fit_transform(data[numeric_columns])

	#Handle catergorical columns
	categorical_columns = data.select_dtypes(include=['object']).columns
	if len(categorical_columns) > 0:
		cat_imputer = SimpleImputer(strategy='most_frequent')
		data[categorical_columns] = cat_imputer.fit_transform(data[categorical_columns])
	return data 


def remove_duplicates(data):
	data = data.loc[:, ~data.columns.duplicated()].copy


#Now validate the results:
def validate_cleaning(data):
	quality_report = {
	  'missing_values': data.isnull().sum().to_dict(),
	  'duplicates': data.duplicated().sum(),
	  'total_rows': len(data)
	}
	return quality_report


st.write('Check Data Quality')
st.write(check_data_quality(data))

st.write("Standardize Datatypes:")
st.write(standardize_datatypes(data))

st.write("Handle Missing Values")
st.write(handle_missing_values(data))

st.write("Remove Duplicate Columns")
st.write(remove_duplicates(data))

st.write("Validate Cleaning")
st.write(validate_cleaning(data))


st.write("cleaned data")
st.write(data)



st.write("Lets visualize some data")

global numeric_columns
numeric_columns = list(data.select_dtypes(['float', 'int']).columns)


st.sidebar.title("Navigation")

st.sidebar.header("Let's Manipulate the Data")

chart_select = st.sidebar.selectbox(
		label="Select the chart type",
		options=['Scatterplots', 'Lineplots', 'Histogram', 'Boxplot']
		)


if chart_select == 'Scatterplots':
	st.sidebar.subheader("Scatterplot Settings")
	x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
	y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
	plotly_figure = px.scatter(data_frame=data, x=x_values, y=y_values)
	st.plotly_chart(plotly_figure)
elif chart_select == 'Lineplots':
	st.sidebar.subheader("Lineplot Settings")
	x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
	y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
	plotly_figure = px.line(data_frame=data, x=x_values, y=y_values)
	st.plotly_chart(plotly_figure)
elif chart_select == 'Histogram':
	st.sidebar.subheader("Histogram Settings")
	x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
	y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
	plotly_figure = px.hist(data_frame=data, x=x_values, y=y_values)
	st.plotly_chart(plotly_figure)
elif chart_select == 'Boxplots':
	st.sidebar.subheader("Boxplot Settings")
	x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
	y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
	plotly_figure = px.box(data_frame=data, x=x_values, y=y_values)
	st.plotly_chart(plotly_figure)
 











