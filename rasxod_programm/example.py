from  client import ModbusClient
import pyodbc, datetime,time ,random,struct
import settings as CONST


SERVER_HOST         = CONST.SERVER_HOST
SERVER_PORT         = CONST.SERVER_PORT
__register_1        = CONST.REGISTR_1
__register_2        = CONST.REGISTR_2
__count_1           = CONST.COUNT_1
__count_2           = CONST.COUNT_2
__coefficent_1      = CONST.COEFFICENT_1
__coefficent_2      = CONST.COEFFICENT_2
__time_sleep        = CONST.TIME_SLEEP
__path              = CONST.PATH
__time_sleep		= CONST.TIME_SLEEP

def sleeping(a=None):
    if a :
        time.sleep(a)
    else:
        time.sleep(__time_sleep)
while True:
    try:
        c = ModbusClient()
        c.host(SERVER_HOST)
        c.port(SERVER_PORT)
        drivers = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
        if drivers!=[]:
            for driver in drivers:
                if driver == 'Microsoft Access Driver (*.mdb, *.accdb)':
                    driver_param = '{Microsoft Access Driver (*.mdb, *.accdb)}'
                elif driver == 'Microsoft Access Driver (*.mdb)':
                    driver_param = '{Microsoft Access Driver (*.mdb)}'
        else:
            print("No find  Microsoft Access Driver")
            continue

        DB = __path
        conn_str = (
            r'DRIVER=' + driver_param + ';'
            r'DBQ='+ DB +';')
        
        try:
            conn = pyodbc.connect(conn_str,autocommit=True)
            while True:
                crsor = conn.cursor()
                # open or reconnect TCP to server
                if not c.is_open():
                    if not c.open():
                        print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))

                if c.is_open():

                    regs_1      = c.read_holding_registers(__register_1,__count_1)[0] * __coefficent_1
                    regs_2      = c.read_holding_registers(__register_2,__count_2)[0] * __coefficent_2
                    time_now    = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    print(regs_1)
                    random_num  = random.random()*100

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
                    crsor.close()
                    
                sleeping()
        except pyodbc.Error as e:
	        print('2-try Exception',e)

    except Exception as e:
        print('1-try Exception',e)
        conn.close()

        sleeping()


 