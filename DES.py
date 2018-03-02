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
    print('El %s se encuentra en espera en %d' % (nombre, env.now))
    print('Cantindad de instrucciones: %d' %(cantidad_de_instrucciones))
    print('Cantidad de memoria: %d' % (cantidad_de_memoria))

   # print('memoria ram %d memoria %d' % (simulador_de_procesos.memoria_ram.level,cantidad_de_memoria)) #prueba de memoria

    if simulador_de_procesos.memoria_ram.level >= cantidad_de_memoria:
        simulador_de_procesos.memoria_ram.get(cantidad_de_memoria)
        yield env.timeout(10) #prueba de yield


env = simpy.Environment()
bcs = simpy.Resource(env, capacity)
simulador_de_procesos = SimuladorProcesos(env)
semilla_random = 45
cantidad_de_procesos = 25
intervalo_de_procesos = 10
env.process(generador_de_procesos(env, cantidad_de_procesos, intervalo_de_procesos, simulador_de_procesos))
env.run()
