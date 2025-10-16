"""
Implementación de algoritmos de grafos para Investigación Operativa
- Kruskal (Árbol Mínimo)
- Prim (Árbol Mínimo)
- Dijkstra (Rutas más cortas desde origen)
- Floyd-Warshall (Rutas más cortas entre todos los pares)
- Ford-Fulkerson (Flujo máximo)
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict, deque
import heapq

class UnionFind:
    """Estructura de datos Union-Find para Kruskal"""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

class AlgoritmosGrafos:
    
    @staticmethod
    def kruskal(aristas, n_nodos):
        """
        Algoritmo de Kruskal para encontrar el árbol de expansión mínima
        
        aristas: lista de tuplas (u, v, peso)
        n_nodos: número de nodos
        
        Retorna: lista de aristas del MST, peso total, lista de iteraciones
        """
        print("\n=== ALGORITMO DE KRUSKAL ===\n")
        
        # Ordenar aristas por peso
        aristas_ordenadas = sorted(aristas, key=lambda x: x[2])
        
        uf = UnionFind(n_nodos)
        mst = []
        peso_total = 0
        iteraciones = []
        
        print("Aristas ordenadas por peso:")
        for u, v, peso in aristas_ordenadas:
            print(f"  {u} - {v}: {peso}")
        
        print("\nProceso de selección:")
        iteracion_num = 1
        for u, v, peso in aristas_ordenadas:
            raiz_u = uf.find(u)
            raiz_v = uf.find(v)
            
            if uf.union(u, v):
                mst.append((u, v, peso))
                peso_total += peso
                print(f"  ✓ Agregada: {u} - {v} (peso: {peso})")
                
                iteraciones.append({
                    'num': iteracion_num,
                    'arista': (u, v, peso),
                    'aceptada': True,
                    'raiz_u': raiz_u,
                    'raiz_v': raiz_v,
                    'mst_actual': list(mst),
                    'peso_acumulado': peso_total
                })
            else:
                print(f"  ✗ Rechazada: {u} - {v} (formaría ciclo)")
                
                iteraciones.append({
                    'num': iteracion_num,
                    'arista': (u, v, peso),
                    'aceptada': False,
                    'raiz_u': raiz_u,
                    'raiz_v': raiz_v,
                    'mst_actual': list(mst),
                    'peso_acumulado': peso_total
                })
            
            iteracion_num += 1
        
        print(f"\nPeso total del MST: {peso_total}")
        return mst, peso_total, iteraciones
    
    @staticmethod
    def prim(grafo, inicio=0):
        """
        Algoritmo de Prim para encontrar el árbol de expansión mínima
        
        grafo: diccionario {nodo: {vecino: peso}}
        inicio: nodo inicial
        
        Retorna: lista de aristas del MST, peso total, lista de iteraciones
        """
        print("\n=== ALGORITMO DE PRIM ===\n")
        print(f"Nodo inicial: {inicio}\n")
        
        visitados = {inicio}
        mst = []
        peso_total = 0
        iteraciones = []
        
        # Cola de prioridad: (peso, nodo_origen, nodo_destino)
        heap = []
        for vecino, peso in grafo[inicio].items():
            heapq.heappush(heap, (peso, inicio, vecino))
        
        # Guardar estado inicial
        iteraciones.append({
            'num': 0,
            'tipo': 'inicial',
            'nodo_inicio': inicio,
            'visitados': set(visitados),
            'mst': [],
            'peso_total': 0,
            'candidatos': [(p, u, v) for p, u, v in heap]
        })
        
        print("Proceso de construcción:")
        iteracion = 1
        
        while heap and len(visitados) < len(grafo):
            peso, u, v = heapq.heappop(heap)
            
            if v in visitados:
                print(f"  {iteracion}. {u} - {v} (peso: {peso}) - Ya visitado, se omite")
                iteraciones.append({
                    'num': iteracion,
                    'tipo': 'rechazada',
                    'arista': (u, v, peso),
                    'razon': 'nodo ya visitado',
                    'visitados': set(visitados),
                    'mst': list(mst),
                    'peso_total': peso_total
                })
                continue
            
            visitados.add(v)
            mst.append((u, v, peso))
            peso_total += peso
            print(f"  {iteracion}. ✓ Agregada: {u} - {v} (peso: {peso})")
            
            # Agregar nuevas aristas
            nuevas_aristas = []
            for vecino, peso_vecino in grafo[v].items():
                if vecino not in visitados:
                    heapq.heappush(heap, (peso_vecino, v, vecino))
                    nuevas_aristas.append((v, vecino, peso_vecino))
            
            iteraciones.append({
                'num': iteracion,
                'tipo': 'aceptada',
                'arista': (u, v, peso),
                'visitados': set(visitados),
                'mst': list(mst),
                'peso_total': peso_total,
                'nuevas_aristas': nuevas_aristas
            })
            
            iteracion += 1
        
        print(f"\nPeso total del MST: {peso_total}")
        return mst, peso_total, iteraciones
    
    @staticmethod
    def dijkstra(grafo, origen):
        """
        Algoritmo de Dijkstra para encontrar rutas más cortas desde un origen
        
        grafo: diccionario {nodo: {vecino: peso}}
        origen: nodo origen
        
        Retorna: diccionario de distancias, diccionario de predecesores, lista de iteraciones
        """
        print("\n=== ALGORITMO DE DIJKSTRA ===\n")
        print(f"Nodo origen: {origen}\n")
        
        distancias = {nodo: float('inf') for nodo in grafo}
        distancias[origen] = 0
        predecesores = {nodo: None for nodo in grafo}
        visitados = set()
        
        # Cola de prioridad: (distancia, nodo)
        heap = [(0, origen)]
        
        # Lista para almacenar las iteraciones
        iteraciones = []
        
        print("Proceso de exploración:")
        iteracion = 1
        
        while heap:
            dist_actual, nodo_actual = heapq.heappop(heap)
            
            if nodo_actual in visitados:
                continue
            
            visitados.add(nodo_actual)
            print(f"\n{iteracion}. Visitando nodo {nodo_actual} (distancia: {dist_actual})")
            
            actualizaciones = []
            
            # Explorar vecinos
            for vecino, peso in grafo[nodo_actual].items():
                if vecino not in visitados:
                    nueva_dist = dist_actual + peso
                    
                    if nueva_dist < distancias[vecino]:
                        print(f"   → Actualizando {vecino}: {distancias[vecino]} → {nueva_dist}")
                        dist_anterior = distancias[vecino]
                        distancias[vecino] = nueva_dist
                        predecesores[vecino] = nodo_actual
                        heapq.heappush(heap, (nueva_dist, vecino))
                        
                        actualizaciones.append({
                            'vecino': vecino,
                            'dist_anterior': dist_anterior,
                            'dist_nueva': nueva_dist,
                            'peso_arista': peso
                        })
            
            # Guardar estado de esta iteración
            iteraciones.append({
                'num': iteracion,
                'nodo_actual': nodo_actual,
                'dist_actual': dist_actual,
                'distancias': dict(distancias),
                'visitados': set(visitados),
                'actualizaciones': actualizaciones
            })
            
            iteracion += 1
        
        print("\n" + "=" * 50)
        print("DISTANCIAS MÍNIMAS DESDE EL ORIGEN")
        print("=" * 50)
        for nodo in sorted(distancias.keys()):
            if distancias[nodo] == float('inf'):
                print(f"  {origen} → {nodo}: ∞ (no alcanzable)")
            else:
                camino = AlgoritmosGrafos._reconstruir_camino(predecesores, origen, nodo)
                print(f"  {origen} → {nodo}: {distancias[nodo]} | Camino: {' → '.join(map(str, camino))}")
        
        return distancias, predecesores, iteraciones
    
    @staticmethod
    def _reconstruir_camino(predecesores, origen, destino):
        """Reconstruye el camino desde el origen hasta el destino"""
        if predecesores[destino] is None and destino != origen:
            return []
        
        camino = []
        nodo = destino
        while nodo is not None:
            camino.append(nodo)
            nodo = predecesores[nodo]
        
        return camino[::-1]
    
    @staticmethod
    def floyd_warshall(grafo):
        """
        Algoritmo de Floyd-Warshall (implementación estilo TORA)
        
        grafo: diccionario {nodo: {vecino: peso}}
        
        Retorna: matriz de distancias, matriz de predecesores, lista de iteraciones
        """
        print("\n=== ALGORITMO DE FLOYD-WARSHALL ===\n")
        
        nodos = sorted(grafo.keys())
        n = len(nodos)
        nodo_a_idx = {nodo: i for i, nodo in enumerate(nodos)}
        
        # Inicializar matrices D (distancias) y P (predecesores)
        D = [[float('inf')] * n for _ in range(n)]
        P = [[None] * n for _ in range(n)]  # Matriz de PREDECESORES
        
        # Lista para almacenar las iteraciones
        iteraciones = []
        
        # Paso 1: Inicializar D y P
        # D[i][i] = 0 para todo i
        for i in range(n):
            D[i][i] = 0.0
            P[i][i] = None  # No hay predecesor para ir de un nodo a sí mismo
        
        # D[i][j] = peso si existe arista i→j, infinito en caso contrario
        # P[i][j] = i si existe arista directa i→j (el predecesor de j es i)
        for i in range(n):
            for j in range(n):
                if i != j:
                    nodo_i = nodos[i]
                    nodo_j = nodos[j]
                    if nodo_i in grafo and nodo_j in grafo[nodo_i]:
                        D[i][j] = grafo[nodo_i][nodo_j]
                        P[i][j] = nodo_i  # El predecesor de j en i→j es i
                    else:
                        D[i][j] = float('inf')
                        P[i][j] = nodo_i  # Inicializar con origen (estándar TORA)
        
        print("Matriz de distancias inicial:")
        AlgoritmosGrafos._imprimir_matriz(D, nodos)
        
        # Guardar estado inicial (K=0)
        iteraciones.append({
            'k': 0,
            'nodo_intermedio': 'Inicial',
            'matriz_d': [row[:] for row in D],
            'matriz_s': [row[:] for row in P],  # Ahora es matriz de predecesores
            'cambios': []
        })
        
        # Paso 2: Aplicar algoritmo de Floyd-Warshall
        # Para cada nodo intermedio k
        for k in range(n):
            print(f"\nIteración {k+1} (usando nodo intermedio: {nodos[k]}):")
            cambios = []
            
            # Para cada par de nodos (i, j)
            for i in range(n):
                for j in range(n):
                    # Verificar si pasar por k mejora la ruta de i a j
                    if D[i][k] != float('inf') and D[k][j] != float('inf'):
                        nueva_dist = D[i][k] + D[k][j]
                        if nueva_dist < D[i][j]:
                            dist_anterior = D[i][j]
                            D[i][j] = nueva_dist
                            P[i][j] = P[k][j]  # El predecesor de j en i→j es el mismo que k→j
                            cambios.append({
                                'origen': nodos[i],
                                'destino': nodos[j],
                                'dist_anterior': dist_anterior,
                                'dist_nueva': D[i][j],
                                'via': nodos[k]
                            })
            
            AlgoritmosGrafos._imprimir_matriz(D, nodos)
            
            # Guardar estado de esta iteración
            iteraciones.append({
                'k': k + 1,
                'nodo_intermedio': nodos[k],
                'matriz_d': [row[:] for row in D],
                'matriz_s': [row[:] for row in P],  # Ahora es matriz de predecesores
                'cambios': cambios
            })
        
        print("\n" + "=" * 50)
        print("MATRIZ DE DISTANCIAS FINAL")
        print("=" * 50)
        AlgoritmosGrafos._imprimir_matriz(D, nodos)
        
        print("\n" + "=" * 50)
        print("CAMINOS MÁS CORTOS")
        print("=" * 50)
        for i, origen in enumerate(nodos):
            for j, destino in enumerate(nodos):
                if i != j and D[i][j] != float('inf'):
                    camino = AlgoritmosGrafos._reconstruir_camino_fw_predecesores(P, nodo_a_idx, origen, destino, nodos)
                    print(f"  {origen} → {destino}: {D[i][j]} | Camino: {' → '.join(map(str, camino))}")
        
        return D, P, nodos, nodo_a_idx, iteraciones
    
    @staticmethod
    def _imprimir_matriz(matriz, nodos):
        """Imprime una matriz de forma legible"""
        n = len(nodos)
        
        # Encabezado
        print("      ", end="")
        for nodo in nodos:
            print(f"{str(nodo):>6}", end="")
        print()
        
        # Filas
        for i, nodo in enumerate(nodos):
            print(f"{str(nodo):>4}:", end="")
            for j in range(n):
                val = matriz[i][j]
                if val == float('inf'):
                    print("   ∞  ", end="")
                else:
                    print(f"{val:>6.1f}", end="")
            print()
    
    @staticmethod
    def _reconstruir_camino_fw(next_node, nodo_a_idx, origen, destino, nodos):
        """Reconstruye el camino en Floyd-Warshall usando matriz de sucesores"""
        i = nodo_a_idx[origen]
        j = nodo_a_idx[destino]
        
        if next_node[i][j] is None:
            return []
        
        camino = [origen]
        while origen != destino:
            origen = next_node[nodo_a_idx[origen]][nodo_a_idx[destino]]
            camino.append(origen)
        
        return camino
    
    @staticmethod
    def _reconstruir_camino_fw_predecesores(pred, nodo_a_idx, origen, destino, nodos):
        """Reconstruye el camino en Floyd-Warshall usando matriz de predecesores"""
        i = nodo_a_idx[origen]
        j = nodo_a_idx[destino]
        
        if pred[i][j] is None:
            return []
        
        # Reconstruir desde el destino hacia el origen
        camino = [destino]
        actual = destino
        
        while actual != origen:
            idx_actual = nodo_a_idx[actual]
            idx_origen = nodo_a_idx[origen]
            predecesor = pred[idx_origen][idx_actual]
            
            if predecesor is None or predecesor == actual:
                break
                
            camino.insert(0, predecesor)
            actual = predecesor
        
        return camino
    
    @staticmethod
    def visualizar_grafo(grafo, mst=None, titulo="Grafo"):
        """Visualiza un grafo con NetworkX"""
        G = nx.Graph()
        
        # Agregar aristas
        for u in grafo:
            for v, peso in grafo[u].items():
                G.add_edge(u, v, weight=peso)
        
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=1000, alpha=0.9)
        
        # Dibujar todas las aristas
        nx.draw_networkx_edges(G, pos, width=1, alpha=0.3, 
                              edge_color='gray')
        
        # Resaltar MST si está disponible
        if mst:
            mst_edges = [(u, v) for u, v, _ in mst]
            nx.draw_networkx_edges(G, pos, edgelist=mst_edges, 
                                  width=3, alpha=1, edge_color='red')
        
        # Etiquetas
        nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')
        
        # Pesos de aristas
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10)
        
        plt.title(titulo, fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        return plt

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo de grafo
    grafo = {
        0: {1: 4, 2: 3},
        1: {0: 4, 2: 1, 3: 2},
        2: {0: 3, 1: 1, 3: 4},
        3: {1: 2, 2: 4}
    }
    
    aristas = [
        (0, 1, 4),
        (0, 2, 3),
        (1, 2, 1),
        (1, 3, 2),
        (2, 3, 4)
    ]
    
    # Kruskal
    mst_k, peso_k = AlgoritmosGrafos.kruskal(aristas, 4)
    
    # Prim
    mst_p, peso_p = AlgoritmosGrafos.prim(grafo, 0)
    
    # Dijkstra
    dist, pred = AlgoritmosGrafos.dijkstra(grafo, 0)
    
    # Floyd-Warshall
    dist_fw, next_fw, nodos, idx = AlgoritmosGrafos.floyd_warshall(grafo)
    
    # Visualizar
    plt_obj = AlgoritmosGrafos.visualizar_grafo(grafo, mst_k, "Árbol de Expansión Mínima (Kruskal)")
    plt_obj.show()
