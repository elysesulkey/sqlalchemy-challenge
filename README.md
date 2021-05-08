# sqlalchemy-challenge

This project uses Python and SQLAlchemy to do basic climate analysis and data exploration of a climate database for Honolulu, Hawaii. 

The Climate Analysis jupyter notebook uses SQLAlchemy create_engine to connect to the Hawaii sqlite database then uses SQLAlchemy automap_base() to reflect the tables into classes and saves a reference to those classes called Station and Measurement before linking Python to the database by creating an SQLAlchemy session.

The precipitation analysis finds the most recent date in the data set and retrieves the last 12 months of precipitation data by querying the 12 preceding months of data. It selects only the date and prcp values and loads the query results into a Pandas DataFrame, setting the index to the date column and sorting the DataFrame values by date. The results are ploted using the DataFrame plot method and Pandas is used to print the summary statistics for the precipitation data.

The station analysis runs a query to calculate the total number of stations in the dataset and to find the most active stations (i.e. which stations have the most rows?). The stations and obvervation counts are listed in descending order. The lowest, highest, and average temperature is calculated for the most active staiton. 
The data is then queried to retrieve the last 12 months of temperature observation data (TOBS) and filtered by the station with the highest number of observations.
The data is then queried for the last 12 months of temperature observation data for this station and the results are plotted as a histogram with bins=12.

The bonus portion uses pandas to convert the date column format from string to datetime, set the date column as the DataFrame index, and drop the date column.
It identifies the average temperature in June and December at all stations across all available years in the dataset then uses a paired t-test to determine whether the difference in the means, if any, is statistically significant. 

The second bonus portion uses the calc_temps function to calculate the min, avg, and max temperatures for a proposed August trip using the matching dates from a previous year. It plots the min, avg, and max temperature from the previous query as a bar chart titled Trip Avg Temp. It also calculates the rainfall per weather station using the previous year's matching dates, sorting the information in descending order by precipitation amount and listing the station, name, latitude, longitude, and elevation. It then calculates the daily normals using the daily_normals function for the dates of the trip, appending to a list called normals. Normals is loaded into a Pandas DataFrame, setting the index equal to the date. This datafram is used to plot an area plot (stacked=False) for the daily normals.

Finally, the session is closed out. 


The app.py file creates a Flask API based on the queries in the previous jupyter notebook. Flask is used to create the routes before listing all routes that are available. The query results are converted to a dictionary using date as the key and prcp as the value and a JSON representation of the dictionary is returned. Next, a JSON list of stations from the dataset is returned before querying the dates and temperature observations of the most active station for the last year of data, then returning a JSON list of temperature observations (TOBS) for the previous year. A JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range is returned. When given the start only, it calculates TMIN, TAVG, and TMAX for all dates greater than and equal to the start date. When given the start and the end date, it calculates the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

