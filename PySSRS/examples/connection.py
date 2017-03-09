# -*- coding: utf-8 -*-

class con_data:
    
    '''
    Return the connection data
    '''
    
    _host   ='http://srvtdv2/report/ReportService2010.asmx?wsdl'
    
    _user   ='frreinert@septodont.intra.fr'
    
    _psw    ='fabrei9496'
    
    def get_data(self):
        
        return self._host, self._user, self_psw
