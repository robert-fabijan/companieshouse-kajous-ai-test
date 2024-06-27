import requests
import yaml
import os
import datetime

class DataConfigurator:


    def __init__(self) -> None:
        pass
        



    def timeframe_window(self) -> (int, int):
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days = 1)

        return int(datetime.datetime.timestamp(start)), int(datetime.datetime.timestamp(end))
    

