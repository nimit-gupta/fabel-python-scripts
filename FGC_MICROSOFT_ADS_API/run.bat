@echo off

start C:\Python310\python.exe "D:\Python_Deployments\FGC_MICROSOFT_ADS_API\microsoft_ads_fr\fr_ads.py"
timeout /t 60 /nobreak > NUL
start C:\Python310\python.exe "D:\Python_Deployments\FGC_MICROSOFT_ADS_API\microsoft_ads_ie\ie_ads.py"
timeout /t 60 /nobreak > NUL
start C:\Python310\python.exe "D:\Python_Deployments\FGC_MICROSOFT_ADS_API\microsoft_ads_uk\uk_ads.py"
timeout /t 60 /nobreak > NUL
start C:\Python310\python.exe "D:\Python_Deployments\FGC_MICROSOFT_ADS_API\microsoft_ads_all\all_ads.py"
timeout /t 60 /nobreak > NUL

@echo on