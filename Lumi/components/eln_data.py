import os, requests
from logger import logging
from exception import LumiException
from dotenv import load_dotenv
from constants.eln import ARTIFACT_DIR, BASE_URL, SANDBOX_BASE_URL
from utils.common import read_yaml_file

import streamlit as st

load_dotenv('../../.env')
current_dir = os.path.dirname(__file__)
st.write(current_dir)
SCHEMA_FILE_PATH = os.path.join('lumi', 'config', 'schema.yaml')

class ELN:
    def __init__(self,
                 eid: str,
                 base_url: str = SANDBOX_BASE_URL,
                 api_key = None):
        
        """_summary_
        """
        # try:
        self.eid = eid
        self.url = base_url + eid
        # self._headers = {'x-api-key': os.environ.get("API_KEY")}
        self._headers = {'x-api-key': api_key}
        self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        # except Exception as e:
        #     raise LumiException(e, sys)

    
    def get_columns(self)-> list:
        """_summary_

        Returns:
            list: _description_
        """
        col_names = [list(col.keys())[0] for col in schema_config['columns']]
        return col_names

    
    def get_request(self, url):
        """_summary_

        Args:
            url (_type_): _description_
        """
       
        return requests.get(url, headers = self._headers)

    
    def get_data(self, url):
        """_summary_

        Args:
            url (_type_): _description_

        Returns:
            _type_: _description_
        """

        response = self.get_request(url = url)
        if response.status_code == 200:
            # Successful request
            exp_data = response.json()
            return exp_data
        else:
            # Request was not successful
            print("Request failed with status code:", response.status_code)
    

    def get_user_details(self, response_data, columns: list, values: dict):
        """_summary_

        Args:
            response_data (_type_): _description_
            columns (list): _description_
            values (dict): _description_

        Raises:
            LumiException: _description_

        Returns:
            _type_: _description_
        """
        # try:
        logging.info('[INFO] Extracting User Information from ELN')
        # user_url = response_data.get('relationships')['createdBy']['links']['self']
        user_url = response_data['data']['relationships']['createdBy']['links']['self']
        
        user_json_data = requests.get(user_url, headers = self._headers)
        user_data = user_json_data.json().get('data')['attributes']
        col_not_found = []
        for col in columns:
            if user_data.get(col):
                values[col] = [user_data[col]]
            else:
                col_not_found.append(col)

        logging.info('[INFO] User Information extracted from ELN')
        return values, col_not_found
        
        # except Exception as e:
        #     logging.error("[ERROR] Error occurred while extarcting user information from ELN")
        #     raise LumiException(e, sys)
        
    
    def get_project_details(self, data, values: dict):
        """_summary_

        Args:
            data (_type_): _description_
            values (dict): _description_

        Raises:
            LumiException: _description_

        Returns:
            _type_: _description_
        """
        # try:
            # print(data)
        exp = self.get_data(url = data['links']['self'])
        logging.info('[INFO] Starting Project information extraction from ELN')
        col_not_found = []
        alternative_names = {'Project Code': 'Project code',
                            'Project Description': 'Project description'}
        for col in self._schema_config['columns']:
            column_name = list(col.keys())[0]

            if column_name in exp['data']['attributes']:
                values[column_name] = [exp['data']['attributes'][column_name]]
            elif column_name in exp['data']['attributes']['fields']:
                values[column_name] = [exp['data']['attributes']['fields'][column_name]['value']]
            else:
                col_not_found.append(column_name)

        for key in alternative_names.keys():
            if key in col_not_found:
                col_name = alternative_names[key]
                values[key] = [exp['data']['attributes']['fields'][col_name]['value']]

        return values, col_not_found
        # except Exception as e:
        #     logging.error("[ERROR] Error occurred while extarcting project information from ELN")
        #     raise LumiException(e, sys)

    
    def transform_json(self, original_json):
        """_summary_

        Args:
            original_json (_type_): _description_
        """
        new_json = {
        "experiment": {
            "id": original_json["eid"][0],
            "name": original_json["Name"][0],
            "projectCode": original_json["Project Code"][0],
            "projectDescription": original_json["Project Description"][0],
            "description": original_json["Description"][0],
            "function": original_json["Function"][0],
            "site": original_json["Site"][0],
            "email": original_json["email"][0],
            "firstName": original_json["firstName"][0],
            "lastName": original_json["lastName"][0],
            "state": original_json["state"][0]
        }
    }
    
        return new_json
    


    def initiate_data_extraction(self):
        values= {}
        # st.write(self._headers)
        data = self.get_data(url = self.url)
        # st.write(data)
        output, col_not_found = self.get_project_details(data= data,
                                                        values= values)
        
        # # get user details
        output, col_not_found = self.get_user_details(response_data= data, 
                                                    columns= col_not_found, 
                                                    values= values)
        
        

        
        if col_not_found:
            raise LumiException("Not all values extracted")
        else:
            lumi_json = self.transform_json(output)
            return lumi_json


# e = ELN(eid = "experiment%3A6ca193c1-ee6f-401b-bc16-6965dc8d90ae")
# data = e.initiate_data_extraction()

# print(data)