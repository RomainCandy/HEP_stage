#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 17:09:38 2018

@author: romain
"""

import xlrd
import shelve

def get_corresp(path='listedesvilles.xlsx'):
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(path)
    first_sheet = book.sheet_by_index(0)
    i = 1
    res = dict()
    while True:
        try:
            zz = first_sheet.row_values(i)
            val = zz[0]
            for key in zz[1:]:
                if not key:
                    break
                res[key] = val
        except IndexError:
            break
        i += 1
    with shelve.open('correspondance') as db:
        db['corresp'] = res
    
get_corresp()