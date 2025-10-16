#!/usr/bin/env python3
"""Script de prueba para verificar el parseo de Floyd-Warshall"""

def parsear_arista(linea, es_dirigido_global=False):
    """
    Parsea una arista con soporte para grafos híbridos.
    """
    partes = linea.strip().split()
    if len(partes) < 3:
        return None
    
    u, v = partes[0], partes[1]
    try:
        peso = float(partes[2])
    except ValueError:
        return None
    
    # Detectar sufijo de dirección
    sufijo = partes[3] if len(partes) >= 4 else None
    
    if sufijo == '->':
        # Forzar unidireccional
        es_bidireccional = False
    elif sufijo == '<->' or sufijo == '<>':
        # Forzar bidireccional
        es_bidireccional = True
    else:
        # Usar configuración global del checkbox
        es_bidireccional = not es_dirigido_global
    
    return (u, v, peso, es_bidireccional)

# Datos de entrada - EXACTAMENTE como deberían ingresarse
texto = """1 2 5
1 3 3
2 3 1
2 4 5
2 5 2
3 4 7
3 7 12
4 5 3
4 7 3
5 6 1
6 4 1 ->
7 6 4 ->"""

print("\n" + "="*60)
print("ANÁLISIS DE PARSEO - Checkbox OFF")
print("="*60)

grafo = {}
es_dirigido = False

for linea in texto.split('\n'):
    if linea.strip():
        resultado = parsear_arista(linea, es_dirigido)
        if resultado:
            u, v, peso, es_bidireccional = resultado
            
            # Agregar arista u -> v siempre
            if u not in grafo:
                grafo[u] = {}
            grafo[u][v] = peso
            
            direccion = "↔" if es_bidireccional else "→"
            print(f"{u} {direccion} {v} (peso: {peso})", end="")
            
            # Si es bidireccional, agregar también v -> u
            if es_bidireccional:
                if v not in grafo:
                    grafo[v] = {}
                grafo[v][u] = peso
                print(f" [Agregó también {v} → {u}]")
            else:
                print(f" [Solo {u} → {v}]")

print("\n" + "="*60)
print("GRAFO RESULTANTE:")
print("="*60)

for nodo in sorted(grafo.keys()):
    if grafo[nodo]:
        print(f"\n{nodo} tiene aristas hacia:")
        for vecino, peso in sorted(grafo[nodo].items()):
            print(f"  → {vecino} (peso: {peso})")
    else:
        print(f"\n{nodo} no tiene aristas salientes")

# Verificar aristas críticas
print("\n" + "="*60)
print("VERIFICACIÓN DE ARISTAS CRÍTICAS:")
print("="*60)

verificaciones = [
    ("6", "4", "Debe existir (6→4 con ->)"),
    ("4", "6", "NO debe existir (6→4 es unidireccional)"),
    ("7", "6", "Debe existir (7→6 con ->)"),
    ("6", "7", "NO debe existir (7→6 es unidireccional)"),
    ("1", "2", "Debe existir (bidireccional)"),
    ("2", "1", "Debe existir (bidireccional)"),
]

for u, v, descripcion in verificaciones:
    existe = u in grafo and v in grafo[u]
    esperado = "debe existir" in descripcion.lower()
    correcto = existe == esperado
    estado = "✅" if correcto else "❌"
    print(f"{estado} {u}→{v}: {descripcion}")
    print(f"   Esperado: {'Existe' if esperado else 'NO existe'} | Real: {'Existe' if existe else 'NO existe'}")

# Ejecutar Floyd-Warshall
print("\n" + "="*60)
print("EJECUTANDO FLOYD-WARSHALL...")
print("="*60)

from algoritmos_grafos import AlgoritmosGrafos

dist, next_node, nodos_lista, nodo_a_idx, iteraciones = AlgoritmosGrafos.floyd_warshall(grafo)

print("\n" + "="*60)
print("RESULTADO FINAL - TU SOFTWARE:")
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
print("RESULTADO ESPERADO - TU PROFESOR:")
print("="*60)

