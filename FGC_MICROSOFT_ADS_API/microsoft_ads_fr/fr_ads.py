from auth_helper import *
from bingads.v13.reporting import *
import pandas as pd 
from IPython.core.display import display
import sqlalchemy


REPORT_FILE_FORMAT='Csv'


FILE_DIRECTORY='D:/Python_Deployments/FGC_MICROSOFT_ADS_API/microsoft_ads_fr'


RESULT_FILE_NAME='ads_fr.' + REPORT_FILE_FORMAT.lower()


TIMEOUT_IN_MILLISECONDS=3600000

def main(authorization_data):

    try:
        report_request=get_report_request(authorization_data.account_id)

        
        
        reporting_download_parameters = ReportingDownloadParameters(
                                                                        report_request=report_request,
                                                                        result_file_directory = FILE_DIRECTORY, 
                                                                        result_file_name = RESULT_FILE_NAME, 
                                                                        overwrite_result_file = True, 
                                                                        timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS 
                                                                   )

        
        print("-----\nAwaiting download_report......")

        download_report(reporting_download_parameters)

    except WebFault as ex:
        print(ex)
    except Exception as ex:
        print(ex)

def background_completion(reporting_download_parameters):
    
    global reporting_service_manager

    result_file_path = reporting_service_manager.download_file(reporting_download_parameters)

    print("Download result file: {0}".format(result_file_path))

def submit_and_download(report_request):
    
    global reporting_service_manager

    reporting_download_operation = reporting_service_manager.submit_download(report_request)

    reporting_operation_status = reporting_download_operation.track(timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS)

    result_file_path = reporting_download_operation.download_result_file(
                                                                         result_file_directory = FILE_DIRECTORY, 
                                                                         result_file_name = RESULT_FILE_NAME, 
                                                                         decompress = True, 
                                                                         overwrite = True,  
                                                                         timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS 
                                                                        )
    
    print("Download result file: {0}".format(result_file_path))

def download_results(request_id, authorization_data):
     
    reporting_download_operation = ReportingDownloadOperation(
                                                               request_id = request_id, 
                                                               authorization_data=authorization_data, 
                                                               poll_interval_in_milliseconds=1000, 
                                                               environment=ENVIRONMENT,
                                                             )

  
    reporting_operation_status = reporting_download_operation.track(timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS)
    
    result_file_path = reporting_download_operation.download_result_file(
                                                                            result_file_directory = FILE_DIRECTORY, 
                                                                            result_file_name = RESULT_FILE_NAME, 
                                                                            decompress = True, 
                                                                            overwrite = True, 
                                                                            timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS 
                                                                        ) 

    print("Download result file: {0}".format(result_file_path))

    print("Status: {0}".format(reporting_operation_status.status))

def download_report(reporting_download_parameters):
    
    global reporting_service_manager

    report_container = reporting_service_manager.download_report(reporting_download_parameters)
 
    display(report_container.report_columns)

    time_period = [ ]    
    impressions = [ ]
    clicks = [ ]
    spend = [ ]
    ctr = [ ]
    averagecpc = [ ]
    conversions = [ ]
    costperconversion = [ ]
    revenue = [ ]
    cr = []

    for record in report_container.report_records:
        time_period.append(record.value("TimePeriod"))
        impressions.append(record.int_value("Impressions"))
        clicks.append(record.int_value("Clicks"))
        spend.append(record.float_value("Spend"))
        ctr.append(record.value("Ctr"))
        averagecpc.append(record.float_value("AverageCpc"))
        conversions.append(record.float_value("Conversions"))
        costperconversion.append(record.float_value("CostPerConversion"))
        revenue.append(record.value("Revenue"))
        cr.append(record.value("ConversionRate"))
        
    df = pd.DataFrame({
                        "Time Period":time_period, 
                        "Impressions":impressions,
                        "Clicks":clicks,
                        "CTR" : ctr,
                        "AVG_CPC" : averagecpc,
                        "Spend":spend,
                        "Conversions":conversions,
                        "CPC":costperconversion,
                        "Conversion_Rate": cr,
                        "Revenue": revenue
                       
                      })

    display(df)

    engine = sqlalchemy.create_engine(f"mssql+pymssql://DevUser3:flgT!9585@217.174.248.77:3689/feelgood.reports")

    con = engine.connect() 

    table_name = 'fgc_fr_mads'

    df.to_sql(table_name, con, if_exists = 'append', method = 'multi', chunksize = 10000, index = False)

def get_report_request(account_id):
    
    aggregation = 'Daily'
    exclude_column_headers=False
    exclude_report_footer=False
    exclude_report_header=False
    time=reporting_service.factory.create('ReportTime')
    time.CustomDateRangeStart = None
    time.CustomDateRangeEnd = None
    time.PredefinedTime='Yesterday'
    time.ReportTimeZone='GreenwichMeanTimeDublinEdinburghLisbonLondon'
    return_only_complete_data=False

    campaign_performance_report_request=get_campaign_performance_report_request(
                                                                                account_id=account_id,
                                                                                aggregation=aggregation,
                                                                                exclude_column_headers=exclude_column_headers,
                                                                                exclude_report_footer=exclude_report_footer,
                                                                                exclude_report_header=exclude_report_header,
                                                                                report_file_format=REPORT_FILE_FORMAT,
                                                                                return_only_complete_data=return_only_complete_data,
                                                                                time=time
                                                                               )

   
    return campaign_performance_report_request

def get_campaign_performance_report_request(
                                             account_id,
                                             aggregation,
                                             exclude_column_headers,
                                             exclude_report_footer,
                                             exclude_report_header,
                                             report_file_format,
                                             return_only_complete_data,
                                             time):

    report_request=reporting_service.factory.create('CampaignPerformanceReportRequest')
    report_request.Aggregation=aggregation
    report_request.ExcludeColumnHeaders=exclude_column_headers
    report_request.ExcludeReportFooter=exclude_report_footer
    report_request.ExcludeReportHeader=exclude_report_header
    report_request.Format=report_file_format
    report_request.ReturnOnlyCompleteData=return_only_complete_data
    report_request.Time=time    
    report_request.ReportName="My Campaign Performance Report"
    scope=reporting_service.factory.create('AccountThroughCampaignReportScope')
    scope.AccountIds={'long': [account_id] }
    scope.Campaigns=None
    report_request.Scope=scope     

    report_columns=reporting_service.factory.create('ArrayOfCampaignPerformanceReportColumn')
    report_columns.CampaignPerformanceReportColumn.append([
                                                            'TimePeriod',
                                                            'Impressions',
                                                            'Clicks',  
                                                            'Spend',
                                                            'Ctr',
                                                            'AverageCpc',
                                                            'Conversions',
                                                            'CostPerConversion',
                                                            'Revenue',
                                                            'ConversionRate'
                                                           ])
    report_request.Columns=report_columns

    return report_request

if __name__ == '__main__':

    print("...Loading the web service client proxies...")

    authorization_data=AuthorizationData(
                                            account_id=None,
                                            customer_id=None,
                                            developer_token=DEVELOPER_TOKEN,
                                            authentication=None,
                                        )

    reporting_service_manager=ReportingServiceManager(
                                                        authorization_data=authorization_data, 
                                                        poll_interval_in_milliseconds=5000, 
                                                        environment=ENVIRONMENT,
                                                     )

    
    reporting_service=ServiceClient(
                                    service='ReportingService', 
                                    version=13,
                                    authorization_data=authorization_data, 
                                    environment=ENVIRONMENT,
                                   )

    authenticate(authorization_data)
        
    main(authorization_data)