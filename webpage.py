from covid_data_handler import parse_csv_data, process_covid_csv_data, covid_API_request, \
    schedule_covid_updates, dict_to_csv
from covid_news_handling import news_API_request, update_news
from extra_functions import remove, hhmm_to_seconds, hhmmss_to_seconds
from config_handler import config_handler
from flask import Flask, config, render_template, request
import sched, time
import logging

logging.basicConfig(filename=config_handler()[2], level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s: %(message)s')
logging.info('Started')
events = list()
s = sched.scheduler(time.time, time.sleep)
logging.info('events and s declared')
#Declaring global variables to be used later on in the program

app = Flask(__name__)
logging.info('Flask found')
app.config["SECRET_KEY"] = config_handler()[3]

@app.route('/index')
def index():
    logging.info('index page loaded')
    global events
    global news_articles

    try:
        news_articles
        logging.warning('news_articles does not exist')
    except:
        news_articles = news_API_request()
        logging.info('news_articles assigned to news_API_request function')
    #Sees if news_articles exists, and if not, assigns it to the news_API_request function

    if request.args.get('update'):
        logging.info('Inputted time has been entered')
        tim = request.args.get('update')
        logging.info(f'Inputted time has been retrieved: {tim}')
        time_in_seconds = hhmm_to_seconds(tim)
        logging.info(f'Inputted time has been converted into seconds: {time_in_seconds}')
        #If a time has been entered on the webpage, it retrieves it and converts it into seconds
        local_time = time.localtime()
        logging.info(f'Local time has been retrieved: {local_time}')
        current_time = time.strftime("%H:%M:%S", local_time)
        logging.info(f'Local time has been put in proper format: {current_time}')
        #The local time is retrieved and formatted in a suitable format that can be converted
        current_time_in_seconds = hhmmss_to_seconds(current_time)
        logging.info(f'Local time converted into seconds: {current_time_in_seconds}')
        difference = time_in_seconds - current_time_in_seconds
        logging.info(f'Difference in seconds has been calculated: {difference}')
        '''The local time is converted into seconds and the difference between the inputted time
        and current time is calculated'''

        if difference < 0:
            logging.info('Difference is negative')
            day_in_seconds = hhmmss_to_seconds('24:00:00')
            logging.info(f'1 day converted into seconds: {day_in_seconds}')
            difference += day_in_seconds
            logging.info(f'Difference and day are added in seconds: {difference}')
            '''If the time inputted is earlier than the current time, it will be counted as the 
            time for the next day, and the equivalent of a day in seconds is added'''
        
        if request.args.get('two'):
            logging.info('Text has been inputted')
            event_name = request.args.get('two')
            logging.info(f'Inputted text has been retrived: {event_name}')
            #The content of the text box is checked, and if it exists, it is retrieved
            if request.args.get('covid-data'):
                logging.info('Update Covid Data has been checked')
                schedule_covid_updates(difference, event_name)
                logging.info('Updating local covid data has been scheduled')
                schedule_covid_updates(difference, event_name, 'England', 'nation')
                logging.info('Updating national covid data has been scheduled')
                '''If the Update Covid Data checkbox is checked, the scheduler will update the 
                covid_API_request function for the local and national data after the given delay'''
                ev = {"title": event_name, "content": tim}
                logging.info(f'Update element has been declared: {ev}')
                events.append(ev)
                logging.info('Update element appended to events list')
                '''The event name and time are stored in a dictionary and added to a list, which is 
                displayed on the page'''
                if request.args.get('repeat'):
                    logging.info('Repeat checkbox has been checked for updating covid data')
                    index = events.index(ev)
                    logging.info(f'Index of update element retrived: {index}')
                    events[index]["title"] = f'Repeating update: {event_name}'
                    logging.info(f'Title of update element updated: {events[index]["title"]}')
                    #Specifies the event will be repeating to help inform the user
                    # for i in range(1, 365):
                    #     difference = difference + (i * hhmmss_to_seconds('24:00:00'))
                    #     schedule_covid_updates(difference, event_name)
                    
                    logging.info(f'Updates scheduled for 364 more days for time: {tim}')
                    '''If the Repeat Update checkbox is also checked, the scheduler will run at the 
                    same time everyday for a year (hence the loop iterates up to 364 plus the current 
                    day)'''

            if request.args.get('news'):
                logging.info('Update News has been checked')
                update_news(difference, event_name)
                logging.info('Update News has been scheduled')
                '''If the Update News checkbox is checked, the scheduler will update the 
                news_API_request function after the given delay'''
                ev = {"title": f'News: {event_name}', "content": tim}
                logging.info(f'Update element has been declared: {ev}')
                events.append(ev)
                logging.info('Update element appended to events list')
                '''The event name and time are stored in a dictionary and added to a list, which is 
                displayed on the page. The name has "News: " prefixing it to make it clear the event
                is to update the news rather than the Covid data'''
                if request.args.get('repeat'):
                    logging.info('Repeat checkbox has been checked for updating news')
                    index = events.index(ev)
                    logging.info(f'Index of update element retrived: {index}')
                    events[index]["title"] = f'News repeating update: {event_name}'
                    logging.info(f'Title of update element updated: {events[index]["title"]}')
                    for i in range(1, 365):
                        difference = difference + (i * hhmmss_to_seconds('24:00:00'))
                        update_news(difference, event_name)
                    logging.info(f'Updates scheduled for 364 more days for time: {tim}')
                    '''If the Repeat Update checkbox is also checked, the scheduler will run at the 
                    same time everyday for a year (hence the loop iterates up to 364 plus the current 
                    day)'''

    if request.args.get('update_item'):
        logging.info('Update has been requested to be deleted')
        update = request.args.get('update_item')
        logging.info(f'Update element has been retrieved: {update}')
        #If the close button on a scheduled update is clicked, the value of the update will be retrieved
        events = remove(update, events)
        logging.info(f'Update element has been removed: {update}')
        #Using the value (name of the update) it is removed from the events list using the remove function

    if request.args.get('notif'):
        logging.info('News has been requested to be deleted')
        update = request.args.get('notif')
        logging.info(f'News element has been retrieved: {update}')
        #If the close button on a news headline is clicked, the value of the update will be retrieved
        news_articles = remove(update, news_articles)
        logging.info(f'News element has been removed: {update}')
        #Using the value (title of article) it is removed from the events list using the remove function

    return render_template('index.html', title='Covid Dashboard', image='covid-icon.jpg', favicon='/static/images/favicon.ico', 
    news_articles=news_articles, location='Exeter', 
    local_7day_infections=process_covid_csv_data(parse_csv_data(dict_to_csv(covid_API_request())))[0], nation_location='England', 
    national_7day_infections=process_covid_csv_data(parse_csv_data(dict_to_csv(covid_API_request('England', 'nation'))))[0], 
    hospital_cases=process_covid_csv_data(parse_csv_data(dict_to_csv(covid_API_request('England', 'nation'))))[1], 
    deaths_total=process_covid_csv_data(parse_csv_data(dict_to_csv(covid_API_request('England', 'nation'))))[2], updates=events)

if __name__ == '__main__':
    app.run()
logging.info('App is running')