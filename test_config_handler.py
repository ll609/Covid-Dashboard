from config_handler import config_handler

def test_config_handler():
    data = config_handler()
    assert data[0] == '96481cdb8b7440b88b70983976b00a62'
    assert data[1] == 'data.csv'
    assert data[2] == 'logfile.log'
    assert data[3] == 'abc'

test_config_handler()