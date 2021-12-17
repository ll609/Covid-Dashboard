Covid Dashboard

The Covid Dashboard will display local and national up-to-date data for Covid-19, including cases in the last 7 days
for both local and national, and the total number of deaths and hospital cases nationwide. The dashboard aims to give
users quick and easy to access data, while also updating them with the newest headlines relating to Covid-19.

Features:
- Ability to schedule updates to the data at a certain time. This can also be repeated everyday at the same time
- Ability to schedule updates to the news articles at a certain time. Can also be repeated everyday at the same time
- Up-to-date news headlines relating to Covid-19

Resources:
- UK Covid-19 API
- News API

How to use:
- Ensure all modules are installed:
	- Install csv by running: pip install csv
	- Install Cov19API by running: pip install uk-covid19
	- Install Flask by running: pip install Flask
	- Install Pandas by running: pip install pandas
- To run the application, run the webpage.py file. Ensure all files are in the folders they were downloaded as
- User Interface:
	Layout:
	- The left-hand side of the webpage will display the scheduled events, showing their name and the time the
	  event is scheduled for. Upon starting the program, this will be empty
	- The centre of the page will display Covid-19 data for the local area and nation. Below is a time input box,
	  text input box, three checkboxes and a submit button
	- The right-hand side of the webpage will display five news articles, each with a headline and a preview
	  of the article's content

	Adding a scheduled event:
	- Input a time using the time input box
	- Enter the name of the scheduled event in the textbox
	- Select the corresponding checkboxes as desired:
		- Update Covid data - This will update the local and national data once the time has been reached
		- Update news articles - This will update the news articles once the time has been reached
		- Repeat update - To be used only with the other checkboxes. Upon being checked, it will schedule
		  the update for everyday at the given time
		Note: The Update Covid data and Update news articles checkboxes can both be checked at the same time.
		The output is two events being scheduled with the same name, however the news update will specify it
		is for updating the news articles. If the repeat update checkbox is checked, it will be made clear 
		that the event will be repeated.

	Removing scheduled events and news articles:
	- To remove a scheduled event or news article, click the 'x' button on the top right corner of the element.
	  The page will refresh and it will no longer appear

	Changing the data:
	- To change the location of the local and/or national Covid-19 data, this can be done by inputting different
	  arguments into the covid_API_request function. Ensure the location_type is also changed depending on 
	  whether it is local or national
	- The data to be displayed on the webpage can also be changed. To add/change the columns of the UK Covid-19
	  API data, this can be done in the covid_API_request function. Make sure the process_covid_csv_data is 
	  updated as well to be able to process this new data. A Jinja variable will need to be changed/created in 
	  the HTML document and the relevant data from should be passed in in the render_template, assigned to the
	  Jinja variable name

Debugging:
- There are files containing test functions to confirm the functions are working as intended. If they run without
  any assertion errors, it means the functions are running correctly
- The logging file can be used to help determine what is running in the program. Each log will have a time, severity
  level and message

 