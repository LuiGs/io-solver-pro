# IO Solver Pro - Sistema de Resolución de Problemas de Investigación Operativa

Sistema completo de resolución de problemas de Investigación Operativa con interfaz gráfica desarrollado en Python.

## 🚀 Características

### Módulos Implementados

1. **Programación Lineal**
   - Método Simplex
   - Método de las Dos Fases
   - Análisis de sensibilidad

2. **Teoría de Grafos**
   - Algoritmo de Dijkstra (camino más corto)
   - Algoritmo de Floyd-Warshall (todos los caminos más cortos)
   - Algoritmo de Kruskal (árbol de expansión mínima)
   - Algoritmo de Prim (árbol de expansión mínima)

3. **Flujo Máximo en Redes**
   - Algoritmo de Ford-Fulkerson con DFS Greedy
   - Identificación de corte mínimo
   - Visualización de flujos
   - Salida paso a paso con notación académica

4. **Programación Entera**
   - Método de Branch and Bound
   - Resolución de problemas de optimización entera

5. **Teoría de Colas**
   - Modelos M/M/1, M/M/s
   - Análisis de sistemas de colas

6. **Cadenas de Markov**
   - Análisis de estados estacionarios
   - Matrices de transición

## 📋 Requisitos

```
Python 3.7+
```

### Dependencias

```bash
pip install -r requirements.txt
```

Incluye:
- `tkinter` - Interfaz gráfica
- `matplotlib` - Visualización de gráficos
- `networkx` - Manejo de grafos
- `numpy` - Cálculos numéricos
- `scipy` - Optimización

## 🔧 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/LuiGs/io-solver-pro.git
cd io-solver-pro
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
python3 interfaz_grafica.py
```

## 💻 Uso

### Módulo de Flujo Máximo

El módulo de Flujo Máximo utiliza el algoritmo de Ford-Fulkerson con estrategia DFS Greedy (prioriza arcos de mayor capacidad).

**Formato de entrada para aristas:**
```
origen->destino,capacidad
```

**Ejemplo:**
```
Nodo origen: 1
Nodo destino: 5

Aristas:
1->2,8
1->3,14
1->5,4
2->3,5
2->4,7
2->5,6
3->2,10
3->4,9
3->5,10
4->2,6
4->3,7
4->5,5
```

**Salida:**
- Rutas de avance paso a paso
- Cálculo de capacidades residuales
- Actualización de flujos (dirección forward y backward)
- Tabla de flujos óptimos con notación académica
- Visualización gráfica del grafo con flujos
- Identificación del corte mínimo

### Módulo de Floyd-Warshall

Calcula todos los caminos más cortos entre todos los pares de nodos usando matriz de predecesores.

**Formato de entrada:**
```
Aristas dirigidas: origen->destino,peso
Aristas no dirigidas: origen<->destino,peso
```

**Salida:**
- Matriz de distancias (D)
- Matriz de predecesores (P)
- Caminos reconstruidos para cada par de nodos

### Otros Módulos

Cada módulo incluye:
- Interfaz intuitiva con validación de entrada
- Visualización de resultados
- Exportación de soluciones

## 🎨 Interfaz

La aplicación cuenta con una interfaz gráfica moderna con:
- Pestañas para cada módulo
- Áreas de texto para entrada de datos
- Visualización de resultados paso a paso
- Gráficos interactivos

## 📐 Notación Académica

El sistema utiliza notación académica estándar:

**Flujo Máximo:**
- `cᵢⱼ` - Capacidad residual del arco (i,j)
- `C̄ᵢⱼ` - Capacidad de diseño (capacidad original)
- `fₚ` - Flujo en la ruta p
- `α` - Flujo óptimo
- `F` - Flujo máximo total

**Floyd-Warshall:**
- `D` - Matriz de distancias
- `P` - Matriz de predecesores

## 🛠️ Estructura del Proyecto

```
io-solver-pro/
├── interfaz_grafica.py      # Aplicación principal con GUI
├── algoritmos_grafos.py     # Algoritmos de teoría de grafos
├── solver_general.py        # Solvers de IO general
├── requirements.txt         # Dependencias del proyecto
└── README.md               # Este archivo
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**LuiGs**
- GitHub: [@LuiGs](https://github.com/LuiGs)

## 🙏 Agradecimientos

- Desarrollo basado en algoritmos clásicos de Investigación Operativa
- Implementación de Ford-Fulkerson adaptada de algoritmos académicos estándar
- Interfaz gráfica construida con tkinter

---

**Nota**: Este proyecto fue desarrollado con fines académicos para el curso de Investigación Operativa.
