#!/usr/bin/python
import psycopg2
import time

from configparser import ConfigParser
table_armonics=("CREATE TABLE armonics ("
        "tiempo timestamp NOT NULL,"
        "vprom float,"
        "vmediana float,"
        "vstd float,"
        "v1 float,v2 float,v3 float,v4 float,v5 float,v6 float,v7 float,v8 float,v9 float,v10 float,"
        "v11 float,v12 float,v13 float,v14 float,v15 float,v16 float,v17 float,v18 float,v19 float,v20 float,"
        "v21 float,v22 float,v23 float,v24 float,v25 float,v26 float,v27 float,v28 float,v29 float,v30 float,"
        "v31 float,v32 float,v33 float,v34 float,v35 float,v36 float,v37 float,v38 float,v39 float,v40 float,"
        "v41 float,v42 float,v43 float,v44 float,v45 float,v46 float,v47 float,v48 float,v49 float,v50 float,"
        "i1 float,i2 float,i3 float,i4 float,i5 float,i6 float,i7 float,i8 float,i9 float,i10 float,"
        "i11 float,i12 float,i13 float,i14 float,i15 float,i16 float,i17 float,i18 float,i19 float,i20 float,"
        "i21 float,i22 float,i23 float,i24 float,i25 float,i26 float,i27 float,i28 float,i29 float,i30 float,"
        "i31 float,i32 float,i33 float,i34 float,i35 float,i36 float,i37 float,i38 float,i39 float,i40 float,"
        "i41 float,i42 float,i43 float,i44 float,i45 float,i46 float,i47 float,i48 float,i49 float,i50 float,"
        "si1 float,si2 float,si3 float,si4 float,si5 float,si6 float,si7 float,si8 float,si9 float,si10 float,"
        "si11 float,si12 float,si13 float,si14 float,si15 float,si16 float,si17 float,si18 float,si19 float,si20 float,"
        "si21 float,si22 float,si23 float,si24 float,si25 float,si26 float,si27 float,si28 float,si29 float,si30 float,"
        "si31 float,si32 float,si33 float,si34 float,si35 float,si36 float,si37 float,si38 float,si39 float,si40 float,"
        "si41 float,si42 float,si43 float,si44 float,si45 float,si46 float,si47 float,si48 float,si49 float,si50 float,"
        "idc float,"
        "papar float,"
        "pact float,"
        "preac float,"
        "thc float,"        
        "turms float,"
        "tudc float,"
        "tirms float,"
        "tidc float"
        ")")

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
        
table_flicker=("CREATE TABLE flicker ("
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

def config(filename='/home/pi/Documents/pqi/database.ini',section='postgresql'):
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

def cargar2():
    #

    sql = ("INSERT INTO armonics(tiempo,vprom,vmediana,vstd,"
            "v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,"
            "v21,v22,v23,v24,v25,v26,v27,v28,v29,v30,v31,v32,v33,v34,v35,v36,v37,v38,v39,v40,"
            "v41,v42,v43,v44,v45,v46,v47,v48,v49,v50,"
            "i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,i14,i15,i16,i17,i18,i19,i20,"
            "i21,i22,i23,i24,i25,i26,i27,i28,i29,i30,i31,i32,i33,i34,i35,i36,i37,i38,i39,i40,"
            "i41,i42,i43,i44,i45,i46,i47,i48,i49,i50,"
            "si1,si2,si3,si4,si5,si6,si7,si8,si9,si10,si11,si12,si13,si14,si15,si16,si17,si18,si19,si20,"
            "si21,si22,si23,si24,si25,si26,si27,si28,si29,si30,si31,si32,si33,si34,si35,si36,si37,si38,si39,si40,"
            "si41,si42,si43,si44,si45,si46,si47,si48,si49,si50,"
            "idc,papar,pact,preac,thc,turms,tudc,tirms,tidc"
            ") VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
            "%s,%s,%s)")
    
    conn = None
    stamp=time.strftime("\"%Y-%m-%d %H:%M:%S\"")
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql,(stamp,12.3,12.3,12.2,
                         1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
                         21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
                         41,42,43,44,45,46,47,48,49,50,
                         1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
                         21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
                         41,42,43,44,45,46,47,48,49,50,
                         1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
                         21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
                         41,42,43,44,45,46,47,48,49,50,
                         1,2,3,4,5,6,7,8,9))
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
#   connect(table_armonics)
    cargar2()
    
