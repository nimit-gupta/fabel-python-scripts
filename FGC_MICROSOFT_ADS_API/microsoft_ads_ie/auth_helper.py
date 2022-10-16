import sys
import webbrowser
from time import gmtime, strftime
from suds import WebFault

from bingads.service_client import ServiceClient
from bingads.authorization import *
from bingads.v13 import *

DEVELOPER_TOKEN='105O2Z4YO7165081' 

ENVIRONMENT='production' 

CLIENT_ID='c8524334-3217-4193-ba33-735faf0b8261'

CLIENT_STATE='ClientStateGoesHere'

REFRESH_TOKEN = r"D:\Python_Deployments\FGC_MICROSOFT_ADS_API\microsoft_ads_ie\refresh_ie.txt"

ALL_CAMPAIGN_TYPES=['Audience Search Shopping']

ALL_TARGET_CAMPAIGN_CRITERION_TYPES=['Age DayTime Device Gender Location LocationIntent Radius']

ALL_TARGET_AD_GROUP_CRITERION_TYPES=['Age DayTime Device Gender Location LocationIntent Radius']

ALL_AD_TYPES={
              'AdType': ['AppInstall', 'DynamicSearch', 'ExpandedText', 'Product', 'ResponsiveAd', 'ResponsiveSearchAd', 'Text']
             }

def authenticate(authorization_data):
    
    customer_service=ServiceClient(
                                    service='CustomerManagementService', 
                                    version=13,
                                    authorization_data=authorization_data, 
                                    environment=ENVIRONMENT,
                                  )

    authenticate_with_oauth(authorization_data)
        
    user=get_user_response=customer_service.GetUser(
                                                    UserId=None
                                                   ).User
    accounts=search_accounts_by_user_id(customer_service, user.Id)
    
    # For this example we'll use the first account.
    authorization_data.account_id=accounts['AdvertiserAccount'][2].Id
    authorization_data.customer_id=accounts['AdvertiserAccount'][2].ParentCustomerId
 
def authenticate_with_oauth(authorization_data):
    
    authentication=OAuthDesktopMobileAuthCodeGrant(
        client_id=CLIENT_ID,
        env=ENVIRONMENT
    )
 
    authentication.state=CLIENT_STATE

    authorization_data.authentication=authentication   

    authorization_data.authentication.token_refreshed_callback=save_refresh_token
    
    refresh_token=get_refresh_token()
    
    try:
        
        if refresh_token is not None:
            authorization_data.authentication.request_oauth_tokens_by_refresh_token(refresh_token)
        else:
            request_user_consent(authorization_data)
    except OAuthTokenRequestException:
           request_user_consent(authorization_data)
            
def request_user_consent(authorization_data):

    webbrowser.open(authorization_data.authentication.get_authorization_endpoint(), new=1)
    
    if(sys.version_info.major >= 3):
        response_uri=input(
                            "You need to provide consent for the application to access your Bing Ads accounts. " \
                            "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
                            "please enter the response URI that includes the authorization 'code' parameter: \n"
                          )
    else:
        response_uri=input(
                            "You need to provide consent for the application to access your Bing Ads accounts. " \
                            "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
                            "please enter the response URI that includes the authorization 'code' parameter: \n"
                          )

    if authorization_data.authentication.state != CLIENT_STATE:
       raise Exception("The OAuth response state does not match the client request state.")

    authorization_data.authentication.request_oauth_tokens_by_response_uri(response_uri=response_uri) 

def get_refresh_token():
    
    file=None

    try:

        file=open(REFRESH_TOKEN)
        line=file.readline()
        file.close()
        return line if line else None

    except IOError:

        if file:
            file.close()
        return None

def save_refresh_token(oauth_tokens):
    
    with open(REFRESH_TOKEN,"w+") as file:
        file.write(oauth_tokens.refresh_token)
        file.close()
    return None

def search_accounts_by_user_id(customer_service, user_id):
    
    predicates={
        'Predicate': [
            {
                'Field': 'UserId',
                'Operator': 'Equals',
                'Value': user_id,
            },
        ]
    }

    accounts=[]

    page_index = 0
    PAGE_SIZE=100
    found_last_page = False

    while (not found_last_page):
        paging=set_elements_to_none(customer_service.factory.create('ns5:Paging'))
        paging.Index=page_index
        paging.Size=PAGE_SIZE
        search_accounts_response = customer_service.SearchAccounts(
            PageInfo=paging,
            Predicates=predicates
        )
        
        if search_accounts_response is not None and hasattr(search_accounts_response, 'AdvertiserAccount'):
            accounts.extend(search_accounts_response['AdvertiserAccount'])
            found_last_page = PAGE_SIZE > len(search_accounts_response['AdvertiserAccount'])
            page_index += 1
        else:
            found_last_page=True
    
    return {
        'AdvertiserAccount': accounts
    }

def set_elements_to_none(suds_object):
    
    for (element) in suds_object:
        suds_object.__setitem__(element[0], None)
    return suds_object

def set_read_only_campaign_elements_to_none(campaign):
    
    if campaign is not None:
        campaign.CampaignType=None
        campaign.Settings=None
        campaign.Status=None

def set_read_only_ad_extension_elements_to_none(extension):

    if extension is None or extension.Id is None:
        return extension
    else:
        
        extension.Version = None
    
        if extension.Type == 'LocationAdExtension':
            extension.GeoCodeStatus = None
        
        return extension