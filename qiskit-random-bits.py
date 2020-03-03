import qiskit
from qiskit import IBMQ
import math
from tqdm import tqdm

tempBits = ''

# This is the circuit that generates uniform random bits in Quantum gate model
def get_nqubit_circuit(n):
    qr = qiskit.QuantumRegister(n)
    cr = qiskit.ClassicalRegister(n)
    circuit = qiskit.QuantumCircuit(qr, cr)
    circuit.h(qr) # Apply Hadamard gate to qubits
    circuit.measure(qr,cr) # Collapses qubit to either 1 or 0 w/ equal prob.
    return circuit

def get_n_random_bits(n, circuit, backend):
    global tempBits
    if len(tempBits) < n:
        iterations = math.ceil(n/circuit.width()*2)
        for _ in tqdm(range(iterations)):
            # Create new job and run the quantum circuit
            job = qiskit.execute(circuit, backend, shots=1)
            tempBits += list(job.result().get_counts())[0]
    randomBits = tempBits[0:n]
    tempBits = tempBits[n:]
    return randomBits

if __name__ == "__main__":
    print('\n----------------------------------------')
    print('Running IBM Q local simulator - Aer')
    backend = qiskit.Aer.get_backend('qasm_simulator')
    circuit = get_nqubit_circuit(8)
    with open('qiskit_local_output.txt', 'w') as f:
        f.write(get_n_random_bits(10000, circuit, backend))
    print('Done. Generated 10000 uniform random bits in qiskit_local_output.txt')

    print('\n----------------------------------------')
    print('Running IBM Q remote simulator - ibmq_qasm_simulator')
    token = 'TOKEN'
    IBMQ.save_account(token)
    IBMQ.load_account()
    provider = IBMQ.get_provider('ibm-q')
    backend = provider.get_backend('ibmq_qasm_simulator')
    circuit = get_nqubit_circuit(12)
    with open('qiskit_ibmq_qasm_simulator_output.txt', 'w') as f:
        f.write(get_n_random_bits(10000, circuit, backend))
    print('Done. Generated 10000 uniform random bits in qiskit_ibmq_qasm_simulator_output.txt')

'''
(qcp) neo@pop-os:~/Desktop$ python qiskit-random-bits.py 

----------------------------------------
Running IBM Q local simulator - Aer
100%|███████████████████████████████████████| 1250/1250 [00:15<00:00, 83.12it/s]
Done. Generated 10000 uniform random bits in qiskit_local_output.txt

----------------------------------------
Running IBM Q remote simulator - ibmq_qasm_simulator
Credentials already present. Set overwrite=True to overwrite.
100%|███████████████████████████████████████| 834/834 [1:35:58<00:00,  6.90s/it]
Done. Generated 10000 uniform random bits in qiskit_ibmq_qasm_simulator_output.txt

'''