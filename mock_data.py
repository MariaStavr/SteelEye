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


xml_data = '''\
<FinInstrm xmlns="urn:iso:std:iso:20022:tech:xsd:auth.036.001.02">
  <TermntdRcrd>
    <FinInstrmGnlAttrbts>
      <Id>DE000A1R07V3</Id>
      <FullNm>KFW 1 5/8 01/15/21</FullNm>
      <ShrtNm>KFW/1.625 ANL 20210115 GGAR</ShrtNm>
      <ClssfctnTp>DBFTFB</ClssfctnTp>
      <NtnlCcy>EUR</NtnlCcy>
      <CmmdtyDerivInd>false</CmmdtyDerivInd>
    </FinInstrmGnlAttrbts>
    <Issr>549300GDPG70E3MBBU98</Issr>
    <TradgVnRltdAttrbts>
      <Id>XEUM</Id>
      <IssrReq>false</IssrReq>
      <FrstTradDt>2014-01-15T06:00:00Z</FrstTradDt>
      <TermntnDt>2020-12-30T23:59:59Z</TermntnDt>
    </TradgVnRltdAttrbts>
    <DebtInstrmAttrbts>
      <TtlIssdNmnlAmt Ccy="EUR">5000000000</TtlIssdNmnlAmt>
      <MtrtyDt>2021-01-15</MtrtyDt>
      <NmnlValPerUnit Ccy="EUR">1000</NmnlValPerUnit>
      <IntrstRate><Fxd>1.625</Fxd></IntrstRate>
    </DebtInstrmAttrbts>
    <TechAttrbts>
      <RlvntCmptntAuthrty>DE</RlvntCmptntAuthrty>
      <RlvntTradgVn>MANL</RlvntTradgVn>
    </TechAttrbts>
  </TermntdRcrd>
</FinInstrm>
'''
