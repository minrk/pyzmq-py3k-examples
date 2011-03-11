"""A test that subscribes to NumPy arrays.

Currently the timing of this example is not accurate as it depends on the
subscriber and publisher being started at exactly the same moment. We should
use a REQ/REP side channel to synchronize the two processes at the beginning.
"""

#
#    Copyright (c) 2010 Brian E. Granger
#
#    This file is part of pyzmq.
#
#    pyzmq is free software; you can redistribute it and/or modify it under
#    the terms of the Lesser GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    pyzmq is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    Lesser GNU General Public License for more details.
#
#    You should have received a copy of the Lesser GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import time

import zmq
import numpy

def main():
    if len (sys.argv) != 3:
        print ('usage: subscriber <connect_to> <array-count>')
        sys.exit (1)

    try:
        connect_to = sys.argv[1]
        array_count = int (sys.argv[2])
    except (ValueError, OverflowError):
        print ('array-count must be integers')
        sys.exit (1)

    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect(connect_to)
    print ("   Done.")
    s.setsockopt(zmq.SUBSCRIBE,b'')

    start = time.clock()

    print ("Receiving arrays...")
    for i in range(array_count):
        a = s.recv_pyobj()
    print ("   Done.")

    end = time.clock()

    elapsed = (end - start) * 1000000
    if elapsed == 0:
    	elapsed = 1
    throughput = (1000000.0 * float (array_count)) / float (elapsed)
    message_size = a.nbytes
    megabits = float (throughput * message_size * 8) / 1000000

    print ("message size: %.0f [B]" % (message_size, ))
    print ("array count: %.0f" % (array_count, ))
    print ("mean throughput: %.0f [msg/s]" % (throughput, ))
    print ("mean throughput: %.3f [Mb/s]" % (megabits, ))

if __name__ == "__main__":
    main()
