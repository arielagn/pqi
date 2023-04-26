from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import time
import pqi
import anemometro
import flicker

s=pqi.pqi(12)
s.setW()

d=s.sendCom('sendV',6000)
#time.sleep(10)
#d=s.sendCom('getVI',6000)
print(d)