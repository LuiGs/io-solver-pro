#!/usr/bin/env python3
"""
Test Floyd-Warshall con el segundo ejemplo
"""

from algoritmos_grafos import AlgoritmosGrafos

# Construir el grafo EXACTAMENTE como lo interpreta TORA
# (solo aristas dirigidas, sin reversas)
grafo = {
    '1': {'2': 3.0, '3': 10.0},
    '2': {'4': 5.0},
    '3': {'4': 6.0, '5': 15.0},
    '4': {'5': 4.0},
    '5': {}
}

print("="*60)
print("GRAFO DIRIGIDO (como TORA):")
print("="*60)
for nodo, vecinos in sorted(grafo.items()):
    if vecinos:
        for vecino, peso in vecinos.items():
            print(f"  {nodo} → {vecino} (peso: {peso})")
    else:
        print(f"  {nodo} (sin aristas salientes)")

print("\n" + "="*60)
print("EJECUTANDO FLOYD-WARSHALL...")
print("="*60)

dist, next_node, nodos_lista, nodo_a_idx, iteraciones = AlgoritmosGrafos.floyd_warshall(grafo)

print("\n" + "="*60)
print("RESULTADO - TU SOFTWARE:")
print("="*60)

n = len(nodos_lista)
print("      ", end="")
for nodo in nodos_lista:
    print(f"{str(nodo):>6}", end="")
print()

for i, nodo in enumerate(nodos_lista):
    print(f"{str(nodo):>4}:", end="")
    for j in range(n):
        val = dist[i][j]
        if val == float('inf'):
            print("   ∞  ", end="")
        else:
            print(f"{val:>6.1f}", end="")
    print()

print("\n" + "="*60)
print("RESULTADO ESPERADO - TORA:")
print("="*60)

resultado_tora = {
    ('1', '1'): 0.0, ('1', '2'): 3.0, ('1', '3'): 10.0, ('1', '4'): 8.0, ('1', '5'): 12.0,
    ('2', '1'): 3.0, ('2', '2'): 0.0, ('2', '3'): 11.0, ('2', '4'): 5.0, ('2', '5'): 9.0,
    ('3', '1'): 10.0, ('3', '2'): 13.0, ('3', '3'): 0.0, ('3', '4'): 6.0, ('3', '5'): 10.0,
    ('4', '1'): 6.0, ('4', '2'): 19.0, ('4', '3'): 6.0, ('4', '4'): 0.0, ('4', '5'): 4.0,
    ('5', '1'): 20.0, ('5', '2'): 23.0, ('5', '3'): 10.0, ('5', '4'): 4.0, ('5', '5'): 0.0,
}

print("      ", end="")
for nodo in nodos_lista:
    print(f"{str(nodo):>6}", end="")
print()

for i, nodo in enumerate(nodos_lista):
    print(f"{str(nodo):>4}:", end="")
    for j, nodo_j in enumerate(nodos_lista):
        val = resultado_tora.get((str(nodo), str(nodo_j)), float('inf'))
        if val == float('inf'):
            print("   ∞  ", end="")
        else:
            print(f"{val:>6.1f}", end="")
    print()

print("\n" + "="*60)
print("COMPARACIÓN - DIFERENCIAS:")
print("="*60)

diferencias = []
for i, nodo_i in enumerate(nodos_lista):
    for j, nodo_j in enumerate(nodos_lista):
        val_software = dist[i][j]
        val_tora = resultado_tora.get((str(nodo_i), str(nodo_j)), float('inf'))
        if abs(val_software - val_tora) > 0.01:
            diferencias.append((nodo_i, nodo_j, val_software, val_tora))
            print(f"❌ D[{nodo_i}][{nodo_j}]: Tu software={val_software:.1f}, TORA={val_tora:.1f}")

if not diferencias:
    print("✅ ¡PERFECTO! Todos los valores coinciden con TORA.")
else:
    print(f"\n❌ Total de diferencias: {len(diferencias)}")
