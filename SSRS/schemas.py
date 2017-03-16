# -*- coding: utf-8 -*-


xml_Execute_Report_Parameter = '''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:rep="http://schemas.microsoft.com/sqlserver/2005/06/30/reporting/reportingservices">
   <soapenv:Header>
      <rep:ExecutionHeader>
         <rep:ExecutionID>{0}</rep:ExecutionID>
      </rep:ExecutionHeader>
   </soapenv:Header>
   <soapenv:Body>
      <rep:SetExecutionParameters>
         <rep:Parameters>
        {1}
         </rep:Parameters>
         <rep:ParameterLanguage>en-US</rep:ParameterLanguage>
      </rep:SetExecutionParameters>
   </soapenv:Body>
</soapenv:Envelope>
'''


xml_Render_Report ='''<soapenv:Envelope 
xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:rep="http://schemas.microsoft.com/sqlserver/2005/06/30/reporting/reportingservices">
<soapenv:Header>
<rep:ExecutionHeader>
<rep:ExecutionID>{0}</rep:ExecutionID>
</rep:ExecutionHeader>
</soapenv:Header>
<soapenv:Body>
<rep:Render>
<rep:Format>{1}</rep:Format>
</rep:Render>
</soapenv:Body>
</soapenv:Envelope>'''