# Here you will intilize your json to use in robot file-Gurdeep
from libraries.main.Main import Main
from robot.api.deco import not_keyword

tools = Main()
# Following Code will return dict of json requestes for all json mentioned in configuration file.
json_requests = tools.get_json_req(cfg_sheet_name='Promotions')

# ************************************************************************************
# Set all local variables in following section
#       ***** Setting json request body *****

Create_Promotion_json = json_requests['Create_Promotion_json']
Update_Promotion_json = json_requests['Update_Promotion_json']

