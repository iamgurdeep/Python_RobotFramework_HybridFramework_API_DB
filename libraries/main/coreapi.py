import requests
from robot.api import logger
from requests.models import Response


def CoreAPI(method:str,baseURL: str, apiEndPoint: str, headers: dict,**kwargs):
    '''
    This is Core API that can be called for any type of request method
    :param method: POST|PUT|GET|DELETE|PATCH
    :param baseURL: Base URL
    :param apiEndPoint: API END Point
    :param headers: Headers as dict
    :param kwargs: Optional parameter (body=body ,isNonPersistent = True|False,)
    :return:
    '''
    if 'isNonPersistent' in kwargs:
        value = kwargs.get('isNonPersistent')
        apiEndPoint = apiEndPoint + f"?isNonPersistent={value}"

    url = baseURL + apiEndPoint
    logger.info(msg=f"About to Execute {url} API", html=True)

    if 'body' in kwargs:
        body = kwargs.get('body')
        logger.info(msg=body,html=True)
        try:
            response: Response = requests.request(method=method,url=url, headers=headers, data=body)
            logger.info(msg=response.text, html=True)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response
    else:
        try:
            response: Response = requests.request(method=method,url=url, headers=headers)
            logger.info(msg=response.text, html=True)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response
