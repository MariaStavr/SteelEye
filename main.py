from helpers import *

def run():
    content = get_data()
    data = create_beautifulSoup_object(content)
    link = get_zip_link(data)
    xml_path = extract_and_get_xml_path(link)
    xml_data = extract_data_from_xml(xml_path)
    export_as_csv(xml_data)

run()