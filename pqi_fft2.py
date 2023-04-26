import pqi_serial
import numpy as np
import time
import anedig2
import psycopg2
from psycopg2.extensions import register_adapter, AsIs

from test_dbconn import config

s=pqi_serial.pqi_serial('/dev/ttyACM0')
#ane=anedig2.aneDig(60)
stamp=time.strftime("\"%Y-%m-%d %H:%M:%S\"")
#viprom,vimediana,vistd=ane.start()
viprom=12.2
vimediana=23.3
vistd=33.3
f=s.pqi_rp_fft()
#print(len(f))
def addapt_numpy_float32(numpy_float32):
    return AsIs(numpy_float32)
register_adapter(np.float32, addapt_numpy_float32)




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

try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute(sql,(stamp,viprom,vimediana,vistd,
            f[0],f[1],f[2],f[3],f[4],f[5],f[6],f[7],f[8],f[9],f[10],f[11],f[12],f[13],f[14],f[15],f[16],f[17],f[18],f[19],
            f[20],f[21],f[22],f[23],f[24],f[25],f[26],f[27],f[28],f[29],f[30],f[31],f[32],f[33],f[34],f[35],f[36],f[37],f[38],f[39],
            f[40],f[41],f[42],f[43],f[44],f[45],f[46],f[47],f[48],f[49],f[50],f[51],f[52],f[53],f[54],f[55],f[56],f[57],f[58],f[59],
            f[60],f[61],f[62],f[63],f[64],f[65],f[66],f[67],f[68],f[69],f[70],f[71],f[72],f[73],f[74],f[75],f[76],f[77],f[78],f[79],
            f[80],f[81],f[82],f[83],f[84],f[85],f[86],f[87],f[88],f[89],f[90],f[91],f[92],f[93],f[94],f[95],f[96],f[97],f[98],f[99],
            f[100],f[101],f[102],f[103],f[104],f[105],f[106],f[107],f[108],f[109],f[110],f[111],f[112],f[113],f[114],f[115],f[116],f[117],f[118],f[119],
            f[120],f[121],f[122],f[123],f[124],f[125],f[126],f[127],f[128],f[129],f[130],f[131],f[132],f[133],f[134],f[135],f[136],f[137],f[138],f[139],
            f[140],f[141],f[142],f[143],f[144],f[145],f[146],f[147],f[148],f[149],f[150],f[151],f[152],f[153],f[154],f[155],f[156],f[157],f[158]))
                         
    conn.commit()
    cur.close()
except (Exception,psycopg2.DatabaseError) as error:
    print (error)
finally:
    if conn is not None:
        conn.close()
print("{\"time\":",stamp,", \"vprom\":",viprom,", \"vmediana\":",vimediana,", \"vstd\":",vistd, 
      ", \"Urms\":",f[155],
      ", \"Udc\":",f[156],
      ", \"Irms\":",f[157],
      ", \"IDC\":",f[158],
      ", \"Papar\":",f[151],
      ", \"Pact\":",f[152],
      ", \"Preac\":",f[153],
      ", \"THC\":",f[154],
      "}")