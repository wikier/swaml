# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2006 Sergio Fdez
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

import sys, os, string
import email.Utils
import time


class DateUtil:
    
    def __init__(self, date):
        self.date = date
    
    def getDay(self):
        return self.date[2]
    
    def getStringDay(self):
        day = self.getDay()
        if (day < 10):
            return ('0' + str(day))
        else:
            return str(day)
        
    def getMonth(self):
        return self.date[1]
    
    def getStringMonth(self):
        month = self.getMonth()
        if (month < 10):
            return ('0' + str(month))
        else:
            return str(month)
    
    def getShortStringMonth(self):
        shortMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return shortMonths[self.getMonth() - 1]
        
    def getLongStringMonth(self):
        longMonths = ['January', 'February', 'March', 'April', 
                       'May', 'June', 'July', 'August', 
                       'September', 'October', 'November', 'December']
        return longMonths[self.getMonth() - 1]  
    
    def getYear(self):
        return self.date[0]
    
    def getStringYear(self):
        return str(self.getYear())
    
    def getNumericFormat(self):
        return [self.getYear(), self.getMonth(), self.getDay()]  
    
    def getStringFormat(self, format='iso'):  
        year = self.getStringYear()
        month = self.getStringMonth()
        day = self.getStringDay()
        
        if(format == 'normal'):
            #normal format: day-month-year
            return day + '-' + month + '-' + year
        else:
            #iso: year-month-day
            return year + '-' + month + '-' + day
            
        

class MailDate(DateUtil):
    
    def __init__(self, date):
        self.date = email.Utils.parsedate(date)


class FileDate(DateUtil):
    """
    Utils functions for date of files
    """
    
    def __init__(self, path):
        """
        FileDate Constructor
        """
        
        self.date = time.localtime(os.stat(path)[8])

