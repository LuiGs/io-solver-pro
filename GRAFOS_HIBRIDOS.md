# 🔥 Grafos Híbridos - Guía de Uso

## ¿Qué son los grafos híbridos?

Los **grafos híbridos** son aquellos que combinan aristas **bidireccionales** (↔) y **unidireccionales** (→) en el mismo grafo. Son muy útiles para modelar situaciones del mundo real como:

- 🚗 Redes de tráfico (calles bidireccionales + calles de un solo sentido)
- 🌐 Redes de comunicación (enlaces simétricos + enlaces asimétricos)
- 💧 Sistemas de tuberías (flujos bidireccionales + válvulas unidireccionales)
- ✈️ Rutas de transporte (rutas regulares + rutas especiales de un sentido)

## 📝 Formato de Entrada

### Sintaxis Básica

```
nodo1 nodo2 peso [sufijo]
```

### Sufijos Disponibles

| Sufijo | Comportamiento | Ejemplo | Resultado |
|--------|----------------|---------|-----------|
| **(ninguno)** | Depende del checkbox | `A B 5` | Bidireccional si checkbox OFF, Unidireccional si ON |
| `->` | **Forzar unidireccional** | `A B 5 ->` | Solo A→B (peso 5), ignora checkbox |
| `<->` o `<>` | **Forzar bidireccional** | `A B 5 <->` | A→B y B→A (peso 5), ignora checkbox |

## 🎯 Ejemplos Prácticos

### Ejemplo 1: Red de Tráfico Urbano

```
# Calles bidireccionales (mayoría)
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

# Calles de un solo sentido (excepciones)
6 4 1 ->
7 6 4 ->
```

**Interpretación:**
- Todas las calles son de doble sentido
- **EXCEPTO:** calle 6→4 y calle 7→6 que son de un solo sentido
- Perfecto para modelar centros históricos con restricciones de tráfico

### Ejemplo 2: Red de Vuelos

```
# Rutas regulares (ida y vuelta)
Madrid Barcelona 350
Barcelona Valencia 200
Valencia Sevilla 180

# Rutas especiales (solo ida por demanda)
IslasCanarias Madrid 800 ->
Sevilla IslasCanarias 750 ->
```

**Interpretación:**
- Rutas continentales: vuelos en ambas direcciones
- Desde Canarias solo hay vuelo directo a Madrid (no regreso directo)
- A Canarias solo hay vuelo directo desde Sevilla

### Ejemplo 3: Sistema de Riego

```
# Tuberías normales (flujo en ambas direcciones)
Embalse ZonaA 100
ZonaA ZonaB 80
ZonaB ZonaC 60

# Válvulas unidireccionales (anti-retorno)
Embalse EstacionBombeo 200 ->
EstacionBombeo ZonaD 150 ->
```

## 🔧 Uso en cada Módulo

### 1. Floyd-Warshall (Todas las rutas)
✅ **SOPORTA HÍBRIDO**

**Checkbox OFF** (recomendado para híbridos):
- Aristas normales → bidireccionales
- Aristas con `->` → unidireccionales

**Ejemplo:**
```
A B 5      # A↔B peso 5
C D 3 ->   # Solo C→D peso 3
E F 7      # E↔F peso 7
```

**Resultado:**
- Puede ir de A a B y de B a A (peso 5 en ambas)
- Puede ir de C a D (peso 3), pero NO de D a C
- Puede ir de E a F y de F a E (peso 7 en ambas)

### 2. Dijkstra (Ruta más corta)
✅ **SOPORTA HÍBRIDO**

Mismo comportamiento que Floyd-Warshall.

**Caso de uso:** Encontrar la ruta más corta desde un origen considerando que algunas calles son de un solo sentido.

### 3. Flujo Máximo (Ford-Fulkerson)
✅ **SOPORTA HÍBRIDO** (avanzado)

