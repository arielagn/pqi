import time

freq_av=50
Urms_av=220
Irms_av=2.3456543
UrmsPoli_av=220.2
IrmsPoli_av=2.353456677
THD_U_av=1
THD_I_av=1
I_dc_av=1
P_av=1
Q_av=1
S_av=1
PF_av=1
Pdesf_av=1
stamp=time.strftime("\"%Y-%m-%d %H:%M:%S\"")
viprom=1.2
vimediana=1.1
vistd=1.2
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
