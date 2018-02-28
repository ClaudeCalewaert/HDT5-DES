import simpy
import random

class SimuladorProcesos:
    def __init__(self, env):
        self.cpu = simpy.Resource(env, capacity=1)
        self.memoria_ram = simpy.Container(env, init=100)


def generador_de_procesos(env,cantidad, intervalo_de_procesos, simulador_de_procesos):
    for i in range(cantidad):
        p = proceso('Proceso %d' % i, env, simulador_de_procesos)
        env.process(p)
        t = random.expovariate(1.0 / intervalo_de_procesos)
        yield env.timeout(t)






env = simpy.Environment()
simulador_de_procesos = SimuladorProcesos(env)
semilla_random = 45
cantidad_de_procesos = 25
intervalo_de_procesos = 10
env.process(generador_de_procesos(env, cantidad_de_procesos, intervalo_de_procesos,simulador_de_procesos))
