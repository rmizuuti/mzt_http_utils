import json
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from enum import Enum


# Defines the protocol to be used
class Protocol(str, Enum):
    HTTP = 'http://'
    HTTPS = 'https://'


# Defines the HTTP Method to be used
class HTTPMethod(int, Enum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3
    PATCH = 4


# Defines the arguments of the request
class RequestArgs:
    method: HTTPMethod = HTTPMethod.GET
    protocol: Protocol = Protocol.HTTP
    timeout: int = None
    url: str = None
    params: dict = None
    data: dict = None
    json_data: dict = None
    headers: dict = None


# Class to make parallel calls to HTTP APIs supporting retries
class HTTPUtils:

    # Initializes the object
    def __init__(self, pool_size=10, retries=5, backoff_factor=0.1):
        retries = Retry(total=retries, backoff_factor=backoff_factor, status_forcelist=[500, 502, 503, 504])
        self.http_adapter = HTTPAdapter(pool_connections=pool_size, max_retries=retries)
        self.executor = ThreadPoolExecutor()

    # Executes a SINGLE call, supporting retries.
    def execute(self, req_args: RequestArgs):
        try:
            session = self.__prepare_session(req_args)
            if req_args.method is HTTPMethod.GET:
                return self.__get(session, req_args)
            if req_args.method is HTTPMethod.POST:
                return self.__post(session, req_args)
            if req_args.method is HTTPMethod.PUT:
                return self.__put(session, req_args)
            if req_args.method is HTTPMethod.DELETE:
                return self.__delete(session, req_args)
            if req_args.method is HTTPMethod.PATCH:
                return self.__patch(session, req_args)
        except Exception as e:
            return json.dumps({
                'status_code': '000',
                'text': e.args
            })

    # Executes MULTIPLE calls, in parallel, each one supporting retries.
    def execute_many(self, req_arg_list):
        ret = {}
        for req_args in req_arg_list:
            future = self.executor.submit(self.execute, req_args)
            ret.update({req_args.url: future.result()})
        return json.dumps(ret)

    # Prepares the requests.Session
    def __prepare_session(self, req_args: RequestArgs):
        if req_args is None:
            raise HTTPException('RequestArgs cannot be empty')
        if req_args.url is None or req_args.url == '':
            raise HTTPException('URL cannot be empty.')
        session = requests.Session()
        session.mount(req_args.protocol, self.http_adapter)
        return session

    # Executes a HTTP GET method
    @staticmethod
    def __get(session, req_args: RequestArgs):
        try:
            response = session.get(req_args.url, params=req_args.params, headers=req_args.headers, timeout=req_args.timeout)
            return json.dumps({
                'status_code': response.status_code,
                'text': response.text
            })
        except Exception as e:
            return json.dumps({
                'status_code': 500,
                'text': "Error: {}".format(str(e))
            })

    # Executes a HTTP POST method
    @staticmethod
    def __post(session, req_args: RequestArgs):
        try:
            response = session.post(req_args.url, params=req_args.params, data=req_args.data, json=req_args.json_data, headers=req_args.headers, timeout=req_args.timeout)
            return json.dumps({
                'status_code': response.status_code,
                'text': response.text
            })
        except Exception as e:
            return json.dumps({
                'status_code': 500,
                'text': "Error: {}".format(str(e))
            })

    # Executes a HTTP PUT method
    @staticmethod
    def __put(session, req_args: RequestArgs):
        try:
            response = session.put(req_args.url, params=req_args.params, data=req_args.data, json=req_args.json_data, headers=req_args.headers, timeout=req_args.timeout)
            return json.dumps({
                'status_code': response.status_code,
                'text': response.text
            })
        except Exception as e:
            return json.dumps({
                'status_code': 500,
                'text': "Error: {}".format(str(e))
            })

    # Executes a HTTP DELETE method
    @staticmethod
    def __delete(session, req_args: RequestArgs):
        try:
            response = session.delete(req_args.url, params=req_args.params, headers=req_args.headers, timeout=req_args.timeout)
            return json.dumps({
                'status_code': response.status_code,
                'text': response.text
            })
        except Exception as e:
            return json.dumps({
                'status_code': 500,
                'text': "Error: {}".format(str(e))
            })

    # Executes a HTTP PATCH method
    @staticmethod
    def __patch(session, req_args: RequestArgs):
        try:
            response = session.patch(req_args.url, params=req_args.params, data=req_args.data, json=req_args.json_data, headers=req_args.headers, timeout=req_args.timeout)
            return json.dumps({
                'status_code': response.status_code,
                'text': response.text
            })
        except Exception as e:
            return json.dumps({
                'status_code': 500,
                'text': "Error: {}".format(str(e))
            })


class HTTPException(Exception):

    def __init__(self, message):
        self.message = message
