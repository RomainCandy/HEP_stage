#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 19:22:33 2017
rajouter un check si on a atteint la limite journalière de requête
@author: romain
"""

import simplejson, urllib.request


def distanceAdresse(ori, dest):
    try:
        url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=drivingN&sensor=false".format(str(ori), str(dest))
        result= simplejson.load(urllib.request.urlopen(url))
        driving_time = result['rows'][0]['elements'][0]['duration']['value']
        return driving_time
    except IndexError :
        raise AttributeError('probleme calcul de distance entre %s et %s'%(ori,dest)+
                             " result = " + str(result))


