#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import SSRS

import connection as con

RS = PySSRS.SSRS(host=con._host, user=con._user, key_password=con._psw)

result = RS.Find(SearchConditions='Qualidade')

print(result)