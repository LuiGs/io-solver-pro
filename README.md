# 🎯 IO Solver Pro

**Herramienta moderna para Investigación Operativa** - Interfaz profesional, potente y gratuita

![Python](https://img.shields.io/badge/Python-3.9+-3498db?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-27ae60?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production-27ae60?style=flat-square)

---

## ⚡ Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar interfaz gráfica (recomendado)
python3 interfaz_grafica.py

# O ejecutar en terminal
python3 solver_general.py
```

**Requisitos:** Python 3.9+

---

## ✨ Módulos Incluidos

| Módulo | Descripción |
|:---|:---|
| 🌳 **Árbol Mínimo** | Kruskal y Prim con visualización paso a paso |
| 🚗 **Rutas Cortas** | Dijkstra con SPT (Shortest Path Tree) y peso total |
| 🌐 **Floyd-Warshall** | Todas las rutas más cortas (grafos dirigidos/no dirigidos) |
| 💧 **Flujo Máximo** | Ford-Fulkerson con corte mínimo |
| 🎲 **Juegos** | Estrategias mixtas para ambos jugadores |
| 📊 **Prog. Lineal** | Simplex con variables continuas/enteras/binarias |

---

## 🎯 Características Principales

### 🌳 Shortest Path Tree (SPT)
El algoritmo de Dijkstra incluye visualización del árbol de caminos más cortos:
- **Visualización dual**: Grafo completo + SPT aislado
- **Aristas destacadas**: SPT en rojo para fácil identificación
- **Peso total**: Suma automática de todos los pesos del árbol
- **Información detallada**: Raíz, nodos alcanzables, lista de aristas

### 📊 Iteraciones Paso a Paso
Todos los algoritmos muestran su proceso de resolución estilo TORA:
- **Kruskal/Prim**: Cada arista evaluada, decisión y peso acumulado
- **Dijkstra**: Exploración nodo por nodo con actualizaciones de distancias
- **Floyd-Warshall**: Matrices de distancias en cada iteración
- **Educativo**: Ideal para aprender cómo funcionan los algoritmos

### 🎨 Interfaz Moderna
- Diseño profesional con paleta de 7 colores
- Navegación intuitiva por pestañas
- Ejemplos predefinidos para cada algoritmo
- Instrucciones claras en cada módulo

### 📈 Visualización Avanzada
- Gráficos interactivos con matplotlib
- Grafos dirigidos con aristas curvas (evita superposiciones)
- Mapas de calor para juegos de suma cero
- 4 tipos de visualización para juegos (barras, radar, heatmap, tabla)

---

## 📖 Ejemplos de Uso

### Dijkstra con SPT

**Entrada:**
```
Origen: A
Grafo:
  A → B: 4, A → C: 2
  C → B: 1, C → D: 8, C → E: 10
  B → D: 5, D → E: 2
```

**Resultado:**
```
Distancias mínimas:
  A → A: 0
  A → B: 3 (camino: A → C → B)
  A → C: 2 (camino: A → C)
  A → D: 8 (camino: A → C → B → D)
  A → E: 10 (camino: A → C → B → D → E)

SPT:
  Nodo raíz: A
  Aristas: A→C (2), C→B (1), B→D (5), D→E (2)
  Peso total del SPT: 10
```

### Juego de Suma Cero

**Entrada:**
```
3 -1  2
1  4 -2
2  1  3
```

**Resultado:**
- 🎮 **Jugador A**: E2=25%, E3=75% (no jugar E1)
- 🎯 **Jugador B**: E1=65%, E2=30%, E3=5%
- 💰 **Valor del juego**: 1.75 (favorece al jugador A)
- 📊 4 visualizaciones: barras, radar, heatmap, tabla

### Programación Lineal

**Problema:**
```
Maximizar: Z = 3x₁ + 5x₂
Sujeto a:
  2x₁ + 1x₂ ≤ 10
  1x₁ + 2x₂ ≤ 8
  x₁ ≤ 4, x₂ ≤ 5
  x₁, x₂ ≥ 0
```

**Resultado:**
```
✅ Solución óptima:
   x₁ = 4.0
   x₂ = 2.0
   Z* = 22.0

Variables básicas: x₁, x₂
Variables no básicas: holguras
```

---

## 🆚 Ventajas vs TORA

| Característica | TORA | IO Solver Pro |
|:---|:---:|:---:|
| Programación Lineal | ✅ | ✅ |
| Variables Enteras/Binarias | ✅ | ✅ |
| Juegos (ambos jugadores) | ⚠️ | ✅ |
| Visualización Moderna | ❌ | ✅ |
| Iteraciones Paso a Paso | ✅ | ✅ |
| Grafos Dirigidos/No Dirigidos | ⚠️ | ✅ |
| SPT con Peso Total | ❌ | ✅ |
| Open Source | ❌ | ✅ |
| Gratuito | ❌ | ✅ |
| Multiplataforma | ⚠️ | ✅ |

---

## 🛠️ Tecnologías

- **Python 3.9+** - Lenguaje principal
- **NumPy** - Cálculos numéricos eficientes
- **NetworkX** - Algoritmos de grafos
- **Matplotlib** - Visualizaciones profesionales
- **SciPy** - Método simplex para programación lineal
- **Tkinter** - Interfaz gráfica nativa

---

## 📦 Estructura del Proyecto

```
io-solver-pro/
├── interfaz_grafica.py    # Interfaz gráfica moderna (GUI)
├── solver_general.py       # Interfaz de terminal (CLI)
├── algoritmos_grafos.py    # Implementaciones de algoritmos
├── requirements.txt        # Dependencias del proyecto
├── LICENSE                 # Licencia MIT
└── README.md              # Esta documentación
```

---

## 💻 Modos de Uso

### 1. Interfaz Gráfica (Recomendado)
```bash
python3 interfaz_grafica.py
```
- Interfaz moderna con pestañas
- Visualización interactiva con matplotlib
- Perfecto para reportes y presentaciones
- Ejemplos predefinidos en cada módulo

### 2. Terminal (CLI)
```bash
python3 solver_general.py
```
- Menú interactivo en consola
- Ideal para uso en servidores
- Sin dependencias gráficas

### 3. Uso Programático
```python
from algoritmos_grafos import dijkstra, kruskal, prim, floyd_warshall

# Ejemplo: Dijkstra
grafo = {'A': {'B': 4, 'C': 2}, 'B': {'D': 5}, 'C': {'B': 1, 'D': 8}, 'D': {}}
distancias, predecesores, iteraciones = dijkstra(grafo, 'A')
print(f"Distancias: {distancias}")
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:
1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📞 Soporte

### Problemas Comunes

**Error: No module named 'numpy'**
```bash
pip install --upgrade numpy networkx matplotlib scipy
```

**Error: tkinter no disponible (macOS)**
```bash
brew install python-tk
```

**Error: matplotlib no muestra gráficos**
```bash
# Cambiar backend en ~/.matplotlib/matplotlibrc
backend: TkAgg
```

---

## 🚀 Roadmap

### Próximas Características
- [ ] Algoritmo de Bellman-Ford
- [ ] A* (A estrella) para grafos
- [ ] Exportar resultados a PDF
- [ ] Tema oscuro/claro
- [ ] Importar grafos desde archivo
- [ ] Tests unitarios completos

---

## 🎉 Versión Actual

**v2.1.0** - Shortest Path Tree + Peso Total (Octubre 2025)

### Cambios Recientes
- ✅ Shortest Path Tree con visualización dual
- ✅ Peso total del SPT en texto y panel visual
- ✅ Iteraciones paso a paso para todos los algoritmos
- ✅ Soporte completo para grafos dirigidos/no dirigidos
- ✅ Interfaz moderna con diseño profesional

---

**¡Listo para usar!** Ejecuta `python3 interfaz_grafica.py` y comienza a resolver problemas de IO. 🚀
