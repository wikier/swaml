# -*- coding: utf8 -*-

# SWAML <http://swaml.berlios.de/>
# Semantic Web Archive of Mailing Lists
#
# Copyright (C) 2005-2007 Sergio Fernández
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

"""Utils functions to work with dates"""

import sys, os, string
import email.Utils
import time
import logging

class Date:
    
    def __init__(self, date):
        """
        Date constructor
        """
        
        self.date = date
    
    def getDay(self):
        """
        Get day value
        """
        
        return self.date[2]
    
    def getStringDay(self):
        """
        Get day as string
        """
        
        day = self.getDay()
        if (day < 10):
            return ('0' + str(day))
        else:
            return str(day)
        
    def getMonth(self):
        """
        Get month value
        """
        
        return self.date[1]
    
    def getStringMonth(self):
        """
        Get month in string number format
        """
        
        month = self.getMonth()
        if (month < 10):
            return ('0' + str(month))
        else:
            return str(month)
    
    def getShortStringMonth(self):
        """
        Get month in short string format
        """
        
        shortMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return shortMonths[self.getMonth() - 1]
        
    def getLongStringMonth(self):
        """
        Get month in long string format
        """        
        
        longMonths = ['January', 'February', 'March', 'April', 
                       'May', 'June', 'July', 'August', 
                       'September', 'October', 'November', 'December']
        return longMonths[self.getMonth() - 1]  
    
    def getYear(self):
        """
        Get year value
        """
        
        return self.date[0]
    
    def getStringYear(self):
        """
        Get year string
        """
        
        return str(self.getYear())
    
    def getNumericFormat(self):
        """
        Get int values
        """
        
        return [self.getYear(), self.getMonth(), self.getDay()]  
    
    def getInteger(self):
        """
        Get long int value
        """
        
        return (self.date[0]*10000000000 + self.date[1]*100000000 + 
                self.date[2]*1000000 + self.date[3]*10000 + 
                self.date[4]*100 + self.date[5])
    
    def getStringFormat(self, format='iso'):  
        """
        Get string format
        
        @param format: standar
        """
        
        year = self.getStringYear()
        month = self.getStringMonth()
        day = self.getStringDay()
        
        if(format == 'normal'):
            #normal format: day-month-year
            return day + '-' + month + '-' + year
        else:
            #iso: year-month-day
            return year + '-' + month + '-' + day
            
        

class MailDate(Date):
    """
    Utils functions for date of emails
    """
        
    def __init__(self, date):
        """
        MailDate constructor
        """
        
        self.date = email.Utils.parsedate(date)

	if (self.date == None):
		logging.error('Error parsing none date, trying alternatives...')
		#trying another format: dd.mm.yyyy
		try:		
			tmp = date.split('.')
			self.date = (int(tmp[2]), int(tmp[1]), int(tmp[0]),
				 	0, 0, 0, 0, 1, -1)
		except:
			self.date = (1970, 1, 1, 0, 0, 0, 0, 1, -1)


class FileDate(Date):
    """
    Utils functions for date of files
    """
    
    def __init__(self, path):
        """
        FileDate constructor
        """
        
        self.date = time.localtime(os.stat(path)[8])

