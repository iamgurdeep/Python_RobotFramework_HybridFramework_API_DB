# To be used to declare global level variables like get Enpoints from Config Excel, Token genration  -Gurdeep
from libraries.main.Main import Main
from robot.api.deco import not_keyword


tools = Main()

@not_keyword
def MyToken():
    '''
    This function reads global sheet which contains base url and token related information
    :return: It will return newly generated token and application base url
    '''
    global_settings = tools.read_conf(sheet_name='global')
    global_settings = global_settings[list(global_settings)[0]]
    token_url = global_settings['token_url']
    app_url = global_settings['api_base_url']
    headers = {"content-type": "application/x-www-form-urlencoded", "Accept-Charset": "UTF-8"}
    admin_data = dict(client_id=global_settings['client_id'], client_secret=global_settings['client_secret'],
                username=global_settings['admin_username'],
                password=global_settings['admin_password'], scope=global_settings['scope'],
                grant_type=global_settings['grant_type'])
    anonymous_data = dict(client_id=global_settings['client_id'], client_secret=global_settings['client_secret'],
                      username=global_settings['anonymous_username'],
                      password=global_settings['anonymous_password'], scope=global_settings['scope'],
                      grant_type=global_settings['grant_type'])
    customer_data = dict(client_id=global_settings['client_id'], client_secret=global_settings['client_secret'],
                      username=global_settings['customer_username'],
                      password=global_settings['customer_password'], scope=global_settings['scope'],
                      grant_type=global_settings['grant_type'])
    admin_token = tools.get_token(token_url=token_url, headers=headers, data=admin_data)
    anonymous_token = tools.get_token(token_url=token_url, headers=headers, data=anonymous_data)
    customer_token = tools.get_token(token_url=token_url, headers=headers, data=customer_data)

    return admin_token, app_url


@not_keyword
def ExtraTokens(user_type='anonymous'):
    '''
    This function reads global sheet which contains base url and token related information
    :return: It will return newly generated anonymous and customer tokens respectifully and application base url
    '''
    assert user_type in ['anonymous', 'customer'], 'user_type type parameter must be anonymous or customer'
    global_settings = tools.read_conf(sheet_name='global')
    global_settings = global_settings[list(global_settings)[0]]
    token_url = global_settings['token_url']
    app_url = global_settings['api_base_url']
    headers = {"content-type": "application/x-www-form-urlencoded", "Accept-Charset": "UTF-8"}
    data = dict(client_id=global_settings['client_id'], client_secret=global_settings['client_secret'],
                          username=global_settings[f'{user_type}_username'],
                          password=global_settings[f'{user_type}_password'], scope=global_settings['scope'],
                          grant_type=global_settings['grant_type'])

    token = tools.get_token(token_url=token_url, headers=headers, data=data)
    return token

@not_keyword
def ApiEndPoints() -> dict:
    '''
    Reads all the end points mentioned in end points sheet within main configuration file
    :return: All Application end points in dictionary
    '''
    api_end_points = tools.read_conf(sheet_name='endpoints')
    api_end_points = api_end_points[list(api_end_points)[0]]
    return api_end_points

# Below section will be used to set global variables

token, base_url = MyToken() # setting up token and base url variables
anonymous_token = ExtraTokens(user_type='anonymous')
customer_token = ExtraTokens(user_type='customer')
####################################################################################



# setting up all api end points variables
# Note ** --> Add All API points here in try section
all_api = ApiEndPoints()
try:

    create_new_api = all_api['create_new']
    create_category_api = all_api['create_category']



except KeyError as e:
    print(f"Key {e} not found in Configuration Excl's Endpoint worksheet")


# print(f'Admin Token is {token}')
# print(f'Anonymous Token is {anonymous_token}')
# print(f'Customer Token is {customer_token}')


