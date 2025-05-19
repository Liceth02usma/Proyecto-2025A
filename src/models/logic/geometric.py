import numpy as np
from itertools import combinations
from src.models.core.solution import Solution
from src.models.base.sia import SIA
from src.constants.base import INFTY_POS
from src.funcs.base import emd_efecto, lil_endian
from src.funcs.format import fmt_biparte_q
import itertools
from src.constants.base import (
    EFECTO,
    ACTUAL,
    INFTY_NEG,
    INFTY_POS,
    LAST_IDX,
)

class GeometricSIA(SIA):
    def __init__(self, config):
        super().__init__(config)
        self.vertices: set[tuple]

    def aplicar_estrategia(self, conditions, purview, mechanism):
        self.sia_preparar_subsistema(conditions, purview, mechanism)

        phi, distribucion = self.find_mip()
        prim, dual = adaptar_a_fmt_biparte(distribucion)
        fmt_mip = fmt_biparte_q(prim, dual)

        return Solution(
            estrategia="Geometric",
            perdida=phi,
            distribucion_subsistema=self.sia_dists_marginales,
            distribucion_particion=distribucion,
            particion=fmt_mip[0],
        )

    def find_mip(self):
        tensors = self.sia_subsistema.ncubos
        n_vars = len(tensors)
        n_est = tensors[0].data.size
        # Impresion de tensores
        print('A')
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    print(f"A({c}|{b}{a}) = {tensors[0].data[a, b, c]}")
                   
        print("B")
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    print(f"B({c}|{b}{a}) = {tensors[1].data[a, b, c]}")
                    
        print("C")
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    print(f"C({c}|{b}{a}) = {tensors[2].data[a, b, c]}")

        # Genera todos los índices multidimensionales (big-endian)
        estados_big = list(np.ndindex(tensors[0].data.shape))
        # Convierte a little-endian invirtiendo el orden de índices
        estados = [tuple(reversed(e)) for e in estados_big]

        T = np.zeros((n_vars, n_est, n_est), dtype=np.float32)
        #T[0, 0, 1] = self.calcular_costo_transicion(estados[0], estados[1], tensors[0].data)
        #print(f'Costo Ta({estados[0]},{estados[1]})=',T[0, 0, 1])
        # A cubo(0) -> 000 (0) 100 (1)

        
        for v, ncubo in enumerate(tensors):
            data = ncubo.data
            for i, estado_i in enumerate(estados):
                for j, estado_j in enumerate(estados):
                    T[v, i, j] = self.calcular_costo_transicion(estado_i, estado_j, data)


        print(T)
        imprimir_tabla_costos_desde_000(T)
        # Generar exhaustivamente todas las biparticiones
        candidates = self.generar_todas_biparticiones(n_vars)
        print(candidates)
        return self.evaluar_candidatos(candidates, self.sia_subsistema, T)
        

    def calcular_costo_transicion(self, i, j, tensor):
        d = np.sum(np.array(i) != np.array(j))
        gamma = 2.0 ** (-d)  # Asegura que gamma sea float
        cost = abs(tensor[i] - tensor[j])
        #print(f"Ta[{i},{j}]={gamma}(|{tensor[i]}-{ tensor[j]}|)+numero de bits cambiantes{d}")
        if d <= 1:
            return gamma * cost
        #vecinos = dict(zip(i, j))
        total = 0
        #print(self.vecinos_hamming(i, j))
        for k in self.vecinos_hamming(i, j):
            valor = self.calcular_costo_transicion(k, j, tensor)
            #print(f"Total Vecinos Ta[{k},{j}]={valor}")
            total += valor
            
        
        return gamma * (cost + total)

    def vecinos_hamming(self, estado_i, estado_j):
        vecinos = []
        for pos in range(len(estado_i)):
            if estado_i[pos] != estado_j[pos]:
                vecino = list(estado_i)
                vecino[pos] = estado_j[pos]
                vecinos.append(tuple(vecino))
        return vecinos

    def generar_todas_biparticiones(self, n_vars):
        variables = set(range(n_vars))
        biparticiones = []
        # Solo consideramos subconjuntos con tamaño <= n_vars // 2 para evitar duplicados
        for r in range(1, (n_vars // 2) + 1):
            for subset in combinations(variables, r):
                S1 = set(subset)
                S2 = variables - S1
                biparticiones.append((S1, S2))
        return biparticiones

    def evaluar_candidatos(self, candidates, sistema, T):
        mejor_phi = INFTY_POS
        mejor_particion = None

        for S1, S2 in candidates:
            phi = self.calcular_phi_real(sistema, S1, S2)
            if phi < mejor_phi:
                mejor_phi = phi
                mejor_particion = (S1, S2)
            print(phi, (S1, S2))

        distrib = self.distribucion_particion_real(sistema, mejor_particion)
        return mejor_phi, distrib

    def calcular_phi_real(self, sistema, S1, S2):
        bipartido = sistema.bipartir(np.array(list(S1)), np.array(list(S2)))
        dist_original = sistema.distribucion_marginal()
        dist_bipartido = bipartido.distribucion_marginal()
        phi = emd_efecto(dist_original, dist_bipartido)
        return float(phi)

    def distribucion_particion_real(self, sistema, particion):
        S1, S2 = particion
        bipartido = sistema.bipartir(np.array(list(S1)), np.array(list(S2)))
        return bipartido.distribucion_marginal()

    def algorithm(self):
        return self.find_mip()


def adaptar_a_fmt_biparte(distribucion: np.ndarray, umbral: float = 0.5):
    prim = []
    dual = []
    for i, p in enumerate(distribucion):
        if p >= umbral:
            prim.append((i, 1))
        else:
            dual.append((i, 1))
    return prim, dual


def imprimir_tabla_costos_desde_000(T):
    n_vars, n_est, _ = T.shape
    # Estados binarios para 3 bits
    estados_binarios = [format(i, '03b') for i in range(n_est)]

    print(f"{'Transición':<12}", end='')
    for v in range(n_vars):
        print(f"Variable {chr(65+v):<10}", end='')
    print()

    for j in range(n_est):
        print(f"t(000,{estados_binarios[j]})".ljust(12), end='')
        for v in range(n_vars):
            costo = T[v, 0, j]  # fila 0: estado 000, columna j: estado j
            print(f"{costo:<10.3f}", end='')
        print()
