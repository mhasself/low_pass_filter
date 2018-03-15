import os
import numpy as np

import npfilt

# On feynman, 8 threads, this settles down to 0.33 seconds per buffer.
n_chan = 1024*12
f_samp = 30000
blocks_per_second = 4  # this is to limit RAM usage...
n_samp = f_samp / blocks_per_second

print('Testing %i channels x %.2f samples per second.' % (n_chan, f_samp))

n_byte = 4
n_payload = n_chan * n_samp * n_byte

print('Creating %s samples of gaussian white noise...' % n_samp)
dat0 = np.zeros((n_chan, n_samp), 'int32')
dat0[0] = np.random.normal(scale=100, size=n_samp)

print('Broadcasting to %i channels.' % n_chan)
dat0[1:] = dat0[0:1,:]
dat1 = np.zeros((n_chan, n_samp), dat0.dtype)

print('Filtering.')
import time
t0 = time.time()
n_iter = 0
n_data = 0
while True:
    if n_iter % 100 == 0:
        print('Iter#    Time  Mean-process-time   Gigabytes/s')
    npfilt.apply_filter(dat0, dat1, 0)
    n_iter += 1
    n_data += n_payload
    dt = time.time() - t0
    if n_iter % 4 == 0:
        print('%4i %8.3f    %8.4f         %9.4f' %
              (n_iter, dt, dt * blocks_per_second / n_iter, n_data/ dt / 1e9))

