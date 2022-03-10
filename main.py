from helpers import *

def run():
    url = 'https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100'
    data = get_data(url)
    bs_object = create_beautifulSoup_object(data)
    link = get_zip_link(bs_object)
    zip_file= get_data(link)
    xml_path = extract_and_get_xml_path(zip_file)
    xml_data = extract_data_from_xml(xml_path)
    export_as_csv(xml_data)
    upload_csvFile_to_s3()

run()
