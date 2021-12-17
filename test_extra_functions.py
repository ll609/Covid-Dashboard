from extra_functions import remove
from extra_functions import minutes_to_seconds
from extra_functions import hours_to_minutes
from extra_functions import hhmm_to_seconds
from extra_functions import hhmmss_to_seconds

def test_remove():
    updates = [{'title': 'a','content': 'abc'}, {'title': 'b','content': 'def'}, 
    {'title': 'c','content': 'ghi'}, {'title': 'd','content': 'jkl'}]
    assert len(remove('a', updates)) == len(updates)
    assert updates == [{'title': 'b','content': 'def'}, {'title': 'c','content': 'ghi'}, 
    {'title': 'd','content': 'jkl'}]

def test_minutes_to_seconds():
    minutes = '60'
    assert minutes_to_seconds(minutes) == 3600
    assert isinstance(minutes_to_seconds(minutes), int)

def test_hours_to_minutes():
    hours = '14'
    assert hours_to_minutes(hours) == 840
    assert isinstance(hours_to_minutes(hours), int)

def test_hhmm_to_seconds():
    hhmm = '13:54'
    assert hhmm_to_seconds(hhmm) == 50040
    assert isinstance(hhmm_to_seconds(hhmm), int)

def test_hhmmss_to_seconds():
    hhmmss = '18:30:27'
    assert hhmmss_to_seconds(hhmmss) == 66627
    assert isinstance(hhmmss_to_seconds(hhmmss), int)

test_remove()
test_minutes_to_seconds()
test_hours_to_minutes()
test_hhmm_to_seconds()
test_hhmmss_to_seconds()