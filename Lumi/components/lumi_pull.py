import os, sys, requests
from logger import logging
from exception import LumiException
from dotenv import load_dotenv
from io import BytesIO

from constants.lumi import GET_EXP
from components.eln_data import ELN

load_dotenv('../../.env')


class LumiData:
    def __init__(self,
                 eid= None,
                 jwt_token = None,
                 get_url: str =  GET_EXP) -> None:
        
        self.eid = eid
        self.params = {"id": self.eid}
        self.url = get_url
        # self._api_key = os.environ.get("AuthToken")
        self._api_key = jwt_token
        self._authToken = f"Bearer {self._api_key}"
        self._headers= {
            "Authorization": self._authToken,
            "Content-Type": "application/json"
        }

    
    def get_image(self, response):

        image_url = response["experiment"]["observations"][0]["Link"]
        # print(image_url)

        img_response = requests.get(image_url)

        if img_response.status_code == 200:
            image_data = BytesIO(img_response.content)
        else:
            print("Failed to download the image.")

        return image_data
    


    def get_data(self):
        response = requests.get(url = self.url,
                               params= self.params, headers= self._headers)
        
        # Check the response status code
        if response.status_code == 200:
            # print("POST request was successful.")
            response_json = response.json()  # Parse the JSON response
            img = self.get_image(response= response_json)
            return img
            
        else:
            print(f"POST request failed with status code {response.status_code}.")
            print(response.text)  # Print the response content for debugging





