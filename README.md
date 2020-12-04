---
page_type: sample
languages:
- python
products:
- azure-active-directory
description: "This sample demonstrates a Python web application calling a Python web API that then calls the Azure Management API subscriptions endpoint. The web application and API are secured using Azure Active Directory."
urlFragment: ms-identity-python-on-behalf-of
---
# Microsoft identity platform and OAuth 2.0 On-Behalf-Of flow in Python

### Overview

This repository contains a sample solution that demonstrates how to implement the OAuth 2.0 On-behalf-of flow using the Microsoft Authentication Library (MSAL) for Python. 

### Scenario

This sample solution contains two applications, a UI developed using the Django framework and an API developed using the Flask framework. The UI signs a user in and acquires an access token to call the API using MSAL. Once called, the API uses MSAL to acquire another access token and acceses the Azure Management API's subscription endpoint.

For more information on how this flow works, please refer to either [Microsoft identity platform and OAuth 2.0 On-Behalf-Of flow](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow) or [Scenario: A web API that calls web APIs](https://docs.microsoft.com/en-us/azure/active-directory/develop/scenario-web-api-call-api-overview).

## Prerequisites

> - [Python 2.7+](https://www.python.org/downloads/release/python-2713/) or [Python 3+](https://www.python.org/downloads/release/python-364/)
> - An Azure Active Directory (Azure AD) tenant. For more information on how to get an Azure AD tenant, see [how to get an Azure AD tenant.](https://docs.microsoft.com/azure/active-directory/develop/quickstart-create-new-tenant)
> - Configure [VS Code](https://code.visualstudio.com/docs/python/python-tutorial) for debugging Python applications


### Step 1:  Clone or download this repository

From your shell or command line:

```Shell
git clone https://github.com/Azure-Samples/ms-identity-python-on-behalf-of.git
```

or download and extract the repository .zip file.

> TIP: To avoid path length limitations on Windows, you may need to clone into a directory with a shorter name or near the root of your drive.

### Step 2:  Register the sample application with your Azure Active Directory tenant

Follow the [Register the application and service in Azure AD](https://github.com/MicrosoftDocs/azure-docs/blob/master/articles/active-directory/azuread-dev/v1-oauth2-on-behalf-of-flow.md#register-the-application-and-service-in-azure-ad) section in the Azure Docs to create and configure app registrations in Azure Active Directory for the UI and API applications.

* Ensure the property [accessTokenAcceptedVersion](https://docs.microsoft.com/en-us/azure/active-directory/develop/reference-app-manifest?WT.mc_id=Portal-Microsoft_AAD_RegisteredApps#accesstokenacceptedversion-attribute) has been updated, in both app registration manifests, to have a value of **2**.

>NOTE! Only use the [Register the application and service in Azure AD](https://github.com/MicrosoftDocs/azure-docs/blob/master/articles/active-directory/azuread-dev/v1-oauth2-on-behalf-of-flow.md#register-the-application-and-service-in-azure-ad) section for configuring the required app registrations in Azure Active Directory from step 1. For examples and further reference, please use the [Microsoft Identity platform](https://github.com/MicrosoftDocs/azure-docs/blob/master/articles/active-directory/develop/v2-oauth2-on-behalf-of-flow.md) documentation instead.

### Step 3: Create the required development.env files for both applications

- Use the production.env files in both applications to create local, development.env, files for each application. 
### Step 4: Run the sample

1. You will need to install dependencies using pip

    * The below shell commands must be executed in both applications as they both have seperate requirements.txt files  
    * There is also Pipfile included in both applications if you prefer to use pipenv instead


For the Flask API application, use the following command: 
```Shell
$ pip install -r requirements.txt
```

For the Django UI application, local execution only, use the following command: 
```Shell
$ pip install -r dev-requirements.txt
```


2. Select the Python interpreter for <a href="https://code.visualstudio.com/docs/languages/python">VS Code</a> to use and start the [debugger](https://code.visualstudio.com/docs/editor/debugging).
    * For this sample, each application will need to be opened in a seperate VS Code instance.
> NOTE! The default ports used for the Django UI and Flask API applications will be 8000 and 5000.


## Community Help and Support

Use [Stack Overflow](http://stackoverflow.com/questions/tagged/msal) to get support from the community.
Ask your questions on Stack Overflow first and browse existing issues to see if someone has asked your question before.
Make sure that your questions or comments are tagged with [`azure-active-directory` `adal` `msal` `python`].

If you find a bug in the sample, please raise the issue on [GitHub Issues](../../issues).

To provide a recommendation, visit the following [User Voice page](https://feedback.azure.com/forums/169401-azure-active-directory).

## Contributing

If you'd like to contribute to this sample, see [CONTRIBUTING.MD](/CONTRIBUTING.md).

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information, see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## More information

For more information, see MSAL.Python's [conceptual documentation]("https://github.com/AzureAD/microsoft-authentication-library-for-python/wiki"):

For more information on how this flow works in this scenario, please see either 
see [Microsoft identity platform and OAuth 2.0 On-Behalf-Of flow](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-on-behalf-of-flow) or [Scenario: A web API that calls web APIs](https://docs.microsoft.com/en-us/azure/active-directory/develop/scenario-web-api-call-api-overview).

For more information about how OAuth 2.0 protocols work in this scenario and other scenarios, see [Authentication Scenarios for Azure AD](http://go.microsoft.com/fwlink/?LinkId=394414).