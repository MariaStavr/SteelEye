import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import zipfile
import io
import logging
import boto3

logging.basicConfig(filename='log_data.log', level=logging.INFO)

csv_name='csv_data.csv'

def get_data(url):
    '''
    Returns content from the get request.

    Parameters:
        url(str): string containing url.

    Returns:
        data(string): content present in the request response.

    '''
    try:
        response = requests.get(url)
        data = response.content
        logging.info('Data retrieved successfully from: {}'.format(url))
        return data

    except Exception as ex:
        logging.info('Cannot retrieve data, exception: {}'.format(ex))
        raise ex
    

def create_beautifulSoup_object(content):
    '''
    Returns data as beautiful soup object.

    Parameters:
        content (str):string containing data.

    Returns:
        soup: The beautiful soup object containg the data.

    '''
    try:
        soup = BeautifulSoup(content, 'html.parser')
        logging.info('Beautiful soup object created successfully')
        return soup

    except Exception as ex:
        logging.info('Data could not be parsed, exception: {}'.format(ex))
        raise ex

def get_zip_link(data):
    '''
    Looks for all file types equal to 'DLTINS' and return the download link of the first one.

    Parameters:
        data (object):The beautiful soup object containg the data.

    Returns:
        zip_url(str):The string which contains the zip file url.   
    '''

    try:
        fileTypes_list = data.find_all(attrs={'name':'file_type'})
        fileTypeDLTINS=[]
        for file in fileTypes_list:
            if file.get_text() == 'DLTINS':
                fileTypeDLTINS.append(file)

        firstElement = fileTypeDLTINS[0].parent
        firstElementLink = firstElement.find(attrs={'name':'download_link'})
        zip_url=firstElementLink.get_text()
        logging.info('Zip file URL: {}'.format(zip_url))
        return zip_url

    except Exception as ex:
        logging.info('Data is not in the correct format, exception: {}'.format(ex))
        raise ex

def extract_and_get_xml_path(zipData):
    '''
    Extracts the zip file and returns the absolute path of the xml file present in the zip.

    Parameters:
        zipData (zipFile): Zip file containing data.

    Returns:
        abs_path(str):The string which contains the absolute path of the xml inside the zip file.   
    '''
    try:
        z = zipfile.ZipFile(io.BytesIO(zipData))
        z.extractall()
        xml_filename = z.namelist()[0]
        
        abs_path = os.path.abspath(xml_filename)
        logging.info('Absolute path of the first file present in the zip file: {}'.format(abs_path))
        return abs_path

    except Exception as ex:
        logging.info('Something went wrong with the zip file, exception: {}'.format(ex))
        raise ex

def extract_data_from_xml(path):
    '''
    Extracts the required data from the xml file.

    Parameters:
        path (string):The string containing the path for the xml file.

    Returns:
        data(list):List with the required data extracted from the xml.   
    '''
    try:
        with open(path, 'r',encoding="utf8" ) as file:
            xml_content=file.read()
        soup = BeautifulSoup(xml_content, "xml")
        data = [[values.find('Id').getText(),values.FinInstrmGnlAttrbts.find('FullNm').getText(), values.FinInstrmGnlAttrbts.find('ClssfctnTp').getText(), values.FinInstrmGnlAttrbts.find('CmmdtyDerivInd').getText(),values.FinInstrmGnlAttrbts.find('NtnlCcy').getText(), values.find('Issr').getText() ]for values in soup.find_all('TermntdRcrd')]
        logging.info('Data extracted from XML file')
        return data

    except Exception as ex:
        logging.info('Data in xml file is not in the correct format, exception: {}'.format(ex))
        raise ex

def export_as_csv(data):
    '''
    Exports the xml data into a csv file.

    Parameters:
        data (list):list containing the xml data.
  
    '''
    try:
        df = pd.DataFrame(data, columns=['id', 'fullname','ClssfctnTp','CmmdtyDerivInd', 'NtnlCcy', 'Issr' ])
        dir_path = os.path.dirname(os.path.realpath(__file__))
        df.to_csv(dir_path + "/" + csv_name, index=False)
        logging.info('csv file created')

    except Exception as ex:
        logging.info('Something went wrong creating the csv file, exception: {}'.format(ex))
        raise ex 
    
def upload_csvFile_to_s3():
    '''
    Uploads csv file to s3.

    '''
    s3_resource = boto3.resource("s3")
    s3 = boto3.client("s3")

    try:
        bucket_list=[]

        for bucket in s3_resource.buckets.all():
            bucket_list.append(bucket)

        s3.upload_file(
        Filename=csv_name,
        Bucket=bucket_list[0].name,
        Key=csv_name,
        )
        logging.info('csv file uploaded to s3')

    except Exception as ex:
        logging.info('cannot upload data to s3, exception: {}'.format(ex))
        raise ex