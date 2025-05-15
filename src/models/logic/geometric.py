import numpy as np
from src.models.core.solution import Solution
from src.models.base.sia import SIA
from src.constants.base import INFTY_POS
from src.funcs.base import emd_efecto
from src.funcs.format import fmt_biparte_q
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

        estados = list(np.ndindex(tensors[0].data.shape))

        T = np.zeros((n_vars, n_est, n_est), dtype=np.float32)

        for v, ncubo in enumerate(tensors):
            data = ncubo.data
            for i, estado_i in enumerate(estados):
                for j, estado_j in enumerate(estados):
                    T[v, i, j] = self.calcular_costo_transicion(estado_i, estado_j, data)

        candidates = self.identificar_candidatos(T)
        return self.evaluar_candidatos(candidates, self.sia_subsistema, T)

    def calcular_costo_transicion(self, i, j, tensor):
        d = np.sum(np.array(i) != np.array(j))
        gamma = 2.0 ** (-d)  # Asegura que gamma sea float
        cost = abs(tensor[i] - tensor[j])

        if d <= 1:
            return gamma * cost

        total = 0
        for k in self.vecinos_hamming(i, j):
            total += self.calcular_costo_transicion(k, j, tensor)

        return gamma * (cost + total)

    def vecinos_hamming(self, estado_i, estado_j):
        vecinos = []
        for pos in range(len(estado_i)):
            if estado_i[pos] != estado_j[pos]:
                vecino = list(estado_i)
                vecino[pos] = estado_j[pos]
                vecinos.append(tuple(vecino))
        return vecinos

    def identificar_candidatos(self, T):
        n_vars = T.shape[0]
        # Estrategia simple: marginalizar una variable a la vez
        return [(set(range(n_vars)) - {v}, {v}) for v in range(n_vars)]

    def evaluar_candidatos(self, candidates, sistema, T, top_k=3):
        def costo_particion(S1, S2):
            # Heurística rápida: suma costos variables marginalizadas
            return np.sum([np.sum(T[v]) for v in S2])

        # Ordenar biparticiones por costo heurístico ascendente
        candidates_ordenados = sorted(candidates, key=lambda p: costo_particion(*p))

        mejor_phi = INFTY_POS
        mejor_particion = None

        # Evaluar EMD solo en las top_k mejores candidatas
        for S1, S2 in candidates_ordenados[:top_k]:
            phi = self.calcular_phi_real(sistema, S1, S2)
            if phi < mejor_phi:
                mejor_phi = phi
                mejor_particion = (S1, S2)

        distrib = self.distribucion_particion(mejor_particion, T)
        return mejor_phi, distrib


    def calcular_phi_real(self, sistema, S1, S2):
        # Genera la bipartición real
        bipartido = sistema.bipartir(np.array(list(S1)), np.array(list(S2)))
        # Obtiene las distribuciones marginales del sistema original y bipartido
        dist_original = sistema.distribucion_marginal()
        dist_bipartido = bipartido.distribucion_marginal()
        # Calcula la pérdida usando Earth Mover's Distance analítica
        phi = emd_efecto(dist_original, dist_bipartido)
        return float(phi)

    def distribucion_particion(self, particion, T):
        S1, S2 = particion
        dist = np.zeros(T.shape[0], dtype=np.float32)
        for v in S1:
            dist[v] = 1.0
        for v in S2:
            dist[v] = 0.75
        return dist

    def algorithm(self):
        return self.find_mip()



def adaptar_a_fmt_biparte(distribucion: np.ndarray, umbral: float = 0.5):
    """
    Convierte un arreglo de probabilidades en las listas prim y dual esperadas por fmt_biparte_q.

    Args:
        distribucion (np.ndarray): arreglo con probabilidades por variable.
        umbral (float): valor para decidir en qué grupo va la variable.

    Returns:
        prim (list[tuple[int,int]]): lista para primer conjunto de bipartición.
        dual (list[tuple[int,int]]): lista para segundo conjunto de bipartición.
    """
    prim = []
    dual = []
    for i, p in enumerate(distribucion):
        # Separamos variables según si la probabilidad es >= umbral o no
        if p >= umbral:
            # Podrías definir el par como (índice, 1) o alguna lógica particular
            prim.append((i, 1))
        else:
            dual.append((i, 1))
    return prim, dual



