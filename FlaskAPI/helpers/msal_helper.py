import msal, os


class AuthenticationHelper:

    """
    A class used to represent helper methods for the Microsoft Authentication Library (MSAL).

    ...
    
    Attributes
    ----------

    Warnings
    ----------
        Please do not directly call the below attributes. They are only used as placeholders for MSAL management objects and
        may be set to None or not fully configured. Instead, use the get methods below to retrieve a management object for MSAL.

    _confidential_client : ConfidentialClientApplication
        A singleton to create access tokens and work with the Microsoft Authentication Library (MSAL).
    
    Methods
    -------
    get_confidential_client()
        Creates and/or returns a singleton to manage this application's use of the Microsoft Authentication Library (MSAL).

    Raises
    ------
    RuntimeError
        If this class is initialized versus using its static method.

    """
    
    _confidential_client = None

    def __init__(self):
        raise RuntimeError('Call get_confidential_client() instead')

    @staticmethod
    def get_confidential_client():
        if AuthenticationHelper._confidential_client is None:
            print('Creating new confidential client')
            #This example only uses the default memory token cache and should not be used for production
            AuthenticationHelper._confidential_client = msal.ConfidentialClientApplication(
                os.environ.get("CLIENT_ID"),
                authority=os.environ.get("AUTHORITY"),
                client_credential=os.environ.get("CLIENT_SECRET"))
        return AuthenticationHelper._confidential_client