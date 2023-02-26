from libraries.main.Main import Main
from robot.api.deco import not_keyword

tools = Main()
# Following Code will return dict of json requestes for all json mentioned in configuration file.
json_requests = tools.get_json_req(cfg_sheet_name='Catalog')

# ************************************************************************************
# Set all local variables in following section
#       ***** Setting json request body *****

create_catalog_json = json_requests['create_catalog_json']
update_catalog_json = json_requests['update_catalog_json']
error_val_catalog_json = json_requests['error_val_catalog_json']

