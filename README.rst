What this is
============

This code implements a low-pass filter similar to the MCE's
(e-mode.phas.ubc.ca/mcewiki) 4-poll readout filter.  This should be a
very good imitation aside from the use of 8-bit based datatypes
(int32_t and int64_t) instead of the tailored accumulators in MCE
firmware.


Running the test
----------------

To generate the transfer function plots:

  make test

To run the timing test (which passes data through numpy C interface):

  make test_np
  python test_np_filt.py

The output from the numpy test is like this::

  Testing 12288 channels x 30000.00 samples per second.
  Creating 7500 samples of gaussian white noise...
  Broadcasting to 12288 channels.
  Filtering.
  Iter#    Time  Mean-process-time   Gigasamples/s
     4    0.966      0.9657            1.5270
     8    1.804      0.9019            1.6350
    12    2.634      0.8780            1.6795
    16    3.466      0.8664            1.7019
    20    4.291      0.8582            1.7183

The effectiveness is given by the "Mean process time" -- it tells you
how long, in seconds, it takes to process 1 second of data.  These
results (0.9s) show that my old dual-core (ht) AMD can just barely
keep up with this data volume.

