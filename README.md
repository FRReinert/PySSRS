# PySSRS
Microsoft Reporting Services (SSRS) RPC trough SOAP

## Installation
You just need to run ```pip install PySSRS```

### Connecting to SSRS
You can use it as a facilitator to make SOAP RPCs.
For example:
```python

From SSRS import SSRS

RS = SSRS('localhost', 'user@domain.com', '@paswd2017')
result = RS.client.service.ListChildren(dir, recursive)

for item in result.CatalogItem:
  print(item['Name'])
```

### Available Functions
We implemented some functions to make it easy to use. Feel free to check their usage on the  **samples** folder.

These functions are available by now:

Function      | Objective                      | Return Type
--------------|--------------------------------|------------
ListMethods() | List all SOAP procedures | List []
DirItems() | List all objects in a directory | Dictionary {}
Find() | Find for a item by it's name | Dictionary {}
GetParameters() | Return all parameters from a Report object | Dictionary {}

### Snippet

Check this small code, it's an sample of usage

```python
# Conneting to SSRS SOAP server

wsdl = 'http://localhost/ReportinServices/ReportService2010.asmx?wsdl'
user = 'user@domain.com
psw  = '@password2017'

RS = SSRS(wsdl, user, psw)

'''
Return a LIST with all available SOAP procedures
so you can iterate over them...
'''
Methods = RS.ListMethods()

'''
Return a DICTIONARY with all items in a specific folder
you can also use the <recursive> parameter to scan subfolders.
If you don't specify the <dir> parameter it'll take the root ('/') as default
'''
DirItems = RS.ListDirItems(dir='/MyReports', recursive=True)

'''
Find() will retrieve a list of items which the name matches with the <text> parameter.
It's recursive, you don't need to specify any folder and you can also specify the object type that you want
by using the <objtype> parameter.

Those are the accepted types of objects
            -> Component 
            -> DataSource 
            -> Folder
            -> Model
            -> LinkedReport
            -> Report
            -> Resource
            -> DataSet
            -> Site
            -> Unknown
'''
ItemsFound = RS.Find(text="Sales", objtype="Report")

#GetParameters() will retrieve a list of paremeters for the report on the specific path
Parameters = RS.GetParameters(path='/MyReports/SalesOrder')
```
