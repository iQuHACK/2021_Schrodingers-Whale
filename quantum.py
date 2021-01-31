# from qiskit import *
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
# from numpy import np

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

gates = ["h","h","meas"]

for i in range(len(gates)):
    if gates[i] == "h":
        circuit.h(qreg_q[0])
    elif gates[i] == "x":
        circuit.x(qreg_q[0])
    elif gates[i] == "meas":
        circuit.measure(qreg_q[0],creg_c[0])

print(circuit.draw())

backend_sim = Aer.get_backend('qasm_simulator')

sim = execute(circuit,backend_sim, shots=1)
result = sim.result()
counts = result.get_counts(circuit)

print(counts)m