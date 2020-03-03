import qiskit
from qiskit import IBMQ
import math
from tqdm import tqdm

tempBits = ''

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
    print('Running IBM Q remote simulator - ibmq_16_melbourne')
    token = 'TOKEN'
    IBMQ.save_account(token)
    IBMQ.load_account()
    provider = IBMQ.get_provider('ibm-q')
    backend = provider.get_backend('ibmq_16_melbourne')

    qr = qiskit.QuantumRegister(12)
    cr = qiskit.ClassicalRegister(12)
    circuit = qiskit.QuantumCircuit(qr, cr)
    circuit.h(qr) # Apply Hadamard gate to qubits
    circuit.measure(qr,cr) # Collapses qubit to either 1 or 0 w/ equal prob.

    with open('qiskit_ibmq_16_melbourne_output.txt', 'w') as f:
        f.write(get_n_random_bits(100, circuit, backend))
    print('Done. Generated 100 uniform random bits in qiskit_ibmq_16_melbourne_output.txt')

'''
(qcp) neo@pop-os:~/Desktop/QCP/hw3$ python qiskit-melbourne.py 

----------------------------------------
Running IBM Q remote simulator - ibmq_16_melbourne
Credentials already present. Set overwrite=True to overwrite.
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 9/9 [13:30<00:00, 90.06s/it]
Done. Generated 100 uniform random bits in qiskit_ibmq_16_melbourne_output.txt

'''