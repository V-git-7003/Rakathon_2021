import jproperties
from jproperties import Properties

start_urls = []

def nifty_fifty_urls_from_properties(file_name):
    configs = Properties()
    with open(file_name, 'rb') as config_file:
        configs.load(config_file)
    items_view = configs.items()
    for item in items_view: 
        start_urls.append(item[1].data)
    return start_urls
        