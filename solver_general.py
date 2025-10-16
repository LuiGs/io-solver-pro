#!/usr/bin/env python3
"""
SOLVER GENERAL DE TEORÍA DE GRAFOS
===================================

Herramienta interactiva para resolver CUALQUIER problema de:
- Árbol de expansión mínima (Kruskal/Prim)
- Rutas más cortas (Dijkstra/Floyd-Warshall)
- Flujo máximo (Ford-Fulkerson)
- Juegos de suma cero

Modo de uso: Ingresa tus datos, elige el algoritmo, obtén la solución.
"""

import sys
from algoritmos_grafos import AlgoritmosGrafos
from ejercicio3_ford_fulkerson import FordFulkerson
import numpy as np
from scipy.optimize import linprog

class SolverGrafos:
    """Solver general para problemas de teoría de grafos"""
    
    @staticmethod
    def parsear_aristas(texto, dirigido=False):
        """
        Parsea aristas desde texto
        Formatos aceptados:
        - "A B 5" (nodo1 nodo2 peso)
        - "1 2 3.5" (con decimales)
        - "# comentario" (ignorado)
        """
        lineas = texto.strip().split('\n')
        aristas = []
        grafo = {}
        nodos = set()
        
        for linea in lineas:
            linea = linea.strip()
            # Ignorar comentarios y líneas vacías
            if not linea or linea.startswith('#'):
                continue
            
            partes = linea.split()
            if len(partes) >= 3:
                try:
                    u, v = partes[0], partes[1]
                    peso = float(partes[2])
                    
                    # Convertir a números si es posible
                    try:
                        u = int(u)
                        v = int(v)
                    except ValueError:
                        pass
                    
                    aristas.append((u, v, peso))
                    nodos.add(u)
                    nodos.add(v)
                    
                    # Construir grafo
                    if u not in grafo:
                        grafo[u] = {}
                    if v not in grafo:
                        grafo[v] = {}
                    
                    grafo[u][v] = peso
                    if not dirigido:
                        grafo[v][u] = peso
                        
                except (ValueError, IndexError):
                    print(f"⚠️ Línea ignorada (formato incorrecto): {linea}")
                    continue
        
        return aristas, grafo, sorted(list(nodos))
    
    @staticmethod
    def resolver_mst(texto, algoritmo='kruskal'):
        """
        Resuelve árbol de expansión mínima
        
        Args:
            texto: string con aristas (una por línea: nodo1 nodo2 peso)
            algoritmo: 'kruskal' o 'prim'
        """
        print("=" * 70)
        print(f"RESOLVIENDO: ÁRBOL DE EXPANSIÓN MÍNIMA ({algoritmo.upper()})")
        print("=" * 70)
        
        aristas, grafo, nodos = SolverGrafos.parsear_aristas(texto)
        
        if not aristas:
            print("❌ Error: No se encontraron aristas válidas")
            return None
        
        print(f"\n📊 Datos de entrada:")
        print(f"   Nodos: {len(nodos)} → {nodos}")
        print(f"   Aristas: {len(aristas)}")
        
        # Mapear nodos a índices
        nodo_a_idx = {nodo: i for i, nodo in enumerate(nodos)}
        aristas_idx = [(nodo_a_idx[u], nodo_a_idx[v], peso) for u, v, peso in aristas]
        grafo_idx = {nodo_a_idx[n]: {nodo_a_idx[v]: p for v, p in vecinos.items()} 
                    for n, vecinos in grafo.items()}
        
        # Resolver
        if algoritmo.lower() == 'kruskal':
            mst, peso_total = AlgoritmosGrafos.kruskal(aristas_idx, len(nodos))
        else:
            mst, peso_total = AlgoritmosGrafos.prim(grafo_idx, 0)
        
        # Convertir índices de vuelta a nombres
        mst = [(nodos[u], nodos[v], peso) for u, v, peso in mst]
        
        print("\n" + "=" * 70)
        print("✅ SOLUCIÓN")
        print("=" * 70)
        print(f"\nAristas del MST:")
        for u, v, peso in mst:
            print(f"   {u} - {v}: {peso}")
        print(f"\n🎯 PESO TOTAL DEL MST: {peso_total}")
        print(f"   Aristas en el MST: {len(mst)}")
        print(f"   Verificación: {len(mst)} = {len(nodos)}-1 ✓")
        print("=" * 70)
        
        return {'mst': mst, 'peso': peso_total, 'nodos': nodos}
    
    @staticmethod
    def resolver_dijkstra(texto, origen):
        """
        Resuelve rutas más cortas desde un origen (Dijkstra)
        
        Args:
            texto: string con aristas
            origen: nodo origen
        """
        print("=" * 70)
        print("RESOLVIENDO: RUTAS MÁS CORTAS (DIJKSTRA)")
        print("=" * 70)
        
        aristas, grafo, nodos = SolverGrafos.parsear_aristas(texto)
        
        if not aristas:
            print("❌ Error: No se encontraron aristas válidas")
            return None
        
        # Convertir origen si es necesario
        try:
            origen = int(origen)
        except ValueError:
            pass
        
        if origen not in grafo:
            print(f"❌ Error: El nodo origen '{origen}' no existe en el grafo")
            print(f"   Nodos disponibles: {nodos}")
            return None
        
        print(f"\n📊 Datos de entrada:")
        print(f"   Nodos: {len(nodos)} → {nodos}")
        print(f"   Origen: {origen}")
        
        # Resolver
        distancias, predecesores = AlgoritmosGrafos.dijkstra(grafo, origen)
        
        print("\n" + "=" * 70)
        print("✅ SOLUCIÓN")
        print("=" * 70)
        
        for nodo in sorted(distancias.keys()):
            if distancias[nodo] == float('inf'):
                print(f"\n{origen} → {nodo}: ∞ (no alcanzable)")
            else:
                camino = SolverGrafos._reconstruir_camino(predecesores, origen, nodo)
                print(f"\n{origen} → {nodo}: {distancias[nodo]}")
                print(f"   Camino: {' → '.join(map(str, camino))}")
        
        print("\n" + "=" * 70)
        
        return {'distancias': distancias, 'predecesores': predecesores}
    
    @staticmethod
    def resolver_floyd_warshall(texto):
        """
        Resuelve rutas más cortas entre todos los pares (Floyd-Warshall)
        """
        print("=" * 70)
        print("RESOLVIENDO: TODAS LAS RUTAS MÁS CORTAS (FLOYD-WARSHALL)")
        print("=" * 70)
        
        # Para Floyd-Warshall, el grafo puede ser dirigido
        aristas, grafo, nodos = SolverGrafos.parsear_aristas(texto, dirigido=True)
        
        if not aristas:
            print("❌ Error: No se encontraron aristas válidas")
            return None
        
        # Asegurar que todos los nodos estén en el grafo
        nodos_set = set(grafo.keys())
        for vecinos in grafo.values():
            nodos_set.update(vecinos.keys())
        
        for nodo in nodos_set:
            if nodo not in grafo:
                grafo[nodo] = {}
        
        print(f"\n📊 Datos de entrada:")
        print(f"   Nodos: {len(nodos_set)}")
        print(f"   Aristas: {len(aristas)}")
        
        # Resolver
        dist, next_node, nodos_lista, nodo_a_idx = AlgoritmosGrafos.floyd_warshall(grafo)
        
        print("\n" + "=" * 70)
        print("✅ MATRIZ DE DISTANCIAS FINALES")
        print("=" * 70)
        
        return {'distancias': dist, 'nodos': nodos_lista, 'indices': nodo_a_idx}
    
    @staticmethod
    def resolver_flujo_maximo(texto, origen, destino):
        """
        Resuelve flujo máximo (Ford-Fulkerson)
        """
        print("=" * 70)
        print("RESOLVIENDO: FLUJO MÁXIMO (FORD-FULKERSON)")
        print("=" * 70)
        
        aristas, grafo_temp, nodos = SolverGrafos.parsear_aristas(texto, dirigido=True)
        
        if not aristas:
            print("❌ Error: No se encontraron aristas válidas")
            return None
        
        # Convertir origen y destino si es necesario
        try:
            origen = int(origen)
            destino = int(destino)
        except ValueError:
            pass
        
        # Construir grafo para Ford-Fulkerson (solo capacidades positivas)
        grafo = {}
        for u, v, cap in aristas:
            if u not in grafo:
                grafo[u] = {}
            grafo[u][v] = cap
        
        # Asegurar que destino esté en el grafo
        if destino not in grafo:
            grafo[destino] = {}
        
        if origen not in grafo:
            print(f"❌ Error: El nodo origen '{origen}' no existe")
            return None
        
        print(f"\n📊 Datos de entrada:")
        print(f"   Nodos: {len(nodos)}")
        print(f"   Origen: {origen}")
        print(f"   Destino: {destino}")
        print(f"   Aristas con capacidad: {len(aristas)}")
        
        # Resolver
        ff = FordFulkerson(grafo)
        flujo_maximo, caminos = ff.calcular_flujo_maximo(origen, destino)
        
        # Corte mínimo
        visitados, corte, cap_corte = ff.encontrar_corte_minimo(origen)
        
        print("\n" + "=" * 70)
        print("✅ SOLUCIÓN")
        print("=" * 70)
        print(f"\n🎯 FLUJO MÁXIMO: {flujo_maximo}")
        print(f"\nCaminos aumentantes utilizados: {len(caminos)}")
        for i, (camino, flujo) in enumerate(caminos, 1):
            print(f"   {i}. {' → '.join(map(str, camino))}: flujo = {flujo}")
        
        print(f"\n📊 CORTE MÍNIMO:")
        print(f"   Capacidad del corte: {cap_corte}")
        print(f"   Nodos alcanzables: {sorted(visitados)}")
        print(f"   Verificación: Flujo máximo = Corte mínimo → {flujo_maximo} = {cap_corte} ✓")
        print("=" * 70)
        
        return {'flujo_maximo': flujo_maximo, 'caminos': caminos, 'corte': corte}
    
    @staticmethod
    def resolver_juego_suma_cero(matriz_texto):
        """
        Resuelve un juego de suma cero
        
        Args:
            matriz_texto: matriz de pagos como string
                         (una fila por línea, valores separados por espacios)
        """
        print("=" * 70)
        print("RESOLVIENDO: JUEGO DE SUMA CERO")
        print("=" * 70)
        
        # Parsear matriz
        lineas = matriz_texto.strip().split('\n')
        matriz = []
        
        for linea in lineas:
            if linea.strip() and not linea.startswith('#'):
                try:
                    fila = [float(x) for x in linea.strip().split()]
                    if fila:
                        matriz.append(fila)
                except ValueError:
                    print(f"⚠️ Línea ignorada: {linea}")
        
        if not matriz:
            print("❌ Error: No se pudo parsear la matriz")
            return None
        
        matriz = np.array(matriz)
        m, n = matriz.shape
        
        print(f"\n📊 Datos de entrada:")
        print(f"   Tamaño: {m}x{n} (Jugador A tiene {m} estrategias, B tiene {n})")
        print("\nMatriz de pagos (Jugador A):")
        for i, fila in enumerate(matriz):
            print(f"   Estrategia {i+1}: {fila}")
        
        # Resolver con programación lineal
        # Jugador A (maximizar)
        c = np.zeros(m + 1)
        c[-1] = -1  # Maximizar v
        
        A_ub = []
        b_ub = []
        for j in range(n):
            fila = [-matriz[i][j] for i in range(m)] + [1]
            A_ub.append(fila)
            b_ub.append(0)
        
        A_eq = [[1] * m + [0]]
        b_eq = [1]
        
        bounds = [(0, None)] * m + [(None, None)]
        
        resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, 
                          bounds=bounds, method='highs')
        
        if resultado.success:
            estrategia_a = resultado.x[:-1]
            valor_juego = resultado.x[-1]
            
            print("\n" + "=" * 70)
            print("✅ SOLUCIÓN")
            print("=" * 70)
            
            print("\n🎮 Estrategia óptima del Jugador A:")
            for i, prob in enumerate(estrategia_a):
                if prob > 0.001:
                    print(f"   Estrategia {i+1}: {prob:.4f} ({prob*100:.2f}%)")
            
            print(f"\n🎯 VALOR DEL JUEGO: {valor_juego:.4f}")
            
            if valor_juego > 0.01:
                print("   → El juego favorece al Jugador A")
            elif valor_juego < -0.01:
                print("   → El juego favorece al Jugador B")
            else:
                print("   → El juego es justo (equilibrado)")
            
            print("=" * 70)
            
            return {'estrategia_a': estrategia_a, 'valor': valor_juego}
        else:
            print("\n❌ No se pudo resolver el juego")
            return None
    
    @staticmethod
    def _reconstruir_camino(predecesores, origen, destino):
        """Reconstruye un camino desde origen hasta destino"""
        if predecesores[destino] is None and destino != origen:
            return []
        
        camino = []
        nodo = destino
        while nodo is not None:
            camino.append(nodo)
            nodo = predecesores[nodo]
        
        return camino[::-1]

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 70)
    print("  🎓 SOLVER GENERAL DE TEORÍA DE GRAFOS")
    print("=" * 70)
    print("\n📚 ALGORITMOS DISPONIBLES:")
    print("  1. Árbol de Expansión Mínima - Kruskal")
    print("  2. Árbol de Expansión Mínima - Prim")
    print("  3. Rutas Más Cortas - Dijkstra")
    print("  4. Todas las Rutas - Floyd-Warshall")
    print("  5. Flujo Máximo - Ford-Fulkerson")
    print("  6. Juego de Suma Cero")
    print("\n  0. Salir")
    print("=" * 70)

