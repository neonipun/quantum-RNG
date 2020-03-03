from tqdm import tqdm
N=10  
h={i:0 for i in range(N)} 
num_reads=10


# Tabu search is a heuristic for optimization applications 
# https://en.wikipedia.org/wiki/Tabu_search
# The ocean tools comes with a Tabu sampler that simulates the D-Wave quantum annealer on my local machine 
from tabu import TabuSampler
tabu_sampler=TabuSampler() 
print('\n----------------------------------------')
print('Running with Tabu Sampler (local simulator) 100 times')
with open('tabu_sampler_output.txt', 'w') as f:
    for _ in tqdm(range(100)):        
        samples=tabu_sampler.sample_ising(h=h, J={}, num_reads=num_reads)
        #All samples 
        for i in range(len(samples.record)):
            f.write(''.join(map(lambda x: '0' if x==-1 else str(x), samples.record[i]['sample'])))
print('Done. Generated 10000 uniform random bits in SA_sampler_output.txt')            
 

# Simulated annealing is a famous heuristic for optimization 
# https://en.wikipedia.org/wiki/Simulated_annealing
# The ocean tools comes with Simulated annealing implementation that simulates the D-Wave quantum annealer on my local computer 
import neal
SA_sampler= neal.SimulatedAnnealingSampler()
print('\n----------------------------------------')
print('Running with SA (Simulated Annealing) Sampler (local simulator) 100 times')
with open('SA_sampler_output.txt', 'w') as f:
    for _ in tqdm(range(100)):        
        samples=SA_sampler.sample_ising(h=h, J={}, num_reads=num_reads)
        #All samples 
        for i in range(len(samples.record)):
            f.write(''.join(map(lambda x: '0' if x==-1 else str(x), samples.record[i]['sample'])))
print('Done. Generated 10000 uniform random bits in SA_sampler_output.txt')
 

# To run a problem on a physical/hardware quantum annealer, you need a sampler for the quantum processing unit 
from dwave.system.samplers import DWaveSampler
# DW_2000Q_5 is the solver on D-Wave hardwarewith 2000+ qubits and about 6000 couplers   
default_solver = 'DW_2000Q_5'
my_token="TOKEN"
my_endpoint="https://cloud.dwavesys.com/sapi/"
print('\n----------------------------------------')
print('Running with D-Wave Quantum Annealer (located in Burnaby, BC, Canada) with 2000 qubits and 5 reads')
DW_sampler= DWaveSampler(token=my_token, endpoint=my_endpoint, solver=dict(name=default_solver))
qubits=DW_sampler.nodelist
h={qubits[i]:0 for i in range(2000)}
samples=DW_sampler.sample_ising(h=h, J={}, num_reads=5)
with open('DW_sampler_output.txt', 'w') as f:
    for i in range(len(samples.record)):
        f.write(''.join(map(lambda x: '0' if x==-1 else str(x), samples.record[i]['sample'])))
print('Done. Generated 10000 uniform random bits in DW_sampler_output.txt')