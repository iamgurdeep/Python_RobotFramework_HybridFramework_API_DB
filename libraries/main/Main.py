'''
This is Main Module part pf Main Package which contains Shared Methods those can be called in any HighLevel code base.
Created by Guru
Last Modified by Guru:27th May 2022
'''
from robot.api.deco import library
import pandas as pd
import json,re
import os, sys
import requests
from robot.api import logger
from pymongo import MongoClient
import yaml

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))


@library
class Main:
    '''
    Main contains all common methods that can be used as part of API automation implementation .
    Example: Reading the configuration file, Reading Data file, Reading and writing json files
    '''
    def __init__(self):
        '''
        Here it's initializing Configuration file and storing in class attribute name conf
        '''
        self.conf = os.path.join(ROOT_DIR, 'Data', 'Configurations', 'configurations.xlsx')
        self.validationyaml = os.path.join(ROOT_DIR, 'Data', 'InputData','DBValidationData.yaml')

    def read_conf(self, sheet_name: str) -> dict:
        '''
        Read the configuration sheet within the configuration file
        :param sheet_name: Sheet name to read within Configuration File
        :return: Configuration Settings in the form of Dict
        '''
        df = pd.read_excel(self.conf, sheet_name, index_col=[0])
        settings = json.loads(df.to_json())
        assert isinstance(settings, dict)
        return settings

    # def read_base_json(self, filename: str) -> dict:
    #     '''
    #     This Method will read Base Json files and returns the content of file in the form of dict
    #     :param filename: Base Json file name with full path as in String
    #     :return: dict of base json content
    #     '''
    #     data = json.load(open(filename))
    #     return data

    def read_data_file(self, datafile_name: str, sheet_name: str):
        '''
        This Method will read Data Sheet within Datafile and returns a Dict
        :param datafile_name: Data File Name to read
        :param sheet_name: Data Sheet name within Data file name to read
        :return: dict of input data from datasheet
        '''
        df = pd.read_excel(datafile_name, sheet_name=sheet_name, index_col=[0])
        df = df.fillna('')
        # input_data: dict = json.loads(df.to_json())
        return df

    def write_modified_json(self, data: dict, filename: str):
        '''
        This Method will Write dict or list of dict (with modified data) like object to given json file
        :param data: Modified dict.
        :param filename: json filename.
        :return: None
        '''
        with open(filename, "w") as write_file:
            json.dump(data, write_file, indent=2)

    def read_modified_json(self, filename):
        body = json.load(open(filename))
        # assert isinstance(body, dict)
        body = json.dumps(body)
        return body

    def get_validation_data(self):
        with open(self.validationyaml, 'r') as stream:
            out = yaml.safe_load(stream)
            return out

    # following logic will read all files marked for enable in config file
    # in createSC Sheet and will store in files_to_modify list for further processing
    def get_modified_json_files(self, cfg_sheet_name:str) -> dict:
        '''
        This Method will read api based configuration sheet within main configuration file
        and will return all the json files mentioned in configurations along with absolute path
        :param cfg_sheet_name: api based configuration sheet within main configuration file
        :return: json files in form of dict
        '''
        settings = self.read_conf(sheet_name=cfg_sheet_name)
        json_files = {}
        for key, value in settings['key_type'].items():
            if value == 'file':
                file = os.path.join(ROOT_DIR, settings['value']['modified_json_path'], settings['value'][key])
                json_files[key] = file
        return json_files

    def json_to_modify(self, cfg_sheet_name:str)->list:
        '''
        This Method will return list of json files to modify which marked as Enabled in configuration file
        :param cfg_sheet_name: api based configuration sheet within main configuration file
        :return: list of json files to modify which marked as Enabled
        '''
        settings = self.read_conf(sheet_name=cfg_sheet_name)
        json_files = []
        files_to_modify = []
        for key, value in settings['key_type'].items():
            if value == 'file':
                json_files.append(key)
        for file in json_files:
            if settings['is_enabled'][file] == 'Y':
                files_to_modify.append(file)
        return files_to_modify

    def get_json_req(self,cfg_sheet_name) -> dict:
        '''
        This Function will read all json files provided in API configuration sheet available in main
        configuration file.It will read all json file and return the dict of json file as key and json file
         content as value.
        :return:
        '''
        json_request = {}
        # Get modified json request body
        # following will fetch all json files : {dict} mentioned in Shopping cart config sheet under config doc.
        json_req_files = self.get_modified_json_files(cfg_sheet_name=cfg_sheet_name)
        # Below piece of code will read all modified jsons body and will store in dict respective to key in conf file.
        for key, value in json_req_files.items():
            json_request[key] = self.read_modified_json(filename=json_req_files[key])
        return json_request

    def test_fun(self, j_file:str, cfg_sheet_name:str):
        '''
        This Method will read the different API based config sheet present in main configuration file
        and will return the base request file, modified request file and data file along with absolute path
        :param j_file: Json File Name
        :param cfg_sheet_name: Configuration Sheet to read for specific API  within main Configuration file
        :return: Base and Modified Json along with Data file (string format)
        '''
        settings = self.read_conf(sheet_name=cfg_sheet_name)
        # base_filename = os.path.join(ROOT_DIR, settings['value']['base_requests_path'],
        #                              settings['value'][j_file])
        # print(settings['value']['data_path'], settings['value']['data_file'])
        data_file = os.path.join(ROOT_DIR, settings['value']['data_path'], settings['value']['data_file'])
        modified_file = os.path.join(ROOT_DIR, settings['value']['modified_json_path'],
                                     settings['value'][j_file])
        #return base_filename, data_file, modified_file
        return data_file, modified_file

    def get_token(self, token_url: str, headers: dict, data: dict) -> str:
        '''
        This Method will create and return the token based on provided URL and Body
        :param token_url: URL to Create Token
        :param headers: Headers
        :param data: Body of request
        :return: Token in String Format
        '''

        try:
            print('in here')
            resp = requests.post(token_url, headers=headers, data=data, timeout=10)
            print('after resp')
            json_resp = resp.json()
            token = json_resp['access_token']
            return token
        except Exception as e:
            #print(f"Not able to generate toke error: {json_resp}")
            #print(f"Not able to generate toke error: {json_resp}")
            logger.warn("Not able to generate token!! \n 1. Check Network Connection.\n 2. Check Token related Data.",html=True)
            sys.exit()



    def close_db_connection(self,client):
        client.close()

    def get_db_data(self,dbname,collection_name):
        db_settings = self.read_conf(sheet_name='global')
        try:
            db_settings = db_settings[list(db_settings)[0]]['dbconnection']
            client = MongoClient(db_settings)
            database = client[dbname]
            collection = database[collection_name]
            return collection,client
        except:
            print("Error While setting up DB or collection Connection!!")


    if __name__ == "__main__":
        print(f'direct execution of {__name__}')
    else:
        print(f"imported execution of {__name__}")
