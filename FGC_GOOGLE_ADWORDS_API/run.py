#! /usr/bin/env python
#-*-coding:utf-8-*-

from google.ads.googleads.client import GoogleAdsClient
import uk_ads as uk
import ie_ads as ie
import fr_ads as fr
import all_ads as all

client = GoogleAdsClient.load_from_storage('D:/Python_Deployments/FGC_GOOGLE_ADWORDS_API/google_ads.yml')

def run():

    uk.main(client, '8799359331')

    ie.main(client, '6393751578')

    fr.main(client, '6534362080')

    all.read_query()

if __name__ == '__main__':
    run()