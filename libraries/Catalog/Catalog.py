'''
This Module will act as custom RobotFramework Library and will contain Custom Keywords related to
Create ShoppingCart
'''

from libraries.main.Main import Main
from libraries.main.DataUtil import DataUtil
from libraries.main import global_variables
from libraries.main.coreapi import CoreAPI

from robot.api.deco import keyword, library
from robot.api import logger

from requests import Response
import json

# Initialize Main module's  class to access all its shared methods
tools = Main()
ValidationData = tools.get_validation_data()
dblist = ValidationData['Catalog']



@library
class Catalog:
    # ****************************************************
    cfg_sheet_name = 'Catalog'
    data_sheet_name = 'Catalog'
    ####################################################

    c = DataUtil(cfg_sheet_name=cfg_sheet_name, data_sheet_name=data_sheet_name)
    c._data_mapper()

    # get token, base_url and endpoint from global variable module .
    token = global_variables.token
    base_url = global_variables.base_url


    create_catalog_api = global_variables.create_catalog_api
    delete_catalog_api = global_variables.delete_catalog_api
    patch_catalog_lifecyclestatus_api = global_variables.patch_catalog_lifecyclestatus_api

    Get_Catalog_api = global_variables.Get_Catalog
    Get_Catalog_Id = global_variables.Get_Catalog_Id
    Get_Catalog_Code = global_variables.Get_Catalog_Code
    Get_Catalog_Name = global_variables.Get_Catalog_Name
    Get_Catalog_Type = global_variables.Get_Catalog_Type
    Get_Catalog_Search = global_variables.Get_Catalog_Search

    # Set default header
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


    @keyword('Create Catalog')
    def Create_Catalog(self, request_json,catalogType, **kwargs):
        request_json = json.loads(request_json)
        request_json['catalogType'] = catalogType
        request_json = json.dumps(request_json)
        response: Response = CoreAPI(method='POST', baseURL=self.base_url,
                                     apiEndPoint=self.create_catalog_api, headers=self.headers,
                                     body=request_json, **kwargs)

        return response


    @keyword('Update Catalog')
    def Update_Catalog(self, request_json,catalogType,id,**kwargs):
        request_json = json.loads(request_json)
        request_json['catalogType'] = catalogType
        request_json['id'] = id
        request_json = json.dumps(request_json)
        response: Response = CoreAPI(method='PUT', baseURL=self.base_url,
                                     apiEndPoint=self.create_catalog_api, headers=self.headers,
                                     body=request_json, **kwargs)

        return response

    @keyword('Delete Catalog')
    def Delete_Catalog(self, id):
        delete_catalog_api = self.delete_catalog_api.format(id=id)
        response: Response = CoreAPI(method='DELETE', baseURL=self.base_url,
                                     apiEndPoint=delete_catalog_api, headers=self.headers)

        return response

    @keyword('Patch Update LifeCycleStatus Catalog')
    def Patch_Update_LifeCycleStatus_Catalog(self, id, status, **kwargs):
        patch_catalog_lifecyclestatus_api = self.patch_catalog_lifecyclestatus_api.format(id=id)
        request_body = {
            "id": id,
            "lifecycleStatus": status,
            "notes": "Lifecycle status change"
        }
        request_json = json.dumps(request_body)
        # logger.info(request_json,also_console=True)
        response: Response = CoreAPI(method='PATCH', baseURL=self.base_url,
                                     apiEndPoint=patch_catalog_lifecyclestatus_api, headers=self.headers,
                                     body=request_json, **kwargs)

        return response


    @keyword('DB Search Catalog by Key')
    def DB_search_catalog(self, id, dbname, collection_name, key):
        tools = Main()
        try:
            cursor, client = tools.get_db_data(dbname=dbname, collection_name=collection_name)
            logger.info(f'checking {id} in DB ', html=True, also_console=True)
            category = cursor.find_one({key: id})
            # logger.info(recommendation,also_console=True)
            tools.close_db_connection(client)
            if category:
                logger.info(f'Data Found :{category} in DB ', html=True, also_console=True)
            else:
                logger.error("Category not found")
            return category
        except:
            logger.error("Unable to connect with Database", html=True)


    @keyword('Get Catalog')
    def Get_Catalog(self):
        response: Response = CoreAPI(method='GET', baseURL=self.base_url,
                                     apiEndPoint=self.Get_Catalog_api, headers=self.headers)

        return response


    @keyword('Get Catalog by ID')
    def Get_Catalog_by_ID(self,id):
        Get_Catalog_Id_api = self.Get_Catalog_Id.format(id=id)
        response: Response = CoreAPI(method='GET', baseURL=self.base_url,
                                     apiEndPoint=Get_Catalog_Id_api, headers=self.headers)

        return response

    @keyword('Get Catalog by Code')
    def Get_Catalog_by_Code(self,Code):
        Get_Catalog_Code = self.Get_Catalog_Code.format(code=Code)
        response: Response = CoreAPI(method='GET', baseURL=self.base_url,
                                     apiEndPoint=Get_Catalog_Code, headers=self.headers)

        return response

    @keyword('Get Catalog by Name')
    def Get_Catalog_by_name(self,Name):
        Get_Catalog_Name_api = self.Get_Catalog_Name.format(name=Name)
        response: Response = CoreAPI(method='GET', baseURL=self.base_url,
                                     apiEndPoint=Get_Catalog_Name_api, headers=self.headers)

        return response

    @keyword('Get Catalog by Type')
    def Get_Catalog_by_Type(self,type):
        Get_Catalog_Type_api = self.Get_Catalog_Type.format(type=type)
        response: Response = CoreAPI(method='GET', baseURL=self.base_url,
                                     apiEndPoint=Get_Catalog_Type_api, headers=self.headers)

        return response

    @keyword('Get Catalog Search')
    def Search_Catalog(self):
        response: Response = CoreAPI(method='GET', baseURL=self.base_url,
                                     apiEndPoint=self.Get_Catalog_Search, headers=self.headers)

        return response

    @keyword('DB Search All')
    def DB_Serach_All(self, List_Data, collection_name, id, key):
        dblist = ValidationData['Catalog']
        logger.info(f"Data to check {dblist}", html=True, also_console=True)
        logger.info(List_Data, also_console=True)
        for i in range(len(dblist)):
            try:
                cursor, client = tools.get_db_data(dbname=dblist[i], collection_name=collection_name)
                db_result = cursor.find_one({id: key})
                tools.close_db_connection(client)
                # logger.info(db_result,also_console=True)
                if db_result:
                    for j in range(len(List_Data)):
                        if List_Data[j] in db_result.values():
                            logger.info(f'{List_Data[j]} found for in {dblist[i]} in DB', html=True, also_console=True)
                        else:
                            logger.error(f'{List_Data[j]} not found in {dblist[i]} in DB')
                            continue
                else:
                    logger.error(f'Data not found in {dblist[i]} in DB')
            except:
                logger.error("Unable to connect with Database", html=True)