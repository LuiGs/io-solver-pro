# 🎯 Mejoras en Floyd-Warshall

## ✨ Nuevas Funcionalidades Implementadas

### 1. 📊 Visualización de AMBAS Matrices (D y S)

**Antes:** Solo se mostraba la matriz D (distancias)

**Ahora:** En cada iteración K se muestran:

#### Matriz D (Distancias)
```
   📐 MATRIZ D (Distancias):
         1     2     3     4     5
   1:   0.0   3.0   8.0   4.0  -4.0
   2:   ∞     0.0   ∞     1.0   7.0
   3:   ∞     4.0   0.0   ∞     ∞
   4:   2.0   ∞    -5.0   0.0   ∞
   5:   ∞     ∞     ∞     6.0   0.0
```

#### Matriz S (Sucesores/Next)
```
   🧭 MATRIZ S (Sucesores):
         1     2     3     4     5
   1:   -     2     3     5     5
   2:   -     -     -     4     5
   3:   -     2     -     -     -
   4:   1     -     3     -     -
   5:   -     -     -     4     -
```

**¿Qué es la Matriz S?**
- Cada celda `S[i][j]` contiene el **próximo nodo** en el camino más corto de `i` a `j`
- Si `S[i][j] = k`, significa que para ir de `i` a `j`, el siguiente paso es ir al nodo `k`
- Usada para **reconstruir el camino completo** entre dos nodos
- `-` indica que no hay camino o que `i = j`

### 2. 🔍 Consulta de Ruta Específica

Nueva sección en la interfaz para consultar **rutas individuales** después de ejecutar Floyd-Warshall:

```
┌─────────────────────────────────────────────┐
│  🔍 Consultar Ruta Específica               │
├─────────────────────────────────────────────┤
│  Origen: [___]  Destino: [___]              │
│  [ 📍 Consultar Ruta ]                      │
└─────────────────────────────────────────────┘
```

#### Características:

✅ **Distancia exacta** entre los dos nodos  
✅ **Camino completo** paso a paso  
✅ **Distancia por segmento** de cada tramo  
✅ **Ventana emergente** con formato profesional

#### Ejemplo de Salida:

```
╔══════════════════════════════════════════════════════╗
║  RUTA ESPECÍFICA: 1 → 3
╚══════════════════════════════════════════════════════╝

📍 ORIGEN:    1
🎯 DESTINO:   3
📏 DISTANCIA: -1.00

🛣️  CAMINO COMPLETO:
    1 → 5 → 4 → 3

📊 DETALLES POR SEGMENTO:
    Paso 1: 1 → 5  (distancia: -4.00)
    Paso 2: 5 → 4  (distancia: 6.00)
    Paso 3: 4 → 3  (distancia: -5.00)

======================================================
✅ DISTANCIA TOTAL: -1.00
======================================================
```

### 3. 📈 Formato de Iteraciones Mejorado

**Nueva estructura para cada iteración K:**

```
============================================================
🔵 ITERACIÓN K=1 (nodo intermedio: 1)
============================================================

   📝 Cambios realizados: 3
      • 2→3: ∞ → 12.0 (vía 1)
      • 3→4: ∞ → 10.0 (vía 1)
      • 4→2: ∞ → 5.0 (vía 1)

   📐 MATRIZ D (Distancias):
      ...

   🧭 MATRIZ S (Sucesores):
      ...
```

**Elementos incluidos:**
- ✅ Número de iteración K claramente visible
- ✅ Nodo intermedio usado en esta iteración
- ✅ Lista de cambios realizados (con límite para no saturar)
- ✅ Ambas matrices actualizadas
- ✅ Separadores visuales entre iteraciones

## 🎮 Cómo Usar

### Paso 1: Ejecutar Floyd-Warshall

1. Ve a la pestaña **"Floyd-Warshall"**
2. Ingresa tu grafo (soporta híbridos con `->`)
3. Haz clic en **"🔄 Ejecutar Floyd-Warshall"**
4. Observa las matrices D y S en cada iteración K

### Paso 2: Consultar Ruta Específica

1. **Después** de ejecutar Floyd-Warshall
2. En la sección **"🔍 Consultar Ruta Específica"**
3. Ingresa el nodo **Origen** (ej: `1`)
4. Ingresa el nodo **Destino** (ej: `3`)
5. Haz clic en **"📍 Consultar Ruta"**
6. ¡Verás una ventana emergente con todos los detalles!

### Ejemplo Completo

#### Entrada (Grafo Híbrido):
```
1 2 5
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
7 6 4 ->
```

#### Paso a Paso:
1. **Ejecuta Floyd-Warshall** → Verás matrices D y S para cada K
2. **Consulta ruta específica:** Origen=`1`, Destino=`6`
3. **Resultado:** Camino completo con distancias

## 📊 Matriz S: Interpretación

### ¿Cómo leer la Matriz S?

**Ejemplo:** Si `S[1][6] = 2`

Significa: Para ir de nodo `1` a nodo `6`, el **siguiente paso** es ir al nodo `2`

