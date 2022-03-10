import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import zipfile
import io
import logging

logging.basicConfig(filename='log_data.log', level= logging.DEBUG)

def get_data():
    '''
    Returns content from the get request.

    Returns:
    data(string): content present in the request response.

    '''
    try:
        url = 'https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100'
        response = requests.get(url)
        #if response.ok:
        data = response.content
        return data

    except requests.exceptions.Timeout:
        return 'Bad response'
    

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
        print(soup)
        return soup

    except (RuntimeError, TypeError, NameError):
        print('asdads')

def get_zip_link(data):
    '''
    Looks for all file types equal to 'DLTINS' and return the download link of the first one.

    Parameters:
        data (object):The beautiful soup object containg the data.

    Returns:
        zip_url(str):The string which contains the zip file url.   
    '''

    fileTypes_list = data.find_all(attrs={'name':'file_type'})
    fileTypeDLTINS=[]
    for file in fileTypes_list:
        if file.get_text() == 'DLTINS':
            fileTypeDLTINS.append(file)

    firstElement = fileTypeDLTINS[0].parent
    firstElementLink = firstElement.find(attrs={'name':'download_link'})
    zip_url=firstElementLink.get_text()
    return zip_url

def extract_and_get_xml_path(url):
    '''
    Extracts the zip file and returns the absolute path of the xml file present in the zip.

    Parameters:
        url (string):The string containing the zip file url.

    Returns:
        abs_path(str):The string which contains the absolute path of the xml inside the zip file.   
    '''

    zipData = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(zipData.content))
    z.extractall()
    xml_filename = z.namelist()[0]
    
    abs_path = os.path.abspath(xml_filename)
    return abs_path

def extract_data_from_xml(path):
    '''
    Extracts the required data from the xml file.

    Parameters:
        path (string):The string containing the path for the xml file.

    Returns:
        data(list):List with the required data extracted from the xml.   
    '''

    with open(path, 'r',encoding="utf8" ) as file:
        xml_content=file.read()
    soup = BeautifulSoup(xml_content, "xml")
    data = [[values.find('Id').getText(),values.FinInstrmGnlAttrbts.find('FullNm').getText(), values.FinInstrmGnlAttrbts.find('ClssfctnTp').getText(), values.FinInstrmGnlAttrbts.find('CmmdtyDerivInd').getText(),values.FinInstrmGnlAttrbts.find('NtnlCcy').getText(), values.find('Issr').getText() ]for values in soup.find_all('TermntdRcrd')]
    return data

def export_as_csv(data):
    '''
    Exports the xml data into a csv file.

    Parameters:
        data (list):list containing the xml data.
  
    '''
    
    df = pd.DataFrame(data, columns=['id', 'fullname','ClssfctnTp','CmmdtyDerivInd', 'NtnlCcy', 'Issr' ])
    dir_path = os.path.dirname(os.path.realpath(__file__))
    df.to_csv(dir_path + "/csv_data.csv", index=False)
