import logging

def remove(update: str, list: list[dict]):
    logging.info(f'Update element to be removed: {update}')
    length = len(list)
    event = 0
    for event in range(length):
        title = list[event]['title']
        #Iterates through each element in the list and finds the title for the given element
        if update == title:
            list.pop(event)
            return list
            #If the value and name are the same, the element is removed from the list and the function closes
        else:
            event = event + 1
            #If the value and name do not match, the loop will iterate to the next element
    return list

def minutes_to_seconds(minutes: str) -> int:
    seconds = int(minutes)*60
    #Calculates the number of seconds in a number of given minutes
    return seconds

def hours_to_minutes(hours: str) -> int:
    seconds = int(hours)*60
    #Calculates the number of minutes in a number of given hours
    return seconds

def hhmm_to_seconds(hhmm: str) -> int:
    logging.info(f'Hours and seconds to be converted into seconds: {hhmm}')
    seconds = minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + minutes_to_seconds(hhmm.split(':')[1])
    #Calculates the number of seconds in a number of given hours and minutes in the format hh:mm
    return seconds

def hhmmss_to_seconds(hhmmss: str) -> int:
    logging.info(f'Hours and seconds to be converted into seconds: {hhmmss}')
    seconds = minutes_to_seconds(hours_to_minutes(hhmmss.split(':')[0])) + minutes_to_seconds(hhmmss.split(':')[1]) + \
    int(hhmmss.split(':')[2])
    #Calculates the number of seconds in a number of given hours, minutes  and seconds in the format hh:mm:ss
    return seconds