### Reconstrucción Manual del Camino

Para encontrar el camino de **1 a 6** usando la matriz S:

```
1. Empezar en nodo 1
2. S[1][6] = 2  →  siguiente es 2  →  camino: [1, 2]
3. S[2][6] = 5  →  siguiente es 5  →  camino: [1, 2, 5]
4. S[5][6] = 6  →  siguiente es 6  →  camino: [1, 2, 5, 6]
5. Llegamos al destino!
```

**Camino final:** `1 → 2 → 5 → 6`

### Casos Especiales en Matriz S

| Valor en S[i][j] | Significado |
|------------------|-------------|
| `None` o `-` | No hay camino de i a j |
| `j` (destino) | Hay arista directa de i a j |
| `k` (otro nodo) | Para ir de i a j, ir primero a k |

## 🔧 Detalles Técnicos

### Cambios en `algoritmos_grafos.py`

**Modificación en `floyd_warshall()`:**

```python
# Antes: Solo guardaba matriz_d
iteraciones.append({
    'k': k + 1,
    'nodo_intermedio': nodos[k],
    'matriz': [row[:] for row in dist],
    'cambios': cambios
})

# Ahora: Guarda matriz_d Y matriz_s
iteraciones.append({
    'k': k + 1,
    'nodo_intermedio': nodos[k],
    'matriz_d': [row[:] for row in dist],
    'matriz_s': [[next_node[i][j] for j in range(n)] for i in range(n)],
    'cambios': cambios
})
```

### Cambios en `interfaz_grafica.py`

1. **Nuevas variables de instancia:**
   ```python
   self.floyd_dist = None      # Matriz de distancias final
   self.floyd_next = None      # Matriz de sucesores final
   self.floyd_nodos = None     # Lista de nodos
   self.floyd_nodo_a_idx = None # Diccionario nodo → índice
   ```

2. **Nuevo método `consultar_ruta_floyd()`:**
   - Valida que Floyd-Warshall se haya ejecutado
   - Obtiene origen y destino del usuario
   - Reconstruye el camino usando la matriz S
   - Calcula distancias por segmento
   - Muestra resultado en ventana emergente

3. **Nuevo método `_reconstruir_camino_floyd()`:**
   - Usa la matriz de sucesores (next_node)
   - Protección contra bucles infinitos
   - Retorna lista ordenada de nodos en el camino

## 💡 Casos de Uso

### Caso 1: Red de Transporte Urbano
```
Objetivo: Encontrar la ruta más corta de la Estación A a la Estación F
Método: 
1. Ejecutar Floyd-Warshall en toda la red
2. Consultar ruta específica A → F
3. Obtener camino y tiempo total
```

### Caso 2: Red de Comunicaciones
```
Objetivo: Ver todas las rutas posibles entre routers
Método:
1. Ejecutar Floyd-Warshall (calcula todas las rutas)
2. Analizar matriz D para ver latencias
3. Analizar matriz S para ver rutas específicas
```

### Caso 3: Análisis de Grafos Híbridos
```
Objetivo: Red con calles bidireccionales y de un sentido
Entrada: Usar formato híbrido con sufijos ->
Resultado: Rutas considerando restricciones de dirección
```

## 🎓 Conceptos Teóricos

### Floyd-Warshall: Programación Dinámica

**Principio:** Para cada par de nodos (i, j), considerar si usar un nodo intermedio k mejora la distancia.

**Fórmula:**
```
D[i][j] = min(D[i][j], D[i][k] + D[k][j])
```

**Complejidad:** O(n³) donde n = número de nodos

### Matriz de Sucesores (S)

**Actualización:** Cuando D[i][j] mejora usando k como intermedio:
```
S[i][j] = S[i][k]
```

Esto significa: "Para ir de i a j, toma el mismo camino que de i a k"

### Ventajas de la Matriz S

✅ Reconstrucción de caminos en O(n)  
✅ No necesita búsqueda adicional  
✅ Camino completo almacenado implícitamente  
✅ Eficiente en espacio: O(n²)

## 📚 Referencias

- **Algoritmo:** Floyd-Warshall (1962)
- **Complejidad temporal:** O(n³)
- **Complejidad espacial:** O(n²)
- **Tipo:** Programación Dinámica
- **Soporta:** Pesos negativos (sin ciclos negativos)

## ✅ Checklist de Funcionalidades

- [x] Visualización de Matriz D en cada iteración K
- [x] Visualización de Matriz S en cada iteración K
- [x] Interfaz para consultar ruta específica
- [x] Reconstrucción del camino completo
- [x] Cálculo de distancia por segmento
- [x] Ventana emergente con resultado formateado
- [x] Validación de nodos existentes
- [x] Manejo de casos especiales (sin camino, mismo nodo)
- [x] Soporte para grafos híbridos
- [x] Guardado de resultados para consultas múltiples

---

**Versión:** 2.0  
**Fecha:** Octubre 2025  
**Mejoras:** Matrices D y S completas + Consulta de rutas específicas
