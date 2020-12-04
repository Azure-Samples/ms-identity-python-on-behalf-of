from requests import Session, adapters
from urllib3.util.retry import Retry

class RequestsHelper:
    """
    A class used to represent helper methods for session objects.

    ...
    
    Attributes
    ----------

    Warnings
    ----------
        Please do not directly call the below attributes. They are only used as placeholders for session objects and
        may be set to None or not fully configured. Instead, use the get methods below to retrieve session objects.

    _discovery_key_session : Session
        A singleton that represents a session object to create requests with. 
    
    Methods
    -------
    get_discovery_key_session()
        Creates and/or returns a singleton that represents a session object to create requests with.

    Raises
    ------
    RuntimeError
        If this class is initialized versus using its static method.

    """
    
    _discovery_key_session = None

    def __init__(self):
        raise RuntimeError('Call get_discovery_key_session instead')

    @staticmethod
    def get_discovery_key_session():
        if RequestsHelper._discovery_key_session is None:
            print('Creating new requests session')      
            session = Session()
            retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
            session.mount('https://', adapters.HTTPAdapter(max_retries=retries))
            session.mount('http://', adapters.HTTPAdapter(max_retries=retries))
            RequestsHelper._discovery_key_session = session

        return RequestsHelper._discovery_key_session