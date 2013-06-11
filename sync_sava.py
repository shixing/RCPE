import sys
import os

para = sys.argv[1]
para_recv = '/'.join(para.split('/')[:-1])+'/'
cmd = 'scp %s xingshi@sava.usc.edu:~/workspace/rcpe/%s' % (para,para_recv)
print cmd
os.system(cmd)
