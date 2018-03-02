import simpy
import random


class SimuladorProcesos:
    def __init__(self, env):
        self.cpu = simpy.Resource(env, capacity=1)
        self.memoria_ram = simpy.Container(env, init=100)


def generador_de_procesos(env, cantidad, intervalo_de_procesos, simulador_de_procesos):
    for i in range(cantidad):
        p = proceso('Proceso %d' % i, env, simulador_de_procesos, cantidad_de_memoria=random.randint(1, 10), cantidad_de_instrucciones=random.randint(1, 10))
        env.process(p)
        t = random.expovariate(1.0 / intervalo_de_procesos)
        yield env.timeout(t)


def proceso(nombre, env, simulador_de_procesos, cantidad_de_memoria, cantidad_de_instrucciones):
    print('El %s se encuentra en new en %d' % (nombre, env.now))

    print('memoria ram disponible %d memoria solicitada por el %s: %d' % (simulador_de_procesos.memoria_ram.level, nombre, cantidad_de_memoria))

    memoria_disponible = False

    while memoria_disponible == False:
        if simulador_de_procesos.memoria_ram.level >= cantidad_de_memoria:
            memoria_disponible = True

        else:
            memoria_disponible = False

    print('El %s esta en Ready en %d' % (nombre, env.now))
    yield simulador_de_procesos.memoria_ram.get(cantidad_de_memoria)

    print('El proceso %s tiene %d intrucciones' % (nombre, cantidad_de_instrucciones))

    with simulador_de_procesos.cpu.request() as req:
            yield req
            cantidad_de_instrucciones = cantidad_de_instrucciones-1
            print('Cantidad de instrucciones restantes %d' % cantidad_de_instrucciones)
            env.timeout(10)

env = simpy.Environment()
simulador_de_procesos = SimuladorProcesos(env)
semilla_random = 45
cantidad_de_procesos = 2
intervalo_de_procesos = 10
env.process(generador_de_procesos(env, cantidad_de_procesos, intervalo_de_procesos, simulador_de_procesos))
env.run()
