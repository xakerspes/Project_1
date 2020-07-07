# -*- coding: utf-8 -*-
SERVER_HOST         = "87.237.237.252"
SERVER_PORT         = 2468
TIME_SLEEP          = 1     	# zaderjda v sekundax
##########################################################
REGISTR_1           = 0x00  	# address registr
COUNT_1             = 0x02     	# size registr 
COEFFICENT_1		= 1			# Exmp: rasxod = 100*1 = 100
REGISTR_2           = 0x08  	# address registr
COUNT_2             = 0x02      # size registr 
COEFFICENT_2		= 0.001		# Exmp: rasxod = 100*1 = 100
###################   DATABASE PARAMETRS          #########################
PATH				= 'C:\\Users\\Apple\\Desktop\\v4.0.32\\rasxod_programm\\Database2.mdb' #PATH file Database MS ACCESS
TABLE_NAME			= 'rasxod'
COLUMNS_NAME		= ['ID','time_record','skorost_rasxod','summ_rasxod'] 
					# counter, datetime,    float, 			float

