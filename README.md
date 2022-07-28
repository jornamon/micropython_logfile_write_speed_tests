# Write to file speed tests for data logging in micropython

These are some test designed to learn which method is more favorable for writing data to a file in micropython while not introducing long and blocking delays when the system is flushing data to the file.

This is important in data logging applications where sampling rate is relatively high and should be as stable as possible. The long delays introduced by file writes can perturb significantly the sampling period and thus should be avoided.

A little bit more explanation about the results can be found here:
https://forum.micropython.org/viewtopic.php?f=18&t=4725&start=10#p69069

If you are interested in this, you should read the whole thread, as it is very interesting and contains the information that got me started.

The queue implementation was taken from [jaycosaur](https://github.com/jaycosaur):
https://github.com/jaycosaur/micropython-queue

The RamDisk code was taken from micropython official documentation.