resultado_profesor = {
    ('1', '1'): 0.0, ('1', '2'): 4.0, ('1', '3'): 3.0, ('1', '4'): 8.0, ('1', '5'): 6.0, ('1', '6'): 7.0, ('1', '7'): 11.0,
    ('2', '1'): 5.0, ('2', '2'): 0.0, ('2', '3'): 1.0, ('2', '4'): 4.0, ('2', '5'): 2.0, ('2', '6'): 3.0, ('2', '7'): 7.0,
    ('3', '1'): 3.0, ('3', '2'): 1.0, ('3', '3'): 0.0, ('3', '4'): 5.0, ('3', '5'): 3.0, ('3', '6'): 4.0, ('3', '7'): 8.0,
    ('4', '1'): 9.0, ('4', '2'): 5.0, ('4', '3'): 6.0, ('4', '4'): 0.0, ('4', '5'): 3.0, ('4', '6'): 4.0, ('4', '7'): 3.0,
    ('5', '1'): 7.0, ('5', '2'): 2.0, ('5', '3'): 3.0, ('5', '4'): 2.0, ('5', '5'): 0.0, ('5', '6'): 1.0, ('5', '7'): 5.0,
    ('6', '1'): 8.0, ('6', '2'): 3.0, ('6', '3'): 4.0, ('6', '4'): 1.0, ('6', '5'): 1.0, ('6', '6'): 0.0, ('6', '7'): 4.0,
    ('7', '1'): 12.0, ('7', '2'): 7.0, ('7', '3'): 8.0, ('7', '4'): 3.0, ('7', '5'): 5.0, ('7', '6'): 4.0, ('7', '7'): 0.0,
}

print("      ", end="")
for nodo in nodos_lista:
    print(f"{str(nodo):>6}", end="")
print()

for i, nodo in enumerate(nodos_lista):
    print(f"{str(nodo):>4}:", end="")
    for j, nodo_j in enumerate(nodos_lista):
        val = resultado_profesor.get((str(nodo), str(nodo_j)), float('inf'))
        if val == float('inf'):
            print("   ∞  ", end="")
        else:
            print(f"{val:>6.1f}", end="")
    print()

print("\n" + "="*60)
print("COMPARACIÓN - DIFERENCIAS:")
print("="*60)

diferencias = []
posiciones_criticas = [('2', '1'), ('5', '1'), ('6', '1'), ('7', '1')]

for i, nodo_i in enumerate(nodos_lista):
    for j, nodo_j in enumerate(nodos_lista):
        val_software = dist[i][j]
        val_profesor = resultado_profesor.get((str(nodo_i), str(nodo_j)), float('inf'))
        if abs(val_software - val_profesor) > 0.01:
            diferencias.append((nodo_i, nodo_j, val_software, val_profesor))
            print(f"❌ D[{nodo_i}][{nodo_j}]: Tu software={val_software:.1f}, Profesor={val_profesor:.1f}")

if not diferencias:
    print("✅ ¡PERFECTO! Todos los valores coinciden.")
else:
    print(f"\n❌ Total de diferencias: {len(diferencias)}")
    
    # Analizar en qué iteración aparecen las diferencias
    print("\n" + "="*60)
    print("ANÁLISIS POR ITERACIÓN - Posiciones críticas:")
    print("="*60)
    
    for k_iter in iteraciones:
        k = k_iter['k']
        matriz_d = k_iter['matriz_d']
        nodo_inter = k_iter.get('nodo_intermedio', 'Inicial')
        
        print(f"\nK={k} (Nodo intermedio: {nodo_inter}):")
        
        for nodo_str_i, nodo_str_j in posiciones_criticas:
            i = nodo_a_idx[nodo_str_i]
            j = nodo_a_idx[nodo_str_j]
            val_soft = matriz_d[i][j]
            val_prof = resultado_profesor.get((nodo_str_i, nodo_str_j), float('inf'))
            
            if abs(val_soft - val_prof) > 0.01:
                print(f"  ❌ D[{nodo_str_i}][{nodo_str_j}]: Software={val_soft:.1f} vs Profesor={val_prof:.1f}")
            else:
                print(f"  ✅ D[{nodo_str_i}][{nodo_str_j}]: {val_soft:.1f} (coincide)")
