#!/usr/bin/python
import psycopg2
import time

from configparser import ConfigParser
table_power=("CREATE TABLE power ("
        "tiempo timestamp NOT NULL,"
        "vprom float,"
        "vmediana float,"
        "vstd float,"
        "freq float,"
        "urms float,"
        "irms float,"
        "urmspoli float,"
        "irmspoli float,"
        "thdu float,"
        "thdi float,"
        "idc float,"
        "pact float,"
        "preac float,"
        "papar float,"
        "factpot float,"
        "pdesf float"
        ")")    
        
table_fliker=("CREATE TABLE fliker ("
        "tiempo timestamp NOT NULL,"
        "vprom float,"
        "vmediana float,"
        "vstd float,"
        "pst float,"
        "vrms float,"
        "irms float,"
        "rcc float,"
        "ang float"      
        ")")

def config(filename='database.ini',section='postgresql'):
    #create a parser
    parser = ConfigParser()
    #read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(' Section {0} not found in the {1} file'.format(section, filename))
    return db

def connect(commands):
    """ Connet to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connecto to the PostgreSQL server
        print('Connecting to the PostgreSQL database ...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        # execute a statemant
        #for command in commands:
        cur.execute(commands)
        
#         db_version = cur.fetchone()
#         print(db_version)
        # close the communication with the postgresql
        cur.close()
        # commit de changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def cargar():
    #

    sql = ("INSERT INTO power(tiempo,vprom,vmediana,vstd,freq,"
            "urms,irms,urmspoli,irmspoli,thdu,thdi,idc,pact,preac,"
            "papar,factpot,pdesf) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s,%s,%s,%s)")
    conn = None

    freq_av=50
    Urms_av=220
    Irms_av=1.23
    UrmsPoli_av=220.2
    IrmsPoli_av=1.24
    THD_U_av=2.3
    THD_I_av=2.4
    I_dc_av=0.02
    P_av=300
    Q_av=120
    S_av=420
    PF_av=0.9
    Pdesf_av=2.3
    stamp=time.strftime("\"%Y-%m-%d %H:%M:%S\"")
    viprom=1.2
    vimediana=1.1
    vistd=1.2
    if (freq_av>49):
        print("{\"time\":",stamp,", \"vprom\":",viprom,", \"vmediana\":",vimediana,", \"vstd\":",vistd,", \"freq\":",freq_av,
          ", \"Urms\":",Urms_av,
          ", \"Irms\":",Irms_av,
          ", \"UrmsPoli\":",UrmsPoli_av,
          ", \"IrmsPoli\":",IrmsPoli_av,
          ", \"THDu\":",THD_U_av,
          ", \"THDi\":",THD_I_av,
          ", \"IDC\":",I_dc_av,
          ", \"Pact\":",P_av,
          ", \"Preac\":",Q_av,
          ", \"Papar\":",S_av,
          ", \"FactPot\":",PF_av,
          ", \"Pdesf\":",Pdesf_av,
          "}")
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql,(stamp,viprom,vimediana,vistd,
                         freq_av,Urms_av,Irms_av,UrmsPoli_av,IrmsPoli_av,
                         THD_U_av,THD_I_av,I_dc_av,P_av,Q_av,S_av,
                         PF_av,Pdesf_av))
        conn.commit()
        cur.close()
    except (Ecveption,psycopg2.DatabaseError) as error:
        print (error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
#     connect('SELECT version()')
#     connect(table_power)
#     connect(table_fliker)
    cargar()
    
