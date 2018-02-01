import os
import numpy as np

import npfilt

# On feynman, 8 threads, this settles down to 0.33 seconds per buffer.
n_chan = 1024*6
n_samp = 30000

print 'Creating %s samples of gaussian white noise...' % n_samp
dat0 = np.zeros((n_chan, n_samp), 'int32')
dat0[0] = np.random.normal(scale=100, size=(n_samp))

print 'Broadcasting to %i channels.' % n_chan
dat0[1:] = dat0[0:1,:]
dat1 = np.zeros((n_chan, n_samp), dat0.dtype)

print 'Filtering.'
import time
t0 = time.time()
n_iter = 0
while True:
    npfilt.apply_filter(dat0, dat1, 0)
    n_iter += 1
    dt = time.time() - t0
    print n_iter, dt, dt/n_iter

