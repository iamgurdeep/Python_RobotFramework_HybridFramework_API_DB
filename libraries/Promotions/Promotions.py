'''
This Module will act as custom RobotFramework Library and will contain Custom Keywords -Gurdeep
'''
from robot.libraries.BuiltIn import BuiltIn

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
dblist = ValidationData['Promotion']


@library
class Promotions:
    # ****************************************************
    cfg_sheet_name = 'Promotions'
    data_sheet_name = 'Promotions'
    ####################################################

    c = DataUtil(cfg_sheet_name=cfg_sheet_name, data_sheet_name=data_sheet_name)
    c._data_mapper()

    # get token, base_url and endpoint from global variable module .
    token = global_variables.token
    base_url = global_variables.base_url


    create_promotion_api = global_variables.create_promotion_api
    update_promotion_api=global_variables.update_promotion_api
    get_promotion_by_id_api=global_variables.get_promotion_by_id
    get_promotion_by_code_api=global_variables.get_promotion_by_code
    search_promotion_api=global_variables.search_promotion
    delete_promotion_by_id_api=global_variables.delete_promotion_by_id
    change_promotion_status_api=global_variables.change_promotion_staus
    meta_extension_promotion_api=global_variables.meta_extension_promotion
    import_promotion_api=global_variables.import_promotion

    # update_tax_api = global_variables.update_tax_api
    # delete_tax_api = global_variables.delete_tax_api
    # get_tax_by_id_api = global_variables.get_tax_by_id_api
    # get_all_tax_api = global_variables.get_all_tax_api
    # get_tax_by_filters_api= global_variables.get_tax_by_filters_api


    # Set default header
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


    @keyword('Create Promotion')
    def Create_Promotion(self, request_json, **kwargs):
        response: Response = CoreAPI(method='POST', baseURL=self.base_url,
                                     apiEndPoint=self.create_promotion_api, headers=self.headers,
                                     body=request_json, **kwargs)

        return response

    @keyword('Get Promotion By Id')
    def Get_Promotion_by_id(self, id):
        get_promotion_by_id_api = self.get_promotion_by_id_api.format(id=id)
        response: Response = CoreAPI(method='GET', baseURL=self.base_url,
                                     apiEndPoint=get_promotion_by_id_api, headers=self.headers)

        return  response

    @keyword('Get Promotion By Code')
    def Get_Promotion_by_Code(self, id):
        get_promtoion_by_code_api = self.get_promotion_by_code_api.format(id=id)
        response: Response = CoreAPI(method='GET', baseURL=self.base_url,
                                     apiEndPoint=get_promtoion_by_code_api, headers=self.headers)

        return  response

    @keyword('Search Promotion')
    def Search_Promotion(self, type):
        search_promotion_api = self.search_promotion_api.format(filter=type)
        response: Response = CoreAPI(method='GET', baseURL=self.base_url,
                                     apiEndPoint=search_promotion_api, headers=self.headers)

        return response



    @keyword('Update Promotion')
    def Update_Promotion(self, request_json,promotion_id, **kwargs):
        update_promotion_api = self.update_promotion_api.format(id=promotion_id)
        request_json = json.loads(request_json)
        request_json['id'] = promotion_id
        request_json = json.dumps(request_json)
        logger.info(request_json,also_console=True)
        response: Response = CoreAPI(method='PUT', baseURL=self.base_url,
                                     apiEndPoint=update_promotion_api, headers=self.headers,
                                     body=request_json, **kwargs)


        return response



    @keyword('Delete Promotion')
    def delete_promotion(self, id, **kwargs):
       delete_promotion_by_id_api = self.delete_promotion_by_id_api.format(id=id)
       response: Response = CoreAPI(method='DELETE', baseURL=self.base_url,
                                     apiEndPoint=delete_promotion_by_id_api, headers=self.headers, **kwargs)

       return response




    @keyword('patch promotion lifecycle status')
    def patch_promotion_lifecycle_status(self, id, status, **kwargs):
        change_promotion_status_api = self.change_promotion_status_api.format(id=id)
        request_body = {
            "id": id,
            "lifecycleStatus": status,
            "notes": "Lifecycle status change"
        }
        request_json = json.dumps(request_body)
        logger.info(request_json, also_console=True)
        response: Response = CoreAPI(method='PATCH', baseURL=self.base_url,
                                     apiEndPoint=change_promotion_status_api, headers=self.headers,
                                     body=request_json, **kwargs)
        return response





    @keyword('Patch MetaExt Promotion')
    def Patch_MetaExt_Promotion(self, request_json, id):
        meta_extension_promotion_api = self.meta_extension_promotion_api.format(id=id)
        response: Response = CoreAPI(method='PATCH', baseURL=self.base_url,
                                     apiEndPoint=meta_extension_promotion_api, headers=self.headers,
                                     body=request_json)

        return response





    @keyword('Import Promotion')
    def Import_Promotion(self, request_json, **kwargs):
        response: Response = CoreAPI(method='POST', baseURL=self.base_url,
                                     apiEndPoint=self.import_promotion_api, headers=self.headers,
                                     body=request_json, **kwargs)

        return response
    
    @keyword('DB Search All')
    def DB_Search_All(self, List_Data, collection_name, id, key):
        logger.info(f"Data to check {dblist}", html=True, also_console=True)
        logger.info(List_Data, also_console=True)
        for i in range(len(dblist)):
            try:
                cursor, client = tools.get_db_data(dbname=dblist[i], collection_name=collection_name)
                db_result = cursor.find_one({id: key})
                tools.close_db_connection(client)
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