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

    _backend_api_session : Session
        A singleton that represents a session object to create requests with. 
        This session object will be created with the needed Authorization headers to call the Flask API.
    
    Methods
    -------
    get_backend_api_session(username, correlation_id, session)
        Creates and/or returns a singleton that represents a session object to create requests with.

    Raises
    ------
    RuntimeError
        If this class is initialized versus using its static method.

    """
    
    _backend_api_session = None

    def __init__(self):
        raise RuntimeError('Call get_backend_api_session instead')

    @staticmethod
    def get_backend_api_session(token_response):
        """
        Creates and/or returns a singleton that represents a session object to create requests with. 
        This session object will be created with the needed Authorization headers to call the Flask API.

        Parameters
        ----------
        token_response : dict, required
            Dictionary containing the access token and token type to use in the Authorization header for this session object.

        Returns
        -------
        Session
            A singleton that represents a session object to create requests with.

        """
        if RequestsHelper._backend_api_session is None:
            print('Creating new requests session')      
            session = Session()
            retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
            session.mount('https://', adapters.HTTPAdapter(max_retries=retries))
            session.mount('http://', adapters.HTTPAdapter(max_retries=retries))
            RequestsHelper._backend_api_session = session

        RequestsHelper._backend_api_session.headers= {'Authorization': token_response['token_type'] + ' ' + token_response['access_token']}
        return RequestsHelper._backend_api_session