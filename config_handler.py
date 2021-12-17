import json

def config_handler():
    with open('config.json', "r") as f:
        config_file = json.load(f)
        config = config_file['data'][0]
        APIkey = config['APIkey']
        data_file = config['data_file']
        log_file = config['logging_file']
        secret_key = config['secret_key']

    return APIkey, data_file, log_file, secret_key