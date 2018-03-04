from inout import *
import time
start_time = time.time()

sim = read('b_should_be_easy.in')
score = sim.daniel_simulate()
write(sim)

elapsed_time = time.time() - start_time

print('time:',elapsed_time)
print('score:',score)
input()
