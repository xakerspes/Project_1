from PyQt5.QtCore import QThread, pyqtSignal
from  client import ModbusClient
import pyodbc, datetime,time ,random,struct
import settings as CONST
import os
 

class DisplayThread(QThread):
    # initialize signal
    data        = pyqtSignal(object)
    exceptions  = pyqtSignal(str,object)

    def __init__(self):
        super(DisplayThread,self).__init__()

        self.SERVER_HOST       = CONST.SERVER_HOST
        self.SERVER_PORT       = CONST.SERVER_PORT
        self.register_1        = CONST.REGISTR_1
        self.register_2        = CONST.REGISTR_2
        self.count_1           = CONST.COUNT_1
        self.count_2           = CONST.COUNT_2
        self.coefficent_1      = CONST.COEFFICENT_1
        self.coefficent_2      = CONST.COEFFICENT_2
        self.time_sleep        = CONST.TIME_SLEEP
        self.path              = CONST.PATH
    
    def run(self):


        while True:
            try:
                c = ModbusClient()
                c.host(self.SERVER_HOST)
                c.port(self.SERVER_PORT)
                drivers = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
                if drivers!=[]:
                    for driver in drivers:
                        if driver == 'Microsoft Access Driver (*.mdb, *.accdb)':
                            driver_param = '{Microsoft Access Driver (*.mdb, *.accdb)}'
                        elif driver == 'Microsoft Access Driver (*.mdb)':
                            driver_param = '{Microsoft Access Driver (*.mdb)}'
                else:
                    print("No find  Microsoft Access Driver")
                    self.exceptions.emit("No find  Microsoft Access Driver", 'Error')
                    continue

                DB = self.path
                conn_str = (
                    r'DRIVER=' + driver_param + ';'
                    r'DBQ='+ DB +';')
                
                try:
                    conn = pyodbc.connect(conn_str,autocommit=True)
                    while True:
                        crsor = conn.cursor()
                        if not c.is_open():
                            if not c.open():
                                print("unable to connect to "+self.SERVER_HOST+":"+str(self.SERVER_PORT))

                        if c.is_open():

                            regs_1      = c.read_holding_registers(self.register_1,self.count_1)[0] * self.coefficent_1
                            regs_2      = c.read_holding_registers(self.register_2,self.count_2)[0] * self.coefficent_2
                       
                            time_now    = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        # random_num  = random.random()*100
                        # sql  =     "INSERT INTO rasxod ( time_record, skorost_rasxod, summ_rasxod ) VALUES ('{}', {:.5f},{:.5f});".format(time_now,random_num,random_num)
                
                        
                            if (regs_1 and regs_2):
                                sql  =     "INSERT INTO rasxod ( time_record, skorost_rasxod, summ_rasxod ) VALUES ('{}', {:.5f},{:.5f});".format(time_now,regs_1,regs_2)
                            else:
                                if   (regs_1):
                                    sql  = "INSERT INTO rasxod ( time_record, skorost_rasxod ) VALUES ('{}', {:.5f});".format(time_now,regs_1)
                                elif (regs_2):
                                    sql  = "INSERT INTO rasxod ( time_record,    summ_rasxod ) VALUES ('{}', {:.5f});".format(time_now,regs_2)

                            crsor.execute(sql)
                            rows = crsor.execute("SELECT *  FROM rasxod  WHERE ID=(SELECT MAX(ID) FROM rasxod);" )
                            for row in rows:
                                print(row)
                                self.data.emit(row)
                            crsor.close()
                        time.sleep(self.time_sleep)#pereriv v zaprosax

                except pyodbc.Error as e:
                    print('2-try Exception',e)
                    self.exceptions.emit('2-try Exception',e)
                    time.sleep(self.time_sleep)


            except Exception as e:
                print('1-try Exception',e)
                self.exceptions.emit('1-try Exception',e)
                conn.close()
                time.sleep(self.time_sleep )