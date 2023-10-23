import os, sys, requests
from logger import logging
from exception import LumiException
from dotenv import load_dotenv
import streamlit as st

from constants.lumi import CREATE_EXP
from components.eln_data import ELN


load_dotenv('../../.env')


class LumiCreateExp:
    def __init__(self,
                 data,
                 lumi_url: str = CREATE_EXP ) -> None:
        
        self.data = data
        self.url = lumi_url
        self._api_key = os.environ.get("AuthToken")
        self._authToken = f"Bearer {self._api_key}"
        self._headers= {
            "Authorization": self._authToken,
            "Content-Type": "application/json"
        }


    
    def create_experiment(self):
        
        response = requests.post(url = self.url,
                                 json= self.data,
                                 headers= self._headers)
        
        if response.status_code == 200:
            response_json = response.json()
            output = response_json.get("output")
            return "success"
        elif response.status_code == 400:
            try:
                response_json = response.json()
                error_message = response_json.get("error")
                if "duplicate key value violates unique constraint" in error_message:
                    st.error("Experiment already exists")
                else:
                    print(f"Error Message: {error_message}")
            except ValueError:
                print("Error Response:", response.text)
        else:
            print(f"POST request failed with status code {response.status_code}.")

        return None

# sandbox experiment
# eid = "experiment:099cd778-ae92-4fa3-998d-c7ab5caf4b6e"
# eid = "experiment:b572a4ea-67e4-4333-b34e-bd78a8d3ee3d"

# e = ELN(eid = "experiment:b572a4ea-67e4-4333-b34e-bd78a8d3ee3d")
# data = e.initiate_data_extraction()

# l = LumiCreateExp(data= data)
# l.create_experiment()