def solicitar_aristas():
    """Solicita al usuario que ingrese aristas"""
    print("\n📝 Ingrese las aristas (formato: nodo1 nodo2 peso)")
    print("   Puede usar letras (A B 5) o números (1 2 5)")
    print("   Ingrese una línea vacía para terminar\n")
    
    lineas = []
    while True:
        linea = input("   ").strip()
        if not linea:
            break
        lineas.append(linea)
    
    return '\n'.join(lineas)

def solicitar_matriz():
    """Solicita matriz para juego de suma cero"""
    print("\n📝 Ingrese la matriz de pagos (una fila por línea)")
    print("   Ejemplo: 2 1 0")
    print("   Ingrese una línea vacía para terminar\n")
    
    lineas = []
    while True:
        linea = input("   ").strip()
        if not linea:
            break
        lineas.append(linea)
    
    return '\n'.join(lineas)

def main():
    """Función principal"""
    print("\n🎓 Bienvenido al Solver General de Teoría de Grafos")
    print("   Herramienta para resolver CUALQUIER problema de grafos\n")
    
    while True:
        try:
            mostrar_menu()
            opcion = input("\n👉 Selecciona un algoritmo (0-6): ").strip()
            
            if opcion == '0':
                print("\n👋 ¡Hasta luego! Buena suerte en tu examen 🍀\n")
                break
            
            elif opcion in ['1', '2']:
                texto = solicitar_aristas()
                if texto:
                    algoritmo = 'kruskal' if opcion == '1' else 'prim'
                    SolverGrafos.resolver_mst(texto, algoritmo)
                input("\nPresiona ENTER para continuar...")
            
            elif opcion == '3':
                texto = solicitar_aristas()
                if texto:
                    origen = input("\n🎯 Nodo origen: ").strip()
                    SolverGrafos.resolver_dijkstra(texto, origen)
                input("\nPresiona ENTER para continuar...")
            
            elif opcion == '4':
                texto = solicitar_aristas()
                if texto:
                    SolverGrafos.resolver_floyd_warshall(texto)
                input("\nPresiona ENTER para continuar...")
            
            elif opcion == '5':
                texto = solicitar_aristas()
                if texto:
                    origen = input("\n🎯 Nodo origen: ").strip()
                    destino = input("🎯 Nodo destino: ").strip()
                    SolverGrafos.resolver_flujo_maximo(texto, origen, destino)
                input("\nPresiona ENTER para continuar...")
            
            elif opcion == '6':
                matriz = solicitar_matriz()
                if matriz:
                    SolverGrafos.resolver_juego_suma_cero(matriz)
                input("\nPresiona ENTER para continuar...")
            
            else:
                print("\n❌ Opción inválida")
                input("Presiona ENTER para continuar...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido. ¡Hasta luego!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print(f"   Tipo: {type(e).__name__}")
            input("\nPresiona ENTER para continuar...")

if __name__ == "__main__":
    main()
