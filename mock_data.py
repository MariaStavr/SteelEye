from bs4 import BeautifulSoup

html_data = '''\
<result name="response" numFound="4" start="0">
  <doc>
    <str name="checksum">852b2dde71cf114289ad95ada2a4e406</str>
    <str name="download_link">zip_link1.zip</str>
    <date name="publication_date">2021-01-17T00:00:00Z</date>
    <str name="_root_">46015</str>
    <str name="id">46015</str>
    <str name="published_instrument_file_id">46015</str>
    <str name="file_name">DLTINS_20210117_01of01.zip</str>
    <str name="file_type">DLTINS</str>
    <long name="_version_">1726789400589762589</long>
    <date name="timestamp">2022-03-09T02:58:21.185Z</date></doc>
  <doc>
    <str name="checksum">3533fe597fc721ed139198503fe87910</str>
    <str name="download_link">zip_link2.zip</str>
    <date name="publication_date">2021-01-19T00:00:00Z</date>
    <str name="_root_">46051</str>
    <str name="id">46051</str>
    <str name="published_instrument_file_id">46051</str>
    <str name="file_name">DLTINS_20210119_01of02.zip</str>
    <str name="file_type">DLTINS</str>
    <long name="_version_">1726789400612831232</long>
    <date name="timestamp">2022-03-09T02:58:21.207Z</date></doc>
  <doc>
</result>
'''

bs_mock_object = BeautifulSoup(html_data, "html.parser")