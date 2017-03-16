#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connection_data as d
import context
from SSRS import SSRS

RS      = SSRS(d._service, d._execution, d._user, d._psw)
result  = RS.GetParameters('/Qualidade/Indice de Conformidade')

print(
        '''
        Get Parameters linked to a specific report.
        
        Available Parameters:
                ParameterTypeName
                Nullable
                AllowBlank      
                MultiValue      
                QueryParameter  
                Prompt       
                PromptUser
                ValidValuesQueryBased
                DefaultValuesQueryBased
        '''
    )

for key, value in result.items() :
    print('Name:', key)
    
    for key2, value2 in value.items():
        print(key2,':', value2)
    
    print('\n')