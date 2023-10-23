import os, sys, requests
from logger import logging
from exception import LumiException
from dotenv import load_dotenv

from components.lumi_pull import LumiData
from constants.eln import SEND_DATA, SANDBOX_BASE_URL
from components.eln_data import ELN
import streamlit as st

load_dotenv('../../.env')

test_eid = "experiment:b572a4ea-67e4-4333-b34e-bd78a8d3ee3d"


class LumiEln:

    def __init__(self, 
                 eid: str,
                 file = None,
                 base_url: str = SANDBOX_BASE_URL,
                 api_key = None):
        
        self.eid = eid
        self.data = file
        self.url = base_url + self.eid + "/children/" "test.png" + "?force=true"
        self._headers = {'x-api-key': api_key}

    
    def send_data_to_eln(self):
        try:
            response = requests.post(self.url, headers= self._headers, data = self.data)

            if response.status_code == 201:
                return "success"
            else:
                return response.status_code

        except Exception as e:
            print(f"Error: {str(e)}")