**Checkbox ON** (recomendado):
- Aristas normales → unidireccionales (típico en flujo)
- Aristas con `<->` → bidireccionales (tuberías especiales)

**Ejemplo:**
```
Fuente A 10     # Fuente→A capacidad 10
A B 5 <->       # A↔B capacidad 5 en ambas direcciones
B Sumidero 8    # B→Sumidero capacidad 8
```

### 4. Árbol Mínimo (Kruskal/Prim)
⚠️ **NO SOPORTA HÍBRIDO** (por definición)

Los árboles mínimos requieren grafos **completamente no dirigidos**. El sufijo `->` será ignorado.

**Razón:** Un árbol mínimo conecta todos los nodos con el mínimo peso total, usando aristas bidireccionales.

## 💡 Consejos de Uso

### ✅ Buenas Prácticas

1. **Checkbox OFF + sufijos `->` para híbridos:**
   ```
   # Mayoría bidireccionales, excepciones unidireccionales
   A B 5
   B C 3
   C D 2 ->   # Solo esta es unidireccional
   ```

2. **Usar sufijos para claridad:**
   Aunque el checkbox esté OFF, agregar `<->` a aristas bidireccionales mejora la legibilidad:
   ```
   A B 5 <->   # Explícitamente bidireccional
   C D 3 ->    # Explícitamente unidireccional
   ```

3. **Comentarios para documentar:**
   ```
   # Red principal (bidireccional)
   1 2 10
   2 3 15
   
   # Conexiones especiales (unidireccional)
   3 1 5 ->
   ```

### ❌ Errores Comunes

1. **Olvidar el sufijo cuando el checkbox está ON:**
   ```
   # ❌ Con checkbox ON (dirigido)
   A B 5      # Solo crea A→B
   
   # ✅ Si quieres bidireccional, agregar sufijo:
   A B 5 <->  # Crea A→B y B→A
   ```

2. **Sufijos en Árbol Mínimo:**
   ```
   # ⚠️ Funciona, pero el sufijo es ignorado
   A B 5 ->   # Se trata como A↔B
   ```

## 🎓 Ejercicios Propuestos

### Ejercicio 1: Campus Universitario
Modela un campus con:
- Pasillos bidireccionales entre edificios
- Escaleras mecánicas (solo suben) entre pisos
- Ascensores (bidireccionales) entre pisos

### Ejercicio 2: Red de Distribución
Modela una red de distribución con:
- Carreteras normales (bidireccionales)
- Autopistas con peajes (unidireccionales por sentido)
- Cálculo del camino más corto considerando restricciones

### Ejercicio 3: Sistema de Agua
Modela un sistema de distribución de agua con:
- Tuberías principales (bidireccionales)
- Válvulas anti-retorno (unidireccionales)
- Cálculo del flujo máximo desde la planta hasta los usuarios

## 🔍 Validación

Puedes verificar que el grafo híbrido se interpretó correctamente:

1. **En Floyd-Warshall:** Observa la matriz de distancias
   - Si `dist[A][B] ≠ dist[B][A]` → hay asimetría (correcto para híbridos)
   - Si `dist[A][B] = ∞` pero `dist[B][A] ≠ ∞` → arista unidireccional

2. **En Dijkstra:** Desde diferentes orígenes
   - Ejecuta desde nodo A y luego desde nodo B
   - Si las distancias difieren, confirmas aristas unidireccionales

3. **Visualización:** Usa el botón de visualizar
   - Aristas unidireccionales → flechas con dirección única
   - Aristas bidireccionales → líneas o flechas en ambas direcciones

## 📚 Referencias

- **Teoría de Grafos:** Los grafos híbridos son grafos mixtos (mixed graphs)
- **Aplicaciones:** Muy comunes en investigación operativa y optimización
- **Algoritmos:** Todos los algoritmos implementados soportan grafos dirigidos y no dirigidos

---

**Versión:** 1.0  
**Fecha:** Octubre 2025  
**Autor:** IO Solver Pro
