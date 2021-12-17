from test_covid_data_handler import *
from test_news_data_handling import *
from test_config_handler import *
from test_extra_functions import *
import schedule, time

def test_functions(interval):
    schedule.every(interval).seconds.do(test_parse_csv_data)
    schedule.every(interval).seconds.do(test_process_covid_csv_data)
    schedule.every(interval).seconds.do(test_covid_API_request)
    schedule.every(interval).seconds.do(test_dict_to_csv) 
    schedule.every(interval).seconds.do(test_schedule_covid_updates)
    schedule.every(interval).seconds.do(test_news_API_request) 
    schedule.every(interval).seconds.do(test_update_news)
    schedule.every(interval).seconds.do(test_config_handler)
    schedule.every(interval).seconds.do(test_remove)
    schedule.every(interval).seconds.do(test_minutes_to_seconds)
    schedule.every(interval).seconds.do(test_hours_to_minutes) 
    schedule.every(interval).seconds.do(test_hhmm_to_seconds)
    schedule.every(interval).seconds.do(test_hhmmss_to_seconds)

    
    while True:
        schedule.run_pending()
        time.sleep(1)