import os
import numpy as np

dat0 = np.zeros((1, 2**16), 'int32')
dat0[:] = np.random.normal(size=dat0.size) * 100
#dat0[:] = 100

dat0.tofile('input.bin')

os.system('./test_fs %i %i input.bin output.bin' % dat0.shape)

dat1 = np.fromfile('output.bin', 'int32').reshape(dat0.shape)

import pylab as pl
pl.plot(dat1[0][:2000])
pl.savefig('test1.png'), pl.clf()

fdat0 = np.fft.fft(dat0)
fdat1 = np.fft.fft(dat1)
f = np.fft.fftfreq(len(dat1[0])) * 15151.
s = (f > 0) * (f<400)
pl.plot(f[s], abs(fdat1[0][s] / fdat0[0][s]))
gs = (f>0) * (f<30)
G = (abs(fdat1[0][gs]**2).sum() / abs(fdat0[0][gs]**2).sum())**.5
pl.axhline(G, label=G)
pl.legend(loc='upper right')
pl.savefig('test2.png'), pl.clf()

