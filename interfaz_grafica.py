"""
Interfaz Gráfica GENERALIZADA para Resolver Problemas de Grafos e Investigación Operativa

Esta herramienta te permite resolver CUALQUIER problema de:
- Árboles de expansión mínima (Kruskal/Prim)
- Rutas más cortas (Dijkstra/Floyd-Warshall)
- Flujo máximo (Ford-Fulkerson)
- Juegos de suma cero

Solo necesitas ingresar tus propios datos.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from algoritmos_grafos import AlgoritmosGrafos
import numpy as np
import sys
from io import StringIO
from scipy.optimize import linprog

class AplicacionGrafos:
    def __init__(self, root):
        self.root = root
        self.root.title("IO Solver Pro - Investigación Operativa")
        self.root.geometry("1400x900")
        
        # Paleta de colores moderna
        self.colors = {
            'primary': '#2C3E50',      # Azul oscuro profesional
            'secondary': '#3498DB',    # Azul brillante
            'success': '#27AE60',      # Verde
            'warning': '#F39C12',      # Naranja
            'danger': '#E74C3C',       # Rojo
            'light': '#ECF0F1',        # Gris claro
            'dark': '#34495E',         # Gris oscuro
            'white': '#FFFFFF',        # Blanco
            'accent': '#9B59B6'        # Púrpura
        }
        
        # Configurar estilo moderno
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilos personalizados para el notebook
        style.configure('TNotebook', background=self.colors['light'], borderwidth=0)
        style.configure('TNotebook.Tab', 
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['light'])
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', self.colors['white']), ('!selected', self.colors['dark'])])
        
        # Estilos para frames
        style.configure('Card.TFrame', background=self.colors['white'], relief='flat')
        style.configure('TFrame', background=self.colors['light'])
        
        # Estilos para labels
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 18, 'bold'),
                       foreground=self.colors['primary'],
                       background=self.colors['white'])
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 11),
                       foreground=self.colors['dark'],
                       background=self.colors['white'])
        style.configure('TLabel', background=self.colors['white'])
        
        # Estilos para botones
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10,
                       background=self.colors['secondary'])
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary'])])
        
        style.configure('Success.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10,
                       background=self.colors['success'])
        
        # Variables para guardar resultados
        self.ultimo_grafo = None
        self.ultimo_resultado = None
        
        # Variables para Floyd-Warshall (consultas de ruta)
        self.floyd_dist = None
        self.floyd_next = None
        self.floyd_nodos = None
        self.floyd_nodo_a_idx = None
        
        # Configurar root background
        self.root.configure(bg=self.colors['light'])
        
        # Header
        self._crear_header()
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        # Crear pestañas
        self.crear_pestaña_arbol_minimo()
        self.crear_pestaña_rutas_cortas()
        self.crear_pestaña_floyd_warshall()
        self.crear_pestaña_flujo_maximo()
        self.crear_pestaña_suma_cero()
        self.crear_pestaña_programacion_lineal()
        
        # Barra de estado moderna
        self._crear_status_bar()
    
    def _crear_header(self):
        """Crea un header moderno y profesional"""
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill='x', padx=0, pady=0)
        header.pack_propagate(False)
        
        # Contenedor interno con padding
        header_content = tk.Frame(header, bg=self.colors['primary'])
        header_content.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Título principal
        title = tk.Label(header_content,
                        text="IO SOLVER PRO",
                        font=('Segoe UI', 24, 'bold'),
                        fg=self.colors['white'],
                        bg=self.colors['primary'])
        title.pack(side='left')
        
        # Subtítulo
        subtitle = tk.Label(header_content,
                           text="Herramientas de Investigación Operativa",
                           font=('Segoe UI', 11),
                           fg=self.colors['light'],
                           bg=self.colors['primary'])
        subtitle.pack(side='left', padx=(15, 0))
        
        # Versión
        version = tk.Label(header_content,
                          text="v2.0",
                          font=('Segoe UI', 9),
                          fg=self.colors['secondary'],
                          bg=self.colors['primary'])
        version.pack(side='right')
    
    def _crear_status_bar(self):
        """Crea una barra de estado moderna"""
        status_frame = tk.Frame(self.root, bg=self.colors['primary'], height=35)
        status_frame.pack(side='bottom', fill='x')
        status_frame.pack_propagate(False)
        
        self.status_bar = tk.Label(status_frame,
                                   text="●  Listo para resolver problemas",
                                   font=('Segoe UI', 9),
                                   fg=self.colors['white'],
                                   bg=self.colors['primary'],
                                   anchor='w',
                                   padx=20)
        self.status_bar.pack(fill='both', expand=True)
    
    def _actualizar_status(self, mensaje, tipo='info'):
        """Actualiza la barra de estado con colores según el tipo"""
        iconos = {
            'info': '●',
            'success': '✓',
            'warning': '⚠',
            'error': '✗',
            'loading': '⟳'
        }
        colores = {
            'info': self.colors['secondary'],
            'success': self.colors['success'],
            'warning': self.colors['warning'],
            'error': self.colors['danger'],
            'loading': self.colors['accent']
        }
        
        icono = iconos.get(tipo, '●')
        color = colores.get(tipo, self.colors['secondary'])
        
        self.status_bar.config(text=f"{icono}  {mensaje}", fg=color)
    
    def _parsear_arista(self, linea, es_dirigido_global=False):
        """
        Parsea una arista con soporte para grafos híbridos.
        
        Formato:
        - "A B 5"     → Bidireccional si es_dirigido_global=False, Unidireccional si True
        - "A B 5 ->"  → SIEMPRE unidireccional A→B (ignora checkbox)
        - "A B 5 <->" → SIEMPRE bidireccional A↔B (ignora checkbox)
        
        Retorna: (u, v, peso, es_bidireccional)
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
        
    def crear_pestaña_arbol_minimo(self):
        """Pestaña para Kruskal y Prim"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🌳 Árbol Mínimo")
        
        # Panel izquierdo: Entrada
        frame_izq = ttk.LabelFrame(frame, text="Entrada de Datos", padding=10)
        frame_izq.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(frame_izq, text="Ingrese las aristas (formato: nodo1 nodo2 peso):", 
                 font=('Arial', 11, 'bold')).pack(anchor='w', pady=5)
        
        # Frame para instrucciones y ejemplos
        frame_info = ttk.LabelFrame(frame_izq, text="ℹ️ Formato de Entrada", padding=5)
        frame_info.pack(fill='x', pady=5)
        
        ttk.Label(frame_info, text="• Una arista por línea: nodo1 nodo2 peso", 
                 font=('Arial', 10)).pack(anchor='w')
        ttk.Label(frame_info, text="• Los nodos pueden ser letras (A,B,C) o números (1,2,3)", 
                 font=('Arial', 10)).pack(anchor='w')
        ttk.Label(frame_info, text="• El peso puede ser decimal (ej: 5.5)", 
                 font=('Arial', 10)).pack(anchor='w')
        
        # Botones de ejemplo
        frame_ejemplos = ttk.Frame(frame_izq)
        frame_ejemplos.pack(fill='x', pady=5)
        ttk.Label(frame_ejemplos, text="Cargar ejemplo:", font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        ttk.Button(frame_ejemplos, text="Pequeño", 
                  command=lambda: self.txt_aristas.delete('1.0', 'end') or 
                  self.txt_aristas.insert('1.0', "A B 4\nA C 3\nB C 1\nB D 2\nC D 4")).pack(side='left', padx=2)
        ttk.Button(frame_ejemplos, text="Mediano", 
                  command=lambda: self.cargar_ejemplo_mediano_mst()).pack(side='left', padx=2)
        ttk.Button(frame_ejemplos, text="Limpiar", 
                  command=lambda: self.txt_aristas.delete('1.0', 'end')).pack(side='left', padx=2)
        
        self.txt_aristas = scrolledtext.ScrolledText(frame_izq, height=15, width=40, font=('Consolas', 11))
        self.txt_aristas.pack(fill='both', expand=True, pady=5)
        
        # Botones
        frame_botones = ttk.Frame(frame_izq)
        frame_botones.pack(pady=10)
        
        ttk.Button(frame_botones, text="🔍 Kruskal", 
                  command=lambda: self.ejecutar_arbol_minimo('kruskal'),
                  width=15).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="🔍 Prim", 
                  command=lambda: self.ejecutar_arbol_minimo('prim'),
                  width=15).pack(side='left', padx=5)
        
        frame_botones2 = ttk.Frame(frame_izq)
        frame_botones2.pack(pady=5)
        
        ttk.Button(frame_botones2, text="📊 Comparar Ambos", 
                  command=self.comparar_algoritmos_mst,
                  width=15).pack(side='left', padx=5)
        ttk.Button(frame_botones2, text="💾 Guardar Resultado", 
                  command=lambda: self.guardar_resultado(self.txt_resultado_mst.get('1.0', 'end')),
                  width=15).pack(side='left', padx=5)
        ttk.Button(frame_botones2, text="🗑️ Limpiar", 
                  command=lambda: self.txt_resultado_mst.delete('1.0', 'end'),
                  width=15).pack(side='left', padx=5)
        
        # Panel derecho: Resultados
        frame_der = ttk.LabelFrame(frame, text="Resultados", padding=10)
        frame_der.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        self.txt_resultado_mst = scrolledtext.ScrolledText(frame_der, height=20, width=60, font=('Consolas', 11))
        self.txt_resultado_mst.pack(fill='both', expand=True)
        
        # Canvas para gráfico
        self.canvas_mst = None
        
    def crear_pestaña_rutas_cortas(self):
        """Pestaña para Dijkstra"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🛣️ Rutas Cortas (Dijkstra)")
        
        # Panel izquierdo
        frame_izq = ttk.LabelFrame(frame, text="Entrada de Datos", padding=10)
        frame_izq.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(frame_izq, text="Ingrese las aristas (formato: nodo1 nodo2 peso):", 
                 font=('Arial', 11, 'bold')).pack(anchor='w', pady=5)
        
        # Frame para instrucciones
        frame_info_d = ttk.LabelFrame(frame_izq, text="ℹ️ Información Importante", padding=5)
        frame_info_d.pack(fill='x', pady=5)
        
        ttk.Label(frame_info_d, text="⚠️  Dijkstra NO funciona con pesos negativos", 
                 font=('Arial', 9, 'bold'), foreground='red').pack(anchor='w')
        
        ttk.Label(frame_info_d, text="📌 GRAFOS DIRIGIDOS (marcar checkbox):", 
                 font=('Arial', 9, 'bold'), foreground='#2C3E50').pack(anchor='w', pady=(5, 2))
        ttk.Label(frame_info_d, text="   • Cada línea es UNA arista con dirección única", 
                 font=('Arial', 10)).pack(anchor='w')
        ttk.Label(frame_info_d, text="   • Ejemplo: 2 6 6 significa 2→6 con peso 6", 
                 font=('Arial', 10)).pack(anchor='w')
        
        ttk.Label(frame_info_d, text="📌 GRAFOS NO DIRIGIDOS (sin marcar):", 
                 font=('Arial', 10, 'bold'), foreground='#2C3E50').pack(anchor='w', pady=(5, 2))
        ttk.Label(frame_info_d, text="   • Cada línea crea aristas en AMBAS direcciones", 
                 font=('Arial', 10)).pack(anchor='w')
        ttk.Label(frame_info_d, text="   • Ejemplo: A B 5 crea A→B y B→A (ambas peso 5)", 
                 font=('Arial', 10)).pack(anchor='w')
        
        ttk.Label(frame_info_d, text="� GRAFOS HÍBRIDOS (mezclar ambos):", 
                 font=('Arial', 10, 'bold'), foreground='#E74C3C').pack(anchor='w', pady=(5, 2))
        ttk.Label(frame_info_d, text="   • Agregar sufijo -> para forzar UNA dirección", 
                 font=('Arial', 10)).pack(anchor='w')
        ttk.Label(frame_info_d, text="   • Ejemplo: 1 2 5 (bidireccional) + 6 4 1 -> (solo 6→4)", 
                 font=('Arial', 10), foreground='#E74C3C').pack(anchor='w')
        ttk.Label(frame_info_d, text="   • Útil para calles de un solo sentido en una red", 
                 font=('Arial', 9, 'italic'), foreground='#7F8C8D').pack(anchor='w')
        
        # Botones de ejemplo
        frame_ej = ttk.Frame(frame_izq)
        frame_ej.pack(fill='x', pady=5)
        ttk.Label(frame_ej, text="Ejemplos:", font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        ttk.Button(frame_ej, text="Simple", 
                  command=lambda: self.cargar_ejemplo_dijkstra('simple')).pack(side='left', padx=2)
        ttk.Button(frame_ej, text="Complejo", 
                  command=lambda: self.cargar_ejemplo_dijkstra('complejo')).pack(side='left', padx=2)
        ttk.Button(frame_ej, text="Dirigido ➡️", 
                  command=lambda: self.cargar_ejemplo_dijkstra('dirigido')).pack(side='left', padx=2)
        
        self.txt_aristas_dijkstra = scrolledtext.ScrolledText(frame_izq, height=10, width=40, font=('Consolas', 11))
        self.txt_aristas_dijkstra.pack(fill='both', expand=True, pady=5)
        
        # Frame para configuración
        frame_config = ttk.LabelFrame(frame_izq, text="⚙️ Configuración", padding=5)
        frame_config.pack(fill='x', pady=5)
        
        ttk.Label(frame_config, text="Nodo origen:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5)
        self.entry_origen = ttk.Entry(frame_config, width=10)
        self.entry_origen.grid(row=0, column=1, sticky='w', padx=5, pady=2)
        self.entry_origen.insert(0, "A")
        
        # Checkbox para grafo dirigido
        self.var_dirigido_dijkstra = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame_config, text="Grafo dirigido (las aristas tienen dirección única)", 
                       variable=self.var_dirigido_dijkstra,
                       command=lambda: self.actualizar_info_dijkstra()).grid(row=1, column=0, columnspan=2, sticky='w', padx=5, pady=5)
        
        # Etiqueta de ayuda dinámica
        self.lbl_ayuda_dijkstra = ttk.Label(frame_config, text="", font=('Arial', 8, 'italic'), foreground='blue')
        self.lbl_ayuda_dijkstra.grid(row=2, column=0, columnspan=2, sticky='w', padx=5)
        self.actualizar_info_dijkstra()
        
        # Botones
        frame_botones = ttk.Frame(frame_izq)
        frame_botones.pack(pady=10)
        
        ttk.Button(frame_botones, text="🚀 Ejecutar Dijkstra", 
                  command=self.ejecutar_dijkstra).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="🗑️ Limpiar", 
                  command=lambda: self.txt_resultado_dijkstra.delete('1.0', 'end')).pack(side='left', padx=5)
        
        # Panel derecho
        frame_der = ttk.LabelFrame(frame, text="Resultados", padding=10)
        frame_der.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        self.txt_resultado_dijkstra = scrolledtext.ScrolledText(frame_der, height=20, width=60, font=('Consolas', 11))
        self.txt_resultado_dijkstra.pack(fill='both', expand=True)
        
        # Canvas para gráfico
        self.canvas_dijkstra = None
        
    def crear_pestaña_floyd_warshall(self):
        """Pestaña para Floyd-Warshall"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🗺️ Todos los Pares (Floyd-Warshall)")
        
        # Panel izquierdo
        frame_izq = ttk.LabelFrame(frame, text="Entrada de Datos", padding=10)
        frame_izq.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(frame_izq, text="Ingrese las aristas (formato: nodo1 nodo2 peso):", 
                 font=('Arial', 11, 'bold')).pack(anchor='w', pady=5)
        
        # Frame de información
        frame_info_fw = ttk.Frame(frame_izq)
        frame_info_fw.pack(fill='x', pady=5)
        
        info_text = tk.Text(frame_info_fw, height=7, wrap='word', font=('Arial', 11), 
                           bg='#ECF0F1', relief='flat', padx=10, pady=5)
        info_text.pack(fill='x')
        
        info_text.insert('1.0', "📌 INSTRUCCIONES:\n\n", 'header')
        info_text.insert('end', "⚠️ Floyd-Warshall calcula distancias entre TODOS los pares de nodos.\n\n", 'warning')
        info_text.insert('end', "🔹 GRAFO DIRIGIDO", 'bold')
        info_text.insert('end', " (marcar checkbox):\n", 'normal')
        info_text.insert('end', "   • Cada línea es UNA arista: ", 'normal')
        info_text.insert('end', "2 6 6", 'example')
        info_text.insert('end', " significa 2→6 con peso 6\n\n", 'normal')
        info_text.insert('end', "🔹 GRAFO NO DIRIGIDO", 'bold')
        info_text.insert('end', " (desmarcar checkbox):\n", 'normal')
        info_text.insert('end', "   • Cada línea crea DOS aristas: ", 'normal')
        info_text.insert('end', "2 6 6", 'example')
        info_text.insert('end', " crea 2→6 y 6→2\n\n", 'normal')
        info_text.insert('end', "� GRAFO HÍBRIDO", 'bold')
        info_text.insert('end', " (agregar sufijo ->):\n", 'normal')
        info_text.insert('end', "   • Mezcla aristas bidireccionales y unidireccionales\n", 'normal')
        info_text.insert('end', "   • Ejemplo: ", 'normal')
        info_text.insert('end', "6 4 1 ->", 'example')
        info_text.insert('end', " fuerza SOLO 6→4 (ignora checkbox)", 'normal')
        
        # Configurar tags de colores
        info_text.tag_config('header', foreground='#2C3E50', font=('Arial', 10, 'bold'))
        info_text.tag_config('warning', foreground='#E74C3C', font=('Arial', 9, 'bold'))
        info_text.tag_config('bold', foreground='#2C3E50', font=('Arial', 9, 'bold'))
        info_text.tag_config('normal', foreground='#2C3E50', font=('Arial', 9))
        info_text.tag_config('example', foreground='#3498DB', font=('Courier', 9, 'bold'))
        info_text.config(state='disabled')
        
        # Botones de ejemplo
        frame_ej_fw = ttk.Frame(frame_izq)
        frame_ej_fw.pack(fill='x', pady=5)
        ttk.Label(frame_ej_fw, text="Ejemplos:", font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        ttk.Button(frame_ej_fw, text="Dirigido ➡️", 
                  command=lambda: self.cargar_ejemplo_floyd('dirigido')).pack(side='left', padx=2)
        ttk.Button(frame_ej_fw, text="No Dirigido ↔️", 
                  command=lambda: self.cargar_ejemplo_floyd('no_dirigido')).pack(side='left', padx=2)
        ttk.Button(frame_ej_fw, text="🔥 Híbrido", 
                  command=lambda: self.cargar_ejemplo_floyd('hibrido')).pack(side='left', padx=2)
        
        self.txt_aristas_fw = scrolledtext.ScrolledText(frame_izq, height=10, width=40, font=('Consolas', 11))
        self.txt_aristas_fw.pack(fill='both', expand=True, pady=5)
        self.txt_aristas_fw.insert('1.0', "1 2 3\n1 3 8\n1 5 -4\n2 4 1\n2 5 7\n3 2 4\n4 1 2\n4 3 -5\n5 4 6")
        
        # Frame para configuración
        frame_config_fw = ttk.LabelFrame(frame_izq, text="⚙️ Configuración", padding=5)
        frame_config_fw.pack(fill='x', pady=5)
        
        self.var_dirigido_floyd = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_config_fw, text="Grafo Dirigido (aristas unidireccionales)", 
                       variable=self.var_dirigido_floyd).pack(anchor='w')
        
        # Botones principales
        frame_botones = ttk.Frame(frame_izq)
        frame_botones.pack(pady=10)
        
        ttk.Button(frame_botones, text="🔄 Ejecutar Floyd-Warshall", 
                  command=self.ejecutar_floyd_warshall).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="🗑️ Limpiar", 
                  command=lambda: self.txt_resultado_fw.delete('1.0', 'end')).pack(side='left', padx=5)
        
        # Frame para consultar ruta específica
        frame_consulta = ttk.LabelFrame(frame_izq, text="🔍 Consultar Ruta Específica", padding=10)
        frame_consulta.pack(fill='x', pady=10)
        
        ttk.Label(frame_consulta, text="Ejecuta Floyd-Warshall primero, luego consulta:", 
                 font=('Arial', 9, 'italic'), foreground='#7F8C8D').pack(anchor='w', pady=(0, 5))
        
        # Origen y destino
        frame_od_fw = ttk.Frame(frame_consulta)
        frame_od_fw.pack(fill='x', pady=5)
        
        ttk.Label(frame_od_fw, text="Origen:", font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        self.entry_origen_fw = ttk.Entry(frame_od_fw, width=10)
        self.entry_origen_fw.pack(side='left', padx=5)
        
        ttk.Label(frame_od_fw, text="Destino:", font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        self.entry_destino_fw = ttk.Entry(frame_od_fw, width=10)
        self.entry_destino_fw.pack(side='left', padx=5)
        
        ttk.Button(frame_consulta, text="📍 Consultar Ruta", 
                  command=self.consultar_ruta_floyd).pack(pady=5)
        
        # Panel derecho
        frame_der = ttk.LabelFrame(frame, text="Resultados", padding=10)
        frame_der.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        self.txt_resultado_fw = scrolledtext.ScrolledText(frame_der, height=20, width=60, font=('Consolas', 11))
        self.txt_resultado_fw.pack(fill='both', expand=True)
        
        # Canvas para gráfico
        self.canvas_fw = None
        
    def crear_pestaña_flujo_maximo(self):
        """Pestaña para Ford-Fulkerson"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💧 Flujo Máximo")
        
        # Panel izquierdo
        frame_izq = ttk.LabelFrame(frame, text="Entrada de Datos", padding=10)
        frame_izq.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(frame_izq, text="Ingrese las aristas (formato: origen destino capacidad):", 
                 font=('Arial', 11, 'bold')).pack(anchor='w', pady=5)
        
        self.txt_aristas_flujo = scrolledtext.ScrolledText(frame_izq, height=12, width=40, font=('Consolas', 11))
        self.txt_aristas_flujo.pack(fill='both', expand=True, pady=5)
        self.txt_aristas_flujo.insert('1.0', "1 2 20\n1 3 30\n2 3 40\n2 4 30\n3 4 20\n3 5 20\n4 5 20")
        
        ttk.Label(frame_izq, text="Nodo origen:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10,0))
        self.entry_origen_flujo = ttk.Entry(frame_izq, width=10)
        self.entry_origen_flujo.pack(anchor='w', pady=5)
        self.entry_origen_flujo.insert(0, "1")
        
        ttk.Label(frame_izq, text="Nodo destino:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.entry_destino_flujo = ttk.Entry(frame_izq, width=10)
        self.entry_destino_flujo.pack(anchor='w', pady=5)
        self.entry_destino_flujo.insert(0, "5")
        
        # Botones
        frame_botones = ttk.Frame(frame_izq)
        frame_botones.pack(pady=10)
        
        ttk.Button(frame_botones, text="💧 Calcular Flujo Máximo", 
                  command=self.ejecutar_flujo_maximo).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="🗑️ Limpiar", 
                  command=lambda: self.txt_resultado_flujo.delete('1.0', 'end')).pack(side='left', padx=5)
        
        # Panel derecho
        frame_der = ttk.LabelFrame(frame, text="Resultados", padding=10)
        frame_der.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        self.txt_resultado_flujo = scrolledtext.ScrolledText(frame_der, height=20, width=60, font=('Consolas', 11))
        self.txt_resultado_flujo.pack(fill='both', expand=True)
        
        # Canvas para gráfico
        self.canvas_flujo = None
        
    def crear_pestaña_suma_cero(self):
        """Pestaña para juegos de suma cero"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎮 Juegos Suma Cero")
        
        # Panel izquierdo
        frame_izq = ttk.LabelFrame(frame, text="Entrada de Datos", padding=10)
        frame_izq.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(frame_izq, text="Ingrese la matriz de pagos (Jugador A por filas):", 
                 font=('Arial', 11, 'bold')).pack(anchor='w', pady=5)
        ttk.Label(frame_izq, text="Formato: valores separados por espacios, una fila por línea", 
                 font=('Arial', 9, 'italic')).pack(anchor='w')
        
        self.txt_matriz_juego = scrolledtext.ScrolledText(frame_izq, height=10, width=40, font=('Consolas', 11))
        self.txt_matriz_juego.pack(fill='both', expand=True, pady=5)
        self.txt_matriz_juego.insert('1.0', "2 1 0\n3 2 -1\n1 -1 -2")
        
        ttk.Label(frame_izq, text="Ejemplos predefinidos:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10,5))
        
        frame_ejemplos = ttk.Frame(frame_izq)
        frame_ejemplos.pack(fill='x', pady=5)
        
        ttk.Button(frame_ejemplos, text="Ejercicio 1", 
                  command=lambda: self.cargar_ejemplo_juego("2 1 0\n3 2 -1\n1 -1 -2")).pack(side='left', padx=2)
        ttk.Button(frame_ejemplos, text="Ejercicio 2", 
                  command=lambda: self.cargar_ejemplo_juego("5 -1\n2 4")).pack(side='left', padx=2)
        
        # Botones
        frame_botones = ttk.Frame(frame_izq)
        frame_botones.pack(pady=10)
        
        ttk.Button(frame_botones, text="🎲 Resolver Juego", 
                  command=self.resolver_juego_suma_cero).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="🗑️ Limpiar", 
                  command=lambda: self.txt_resultado_juego.delete('1.0', 'end')).pack(side='left', padx=5)
        
        # Panel derecho
        frame_der = ttk.LabelFrame(frame, text="Resultados", padding=10)
        frame_der.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        self.txt_resultado_juego = scrolledtext.ScrolledText(frame_der, height=20, width=60, font=('Consolas', 11))
        self.txt_resultado_juego.pack(fill='both', expand=True)
    
    def _calcular_tamano_nodos(self, n_nodos):
        """
        Calcula el tamaño óptimo de nodos según la cantidad.
        Escala dinámicamente para evitar solapamiento en grafos grandes.
        """
        if n_nodos <= 5:
            return 900
        elif n_nodos <= 10:
            return 700
        elif n_nodos <= 15:
            return 550
        elif n_nodos <= 20:
            return 450
        else:
            return max(300, 900 - n_nodos * 25)
    
    def _calcular_tamano_fuente(self, n_nodos):
        """
        Calcula el tamaño óptimo de fuente según la cantidad de nodos.
        """
        if n_nodos <= 5:
            return 12
        elif n_nodos <= 10:
            return 11
        elif n_nodos <= 15:
            return 10
        else:
            return max(8, 12 - n_nodos // 5)
    
    def _guardar_figura(self, fig, ventana, nombre_default="grafo"):
        """
        Guarda la figura actual como imagen PNG o SVG.
        """
        from tkinter import filedialog
        archivo = filedialog.asksaveasfilename(
            parent=ventana,
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("SVG Vector", "*.svg"),
                ("PDF Document", "*.pdf"),
                ("All files", "*.*")
            ],
            initialfile=nombre_default,
            title="Guardar gráfico como imagen"
        )
        if archivo:
            try:
                fig.savefig(archivo, dpi=150, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
                messagebox.showinfo("Éxito", f"Imagen guardada en:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
    
    def _calcular_layout_inteligente(self, G, seed=None):
        """
        Calcula el mejor layout para visualizar el grafo según sus características.
        Intenta múltiples algoritmos y elige el que mejor separa los nodos.
        """
        import random
        if seed is None:
            seed = random.randint(1, 10000)
        
        n_nodos = G.number_of_nodes()
        n_aristas = G.number_of_edges()
        
        # Para grafos muy pequeños (≤3 nodos), usar layout circular
        if n_nodos <= 3:
            return nx.circular_layout(G)
        
        # Para grafos pequeños (4-8 nodos), intentar varios layouts y elegir el mejor
        if n_nodos <= 8:
            layouts = []
            
            # Spring layout con diferentes parámetros
            try:
                layouts.append(('spring_k2', nx.spring_layout(G, k=2/n_nodos**0.5, iterations=100, seed=seed)))
            except:
                pass
            
            try:
                layouts.append(('spring_k1', nx.spring_layout(G, k=1, iterations=100, seed=seed)))
            except:
                pass
            
            # Kamada-Kawai (muy bueno para grafos pequeños/medianos)
            try:
                layouts.append(('kamada', nx.kamada_kawai_layout(G)))
            except:
                pass
            
            # Planar si el grafo es planar
            try:
                if nx.is_planar(G):
                    layouts.append(('planar', nx.planar_layout(G)))
            except:
                pass
            
            # Circular como respaldo
            layouts.append(('circular', nx.circular_layout(G)))
            
            # Evaluar cuál layout tiene mejor separación entre nodos
            mejor_layout = None
            mejor_score = -1
            
            for nombre, pos in layouts:
                # Calcular distancia mínima entre nodos
                distancias = []
                nodos = list(pos.keys())
                for i in range(len(nodos)):
                    for j in range(i+1, len(nodos)):
                        p1 = pos[nodos[i]]
                        p2 = pos[nodos[j]]
                        dist = ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
                        distancias.append(dist)
                
                if distancias:
                    # Score: distancia mínima (queremos maximizarla)
                    score = min(distancias)
                    if score > mejor_score:
                        mejor_score = score
                        mejor_layout = pos
            
            return mejor_layout if mejor_layout else nx.spring_layout(G, seed=seed)
        
        # Para grafos medianos (9-15 nodos)
        elif n_nodos <= 15:
            try:
                # Kamada-Kawai es excelente para grafos medianos
                return nx.kamada_kawai_layout(G)
            except:
                # Si falla, usar spring con buenos parámetros
                return nx.spring_layout(G, k=1.5/n_nodos**0.5, iterations=100, seed=seed)
        
        # Para grafos grandes (>15 nodos)
        else:
            # Spring layout optimizado para grafos grandes
            return nx.spring_layout(G, k=3/n_nodos**0.5, iterations=50, seed=seed)
    
    def cargar_ejemplo_juego(self, texto):
        """Carga un ejemplo de juego en el área de texto"""
        self.txt_matriz_juego.delete('1.0', 'end')
        self.txt_matriz_juego.insert('1.0', texto)
    
    def cargar_ejemplo_mediano_mst(self):
        """Carga un ejemplo mediano para MST"""
        ejemplo = """A B 7
A D 5
B C 8
B D 9
B E 7
C E 5
D E 15
D F 6
E F 8
E G 9
F G 11"""
        self.txt_aristas.delete('1.0', 'end')
        self.txt_aristas.insert('1.0', ejemplo)
    
    def actualizar_info_dijkstra(self):
        """Actualiza el mensaje de ayuda según si el grafo es dirigido o no"""
        if self.var_dirigido_dijkstra.get():
            self.lbl_ayuda_dijkstra.config(
                text="📌 Modo DIRIGIDO: La arista 'A B 5' solo permite ir de A → B (no de B → A)",
                foreground='darkblue'
            )
        else:
            self.lbl_ayuda_dijkstra.config(
                text="📌 Modo NO DIRIGIDO: La arista 'A B 5' permite ir A ↔ B (ambas direcciones)",
                foreground='darkgreen'
            )
    
    def cargar_ejemplo_dijkstra(self, tipo):
        """Carga ejemplos para Dijkstra"""
        if tipo == 'simple':
            ejemplo = "A B 4\nA C 2\nB C 1\nB D 5\nC D 8\nC E 10\nD E 2"
            self.var_dirigido_dijkstra.set(False)
            origen = "A"
            mensaje = "Ejemplo simple cargado (grafo no dirigido)"
        elif tipo == 'complejo':
            ejemplo = """1 2 4
1 3 2
2 3 3
2 4 2
2 5 3
3 5 4
3 6 1
4 5 5
5 6 2
5 7 6
6 7 3"""
            self.var_dirigido_dijkstra.set(False)
            origen = "1"
            mensaje = "Ejemplo complejo cargado (grafo no dirigido)"
        else:  # tipo == 'dirigido'
            ejemplo = """1 2 5
1 3 1
2 1 5
2 4 7
2 6 6
3 1 1
3 4 4
3 5 3
4 2 7
4 3 4
4 7 3
5 3 3
5 6 2
6 2 7
6 5 2
6 7 2"""
            self.var_dirigido_dijkstra.set(True)
            origen = "1"
            mensaje = "Ejemplo DIRIGIDO cargado: 2→6 peso 6, pero 6→2 peso 7\n(Marca 'Grafo Dirigido' activa)"
        
        self.txt_aristas_dijkstra.delete('1.0', 'end')
        self.txt_aristas_dijkstra.insert('1.0', ejemplo)
        self.entry_origen.delete(0, 'end')
        self.entry_origen.insert(0, origen)
        messagebox.showinfo("Ejemplo Cargado", mensaje)
    
    def cargar_ejemplo_floyd(self, tipo):
        """Carga ejemplos para Floyd-Warshall"""
        if tipo == 'dirigido':
            ejemplo = """1 2 3
1 3 8
1 5 -4
2 4 1
2 5 7
3 2 4
4 1 2
4 3 -5
5 4 6"""
            self.var_dirigido_floyd.set(True)
            mensaje = "Ejemplo DIRIGIDO cargado.\nCada arista es unidireccional.\nObserva que no todas las conexiones son bidireccionales."
        elif tipo == 'hibrido':
            ejemplo = """1 2 5
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
            self.var_dirigido_floyd.set(False)
            mensaje = "🔥 Ejemplo HÍBRIDO cargado!\n\nLa mayoría son BIDIRECCIONALES (sin sufijo).\nPero las últimas 2 son UNIDIRECCIONALES con '->':\n  • 6→4 peso 1 (solo ida)\n  • 7→6 peso 4 (solo ida)\n\n✨ Perfecto para redes mixtas (calles bidireccionales + de un solo sentido)."
        else:  # no_dirigido
            ejemplo = """A B 4
A C 2
B C 1
B D 5
C D 8
C E 10
D E 2"""
            self.var_dirigido_floyd.set(False)
            mensaje = "Ejemplo NO DIRIGIDO cargado.\nCada línea crea aristas bidireccionales (ida y vuelta) con el mismo peso."
        
        self.txt_aristas_fw.delete('1.0', 'end')
        self.txt_aristas_fw.insert('1.0', ejemplo)
        messagebox.showinfo("Ejemplo Cargado", mensaje)
    
    def guardar_resultado(self, texto):
        """Guarda el resultado en un archivo"""
        try:
            archivo = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Guardar resultado"
            )
            if archivo:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(texto)
                messagebox.showinfo("Éxito", "Resultado guardado correctamente")
                self.status_bar.config(text=f"✅ Guardado en: {archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
    
    def comparar_algoritmos_mst(self):
        """Compara Kruskal y Prim mostrando ambos resultados"""
        try:
            self.txt_resultado_mst.delete('1.0', 'end')
            self.txt_resultado_mst.insert('end', "=" * 70 + "\n")
            self.txt_resultado_mst.insert('end', "COMPARACIÓN: KRUSKAL vs PRIM\n")
            self.txt_resultado_mst.insert('end', "=" * 70 + "\n\n")
            
            # Parsear aristas
            texto = self.txt_aristas.get('1.0', 'end').strip()
            if not texto:
                messagebox.showwarning("Advertencia", "Debe ingresar al menos una arista")
                return
            
            lineas = texto.split('\n')
            aristas = []
            grafo = {}
            nodos = set()
            
            for linea in lineas:
                if linea.strip():
                    # Los árboles mínimos siempre son NO dirigidos (bidireccionales)
                    resultado = self._parsear_arista(linea, es_dirigido_global=False)
                    if resultado:
                        u, v, peso, es_bidireccional = resultado
                        # Siempre agregar como bidireccional (MST requiere grafo no dirigido)
                        aristas.append((u, v, peso))
                        nodos.add(u)
                        nodos.add(v)
                        
                        if u not in grafo:
                            grafo[u] = {}
                        if v not in grafo:
                            grafo[v] = {}
                        
                        grafo[u][v] = peso
                        grafo[v][u] = peso
            
            if not aristas:
                messagebox.showerror("Error", "No se encontraron aristas válidas")
                return
            
            # Mapear nodos a índices
            nodos_lista = sorted(list(nodos))
            nodo_a_idx = {nodo: i for i, nodo in enumerate(nodos_lista)}
            aristas_idx = [(nodo_a_idx[u], nodo_a_idx[v], peso) for u, v, peso in aristas]
            grafo_idx = {nodo_a_idx[n]: {nodo_a_idx[v]: p for v, p in vecinos.items()} 
                        for n, vecinos in grafo.items()}
            
            # Redirigir stdout
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Ejecutar Kruskal
            self.txt_resultado_mst.insert('end', "🌳 ALGORITMO DE KRUSKAL\n")
            self.txt_resultado_mst.insert('end', "=" * 70 + "\n\n")
            mst_k, peso_k, iteraciones_k = AlgoritmosGrafos.kruskal(aristas_idx, len(nodos))
            output_k = sys.stdout.getvalue()
            sys.stdout = StringIO()
            
            # Mostrar iteraciones de Kruskal
            self.txt_resultado_mst.insert('end', "📊 PROCESO PASO A PASO:\n")
            self.txt_resultado_mst.insert('end', "-" * 70 + "\n\n")
            
            for iter_data in iteraciones_k:
                u_orig, v_orig, peso = iter_data['arista']
                u, v = nodos_lista[u_orig], nodos_lista[v_orig]
                
                if iter_data['aceptada']:
                    self.txt_resultado_mst.insert('end', 
                        f"✅ Iteración {iter_data['num']}: ACEPTAR {u}-{v} (peso: {peso})\n")
                    self.txt_resultado_mst.insert('end', 
                        f"   Peso acumulado: {iter_data['peso_acumulado']}\n")
                    self.txt_resultado_mst.insert('end', 
                        f"   Aristas en MST: {len(iter_data['mst_actual'])}\n\n")
                else:
                    self.txt_resultado_mst.insert('end', 
                        f"❌ Iteración {iter_data['num']}: RECHAZAR {u}-{v} (peso: {peso})\n")
                    self.txt_resultado_mst.insert('end', 
                        f"   Razón: Formaría un ciclo (ambos nodos ya conectados)\n\n")
            
            # Ejecutar Prim
            mst_p, peso_p, iteraciones_p = AlgoritmosGrafos.prim(grafo_idx, 0)
            output_p = sys.stdout.getvalue()
            
            # Restaurar stdout
            sys.stdout = old_stdout
            
            # Mostrar resultados finales de Kruskal
            self.txt_resultado_mst.insert('end', "=" * 70 + "\n")
            self.txt_resultado_mst.insert('end', "✅ RESULTADO FINAL - KRUSKAL\n")
            self.txt_resultado_mst.insert('end', "=" * 70 + "\n")
            self.txt_resultado_mst.insert('end', f"\nPeso total del MST: {peso_k}\n")
            self.txt_resultado_mst.insert('end', "Aristas seleccionadas:\n")
            mst_k = [(nodos_lista[u], nodos_lista[v], peso) for u, v, peso in mst_k]
            for u, v, peso in mst_k:
                self.txt_resultado_mst.insert('end', f"  {u} - {v}: {peso}\n")
            
            self.txt_resultado_mst.insert('end', "\n\n" + "=" * 70 + "\n")
            self.txt_resultado_mst.insert('end', "🌲 ALGORITMO DE PRIM\n")
            self.txt_resultado_mst.insert('end', "=" * 70 + "\n\n")
            
            # Mostrar iteraciones de Prim
            self.txt_resultado_mst.insert('end', "📊 PROCESO PASO A PASO:\n")
            self.txt_resultado_mst.insert('end', "-" * 70 + "\n\n")
            
            for iter_data in iteraciones_p:
                if iter_data['tipo'] == 'inicial':
                    nodo_inicio = nodos_lista[iter_data['nodo_inicio']]
                    self.txt_resultado_mst.insert('end', 
                        f"🔵 INICIO: Desde nodo {nodo_inicio}\n")
                    self.txt_resultado_mst.insert('end', 
                        f"   Candidatos iniciales: {len(iter_data['candidatos'])}\n\n")
                elif iter_data['tipo'] == 'aceptada':
                    u_orig, v_orig, peso = iter_data['arista']
                    u, v = nodos_lista[u_orig], nodos_lista[v_orig]
                    self.txt_resultado_mst.insert('end', 
                        f"✅ Iteración {iter_data['num']}: AGREGAR {u}-{v} (peso: {peso})\n")
                    self.txt_resultado_mst.insert('end', 
                        f"   Nodos visitados: {len(iter_data['visitados'])}\n")
                    self.txt_resultado_mst.insert('end', 
                        f"   Peso acumulado: {iter_data['peso_total']}\n")
                    if iter_data['nuevas_aristas']:
                        self.txt_resultado_mst.insert('end', 
                            f"   Nuevas aristas candidatas: {len(iter_data['nuevas_aristas'])}\n\n")
                    else:
                        self.txt_resultado_mst.insert('end', "\n")
                elif iter_data['tipo'] == 'rechazada':
                    u_orig, v_orig, peso = iter_data['arista']
                    u, v = nodos_lista[u_orig], nodos_lista[v_orig]
                    self.txt_resultado_mst.insert('end', 
                        f"⏭️  Iteración {iter_data['num']}: OMITIR {u}-{v} (peso: {peso})\n")
                    self.txt_resultado_mst.insert('end', 
                        f"   Razón: {iter_data['razon']}\n\n")
            
            # Mostrar resultados finales de Prim
            self.txt_resultado_mst.insert('end', "=" * 70 + "\n")
            self.txt_resultado_mst.insert('end', "✅ RESULTADO FINAL - PRIM\n")
            self.txt_resultado_mst.insert('end', "=" * 70 + "\n")
            self.txt_resultado_mst.insert('end', f"\nPeso total del MST: {peso_p}\n")
            self.txt_resultado_mst.insert('end', "Aristas seleccionadas:\n")
            mst_p = [(nodos_lista[u], nodos_lista[v], peso) for u, v, peso in mst_p]
            for u, v, peso in mst_p:
                self.txt_resultado_mst.insert('end', f"  {u} - {v}: {peso}\n")
            
            self.txt_resultado_mst.insert('end', "\n" + "=" * 70 + "\n")
            self.txt_resultado_mst.insert('end', "📊 VERIFICACIÓN\n")
            self.txt_resultado_mst.insert('end', "=" * 70 + "\n")
            self.txt_resultado_mst.insert('end', f"Peso Kruskal: {peso_k}\n")
            self.txt_resultado_mst.insert('end', f"Peso Prim:    {peso_p}\n")
            self.txt_resultado_mst.insert('end', f"¿Iguales? {'✅ SÍ' if abs(peso_k - peso_p) < 0.001 else '❌ NO'}\n")
            self.txt_resultado_mst.insert('end', f"\nNúmero de nodos: {len(nodos)}\n")
            self.txt_resultado_mst.insert('end', f"Aristas en el MST: {len(mst_k)}\n")
            self.txt_resultado_mst.insert('end', f"¿Correcto? {'✅ SÍ (V-1)' if len(mst_k) == len(nodos)-1 else '❌ NO'}\n")
            
            self.status_bar.config(text=f"✅ Comparación completada - Peso MST: {peso_k}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la comparación: {str(e)}\n{type(e).__name__}")
            self.status_bar.config(text="❌ Error en la comparación")
    
    def ejecutar_arbol_minimo(self, algoritmo):
        """Ejecuta Kruskal o Prim"""
        try:
            # Limpiar resultado
            self.txt_resultado_mst.delete('1.0', 'end')
            
            # Parsear aristas
            texto = self.txt_aristas.get('1.0', 'end').strip()
            lineas = texto.split('\n')
            
            aristas = []
            grafo = {}
            nodos = set()
            
            for linea in lineas:
                if linea.strip():
                    partes = linea.strip().split()
                    if len(partes) == 3:
                        u, v, peso = partes[0], partes[1], float(partes[2])
                        aristas.append((u, v, peso))
                        nodos.add(u)
                        nodos.add(v)
                        
                        if u not in grafo:
                            grafo[u] = {}
                        if v not in grafo:
                            grafo[v] = {}
                        
                        grafo[u][v] = peso
                        grafo[v][u] = peso  # Grafo no dirigido
            
            if not aristas:
                messagebox.showerror("Error", "No se encontraron aristas válidas")
                return
            
            # Mapear nodos a índices
            nodos_lista = sorted(list(nodos))
            nodo_a_idx = {nodo: i for i, nodo in enumerate(nodos_lista)}
            aristas_idx = [(nodo_a_idx[u], nodo_a_idx[v], peso) for u, v, peso in aristas]
            grafo_idx = {nodo_a_idx[n]: {nodo_a_idx[v]: p for v, p in vecinos.items()} 
                        for n, vecinos in grafo.items()}
            
            # Ejecutar algoritmo
            if algoritmo == 'kruskal':
                self.txt_resultado_mst.insert('end', "=" * 60 + "\n")
                self.txt_resultado_mst.insert('end', "ALGORITMO DE KRUSKAL\n")
                self.txt_resultado_mst.insert('end', "=" * 60 + "\n\n")
                mst, peso_total, iteraciones = AlgoritmosGrafos.kruskal(aristas_idx, len(nodos))
                
                # Mostrar iteraciones
                self.txt_resultado_mst.insert('end', "📊 PROCESO PASO A PASO:\n")
                self.txt_resultado_mst.insert('end', "-" * 60 + "\n\n")
                
                for iter_data in iteraciones:
                    u_orig, v_orig, peso = iter_data['arista']
                    u, v = nodos_lista[u_orig], nodos_lista[v_orig]
                    
                    if iter_data['aceptada']:
                        self.txt_resultado_mst.insert('end', 
                            f"✅ {iter_data['num']}. ACEPTAR {u}-{v} (peso: {peso})\n")
                        self.txt_resultado_mst.insert('end', 
                            f"   Peso acumulado: {iter_data['peso_acumulado']}\n\n")
                    else:
                        self.txt_resultado_mst.insert('end', 
                            f"❌ {iter_data['num']}. RECHAZAR {u}-{v} (peso: {peso}) - Formaría ciclo\n\n")
                
                # Convertir índices de vuelta a nombres
                mst = [(nodos_lista[u], nodos_lista[v], peso) for u, v, peso in mst]
            else:
                self.txt_resultado_mst.insert('end', "=" * 60 + "\n")
                self.txt_resultado_mst.insert('end', "ALGORITMO DE PRIM\n")
                self.txt_resultado_mst.insert('end', "=" * 60 + "\n\n")
                mst, peso_total, iteraciones = AlgoritmosGrafos.prim(grafo_idx, 0)
                
                # Mostrar iteraciones
                self.txt_resultado_mst.insert('end', "📊 PROCESO PASO A PASO:\n")
                self.txt_resultado_mst.insert('end', "-" * 60 + "\n\n")
                
                for iter_data in iteraciones:
                    if iter_data['tipo'] == 'inicial':
                        nodo_inicio = nodos_lista[iter_data['nodo_inicio']]
                        self.txt_resultado_mst.insert('end', 
                            f"🔵 INICIO desde nodo {nodo_inicio}\n\n")
                    elif iter_data['tipo'] == 'aceptada':
                        u_orig, v_orig, peso = iter_data['arista']
                        u, v = nodos_lista[u_orig], nodos_lista[v_orig]
                        self.txt_resultado_mst.insert('end', 
                            f"✅ {iter_data['num']}. AGREGAR {u}-{v} (peso: {peso})\n")
                        self.txt_resultado_mst.insert('end', 
                            f"   Peso acumulado: {iter_data['peso_total']}\n\n")
                
                # Convertir índices de vuelta a nombres
                mst = [(nodos_lista[u], nodos_lista[v], peso) for u, v, peso in mst]
            
            # Mostrar resultado final
            self.txt_resultado_mst.insert('end', "=" * 60 + "\n")
            self.txt_resultado_mst.insert('end', "✅ RESULTADO FINAL\n")
            self.txt_resultado_mst.insert('end', "=" * 60 + "\n\n")
            self.txt_resultado_mst.insert('end', f"Árbol de Expansión Mínima:\n")
            for u, v, peso in mst:
                self.txt_resultado_mst.insert('end', f"  {u} - {v}: {peso}\n")
            
            self.txt_resultado_mst.insert('end', f"\n{'='*60}\n")
            self.txt_resultado_mst.insert('end', f"PESO TOTAL: {peso_total}\n")
            self.txt_resultado_mst.insert('end', f"{'='*60}\n")
            
            # Visualizar
            self.visualizar_mst(grafo, mst, f"Árbol de Expansión Mínima ({algoritmo.upper()})")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar {algoritmo}: {str(e)}")
    
    def visualizar_mst(self, grafo, mst, titulo):
        """Visualiza el árbol de expansión mínima con mejoras visuales"""
        G = nx.Graph()
        
        # Agregar todas las aristas
        for u in grafo:
            for v, peso in grafo[u].items():
                if u < v:  # Evitar duplicados
                    G.add_edge(u, v, weight=peso, in_mst=False)
        
        # Marcar aristas del MST
        for u, v, peso in mst:
            if G.has_edge(u, v):
                G[u][v]['in_mst'] = True
            elif G.has_edge(v, u):
                G[v][u]['in_mst'] = True
        
        # Calcular tamaños dinámicos
        n_nodos = G.number_of_nodes()
        node_size = self._calcular_tamano_nodos(n_nodos)
        font_size = self._calcular_tamano_fuente(n_nodos)
        font_size_edges = max(7, font_size - 2)
        
        # Crear figura
        fig = plt.Figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        
        # Usar layout inteligente
        pos = self._calcular_layout_inteligente(G)
        
        # Dibujar aristas no MST (gris, discontinuas)
        aristas_no_mst = [(u, v) for u, v, d in G.edges(data=True) if not d.get('in_mst', False)]
        nx.draw_networkx_edges(G, pos, edgelist=aristas_no_mst, 
                              width=1.5, alpha=0.4, edge_color='#95A5A6', 
                              style='dashed', ax=ax)
        
        # Dibujar aristas MST (rojo, sólidas y gruesas)
        aristas_mst = [(u, v) for u, v, d in G.edges(data=True) if d.get('in_mst', False)]
        nx.draw_networkx_edges(G, pos, edgelist=aristas_mst, 
                              width=3.5, alpha=1, edge_color='#E74C3C', ax=ax)
        
        # Dibujar nodos con borde
        nx.draw_networkx_nodes(G, pos, node_color='#AED6F1', 
                              node_size=node_size, ax=ax,
                              edgecolors='#2980B9', linewidths=2)
        nx.draw_networkx_labels(G, pos, font_size=font_size, font_weight='bold', ax=ax)
        
        # Etiquetas de pesos con fondo blanco para legibilidad
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=font_size_edges, ax=ax,
                                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                             edgecolor='none', alpha=0.8))
        
        # Calcular peso total del MST
        peso_total = sum(peso for u, v, peso in mst)
        
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=15)
        ax.axis('off')
        
        # Agregar leyenda
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch
        leyenda_elementos = [
            Line2D([0], [0], color='#E74C3C', linewidth=3.5, label=f'Aristas del MST (peso total: {peso_total})'),
            Line2D([0], [0], color='#95A5A6', linewidth=1.5, linestyle='--', label='Aristas descartadas'),
            Patch(facecolor='#AED6F1', edgecolor='#2980B9', linewidth=2, label=f'Nodos ({n_nodos} total)')
        ]
        ax.legend(handles=leyenda_elementos, loc='upper left', fontsize=9, 
                 framealpha=0.9, fancybox=True)
        
        fig.tight_layout()
        
        # Mostrar en ventana nueva
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("1100x750")
        
        # Frame para botones en la parte inferior
        frame_botones_mst = ttk.Frame(ventana)
        frame_botones_mst.pack(side='bottom', fill='x', padx=10, pady=5)
        
        ttk.Label(frame_botones_mst, text="🛠️ Opciones:").pack(side='left', padx=5)
        ttk.Button(frame_botones_mst, text="🔄 Regenerar Layout", 
                  command=lambda: self._regenerar_mst(ventana, grafo, mst, titulo)).pack(side='left', padx=5)
        ttk.Button(frame_botones_mst, text="💾 Guardar Imagen", 
                  command=lambda: self._guardar_figura(fig, ventana, "mst_grafo")).pack(side='left', padx=5)
        
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def _regenerar_mst(self, ventana, grafo, mst, titulo):
        """Regenera la visualización de MST con un layout diferente"""
        ventana.destroy()
        import time
        time.sleep(0.1)
        self.visualizar_mst(grafo, mst, titulo)
    
    def ejecutar_dijkstra(self):
        """Ejecuta el algoritmo de Dijkstra"""
        try:
            self.txt_resultado_dijkstra.delete('1.0', 'end')
            
            # Parsear aristas
            texto = self.txt_aristas_dijkstra.get('1.0', 'end').strip()
            origen = self.entry_origen.get().strip()
            
            if not origen:
                messagebox.showerror("Error", "Debe especificar un nodo origen")
                return
            
            es_dirigido = self.var_dirigido_dijkstra.get()
            
            grafo = {}
            for linea in texto.split('\n'):
                if linea.strip():
                    resultado = self._parsear_arista(linea, es_dirigido)
                    if resultado:
                        u, v, peso, es_bidireccional = resultado
                        
                        if u not in grafo:
                            grafo[u] = {}
                        if v not in grafo:
                            grafo[v] = {}
                        
                        # Agregar arista u → v siempre
                        grafo[u][v] = peso
                        
                        # Si es bidireccional, agregar también v → u
                        if es_bidireccional:
                            grafo[v][u] = peso
            
            if origen not in grafo:
                messagebox.showerror("Error", f"El nodo origen '{origen}' no existe en el grafo")
                return
            
            # Ejecutar Dijkstra
            tipo_grafo = "DIRIGIDO" if es_dirigido else "NO DIRIGIDO"
            self.txt_resultado_dijkstra.insert('end', "=" * 60 + "\n")
            self.txt_resultado_dijkstra.insert('end', "ALGORITMO DE DIJKSTRA\n")
            self.txt_resultado_dijkstra.insert('end', "=" * 60 + "\n\n")
            self.txt_resultado_dijkstra.insert('end', f"Tipo de grafo: {tipo_grafo}\n")
            self.txt_resultado_dijkstra.insert('end', f"Nodo origen: {origen}\n\n")
            
            distancias, predecesores, iteraciones = AlgoritmosGrafos.dijkstra(grafo, origen)
            
            # Mostrar iteraciones paso a paso
            self.txt_resultado_dijkstra.insert('end', "📊 PROCESO DE EXPLORACIÓN PASO A PASO:\n")
            self.txt_resultado_dijkstra.insert('end', "=" * 60 + "\n\n")
            
            for iter_data in iteraciones:
                self.txt_resultado_dijkstra.insert('end', 
                    f"🔵 ITERACIÓN {iter_data['num']}: Visitando nodo {iter_data['nodo_actual']} ")
                self.txt_resultado_dijkstra.insert('end', 
                    f"(distancia: {iter_data['dist_actual']:.1f})\n")
                
                if iter_data['actualizaciones']:
                    self.txt_resultado_dijkstra.insert('end', "   Actualizaciones:\n")
                    for act in iter_data['actualizaciones']:
                        self.txt_resultado_dijkstra.insert('end', 
                            f"   • {act['vecino']}: ")
                        if act['dist_anterior'] == float('inf'):
                            self.txt_resultado_dijkstra.insert('end', "∞")
                        else:
                            self.txt_resultado_dijkstra.insert('end', f"{act['dist_anterior']:.1f}")
                        self.txt_resultado_dijkstra.insert('end', 
                            f" → {act['dist_nueva']:.1f} (peso arista: {act['peso_arista']})\n")
                else:
                    self.txt_resultado_dijkstra.insert('end', "   ✓ Sin actualizaciones (nodo sin vecinos no visitados)\n")
                
                # Mostrar estado actual de distancias
                self.txt_resultado_dijkstra.insert('end', "\n   Estado actual de distancias:\n")
                self.txt_resultado_dijkstra.insert('end', "   ")
                nodos_ordenados = sorted(iter_data['distancias'].keys())
                for nodo in nodos_ordenados:
                    dist = iter_data['distancias'][nodo]
                    if dist == float('inf'):
                        dist_str = "∞"
                    else:
                        dist_str = f"{dist:.1f}"
                    
                    visitado = "✓" if nodo in iter_data['visitados'] else "○"
                    self.txt_resultado_dijkstra.insert('end', f"{nodo}:{dist_str}{visitado} ")
                self.txt_resultado_dijkstra.insert('end', "\n\n")
            
            self.txt_resultado_dijkstra.insert('end', "=" * 60 + "\n")
            self.txt_resultado_dijkstra.insert('end', "✅ RESULTADO FINAL - DISTANCIAS MÍNIMAS\n")
            self.txt_resultado_dijkstra.insert('end', "=" * 60 + "\n\n")
            
            nodos_alcanzables = 0
            for nodo in sorted(distancias.keys()):
                if distancias[nodo] == float('inf'):
                    self.txt_resultado_dijkstra.insert('end', f"{origen} → {nodo}: ∞ (no alcanzable)\n")
                else:
                    if nodo != origen:
                        nodos_alcanzables += 1
                    camino = self._reconstruir_camino(predecesores, origen, nodo)
                    self.txt_resultado_dijkstra.insert('end', 
                        f"{origen} → {nodo}: {distancias[nodo]}\n")
                    self.txt_resultado_dijkstra.insert('end', 
                        f"  Camino: {' → '.join(map(str, camino))}\n\n")
            
            # Información del Shortest Path Tree (SPT)
            self.txt_resultado_dijkstra.insert('end', "\n" + "=" * 60 + "\n")
            self.txt_resultado_dijkstra.insert('end', "🌳 SHORTEST PATH TREE (SPT)\n")
            self.txt_resultado_dijkstra.insert('end', "=" * 60 + "\n\n")
            
            self.txt_resultado_dijkstra.insert('end', f"Nodo raíz: {origen}\n")
            self.txt_resultado_dijkstra.insert('end', f"Nodos alcanzables: {nodos_alcanzables}\n")
            self.txt_resultado_dijkstra.insert('end', f"Aristas en el SPT: {nodos_alcanzables}\n\n")
            
            # Calcular peso total del SPT
            peso_total_spt = 0
            self.txt_resultado_dijkstra.insert('end', "Aristas del SPT (predecesor → nodo):\n")
            for nodo in sorted(grafo.keys()):
                if nodo != origen and predecesores.get(nodo) is not None:
                    pred = predecesores[nodo]
                    peso = grafo[pred][nodo]
                    peso_total_spt += peso
                    self.txt_resultado_dijkstra.insert('end', 
                        f"  {pred} → {nodo} (peso: {peso})\n")
            
            # Mostrar peso total del SPT
            self.txt_resultado_dijkstra.insert('end', f"\n{'='*60}\n")
            self.txt_resultado_dijkstra.insert('end', f"💰 PESO TOTAL DEL SPT: {peso_total_spt}\n")
            self.txt_resultado_dijkstra.insert('end', f"{'='*60}\n")
            
            # Visualizar el grafo con las rutas más cortas y el SPT
            self._visualizar_dijkstra(grafo, origen, distancias, predecesores)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar Dijkstra: {str(e)}")
    
    def _reconstruir_camino(self, predecesores, origen, destino):
        """Reconstruye un camino desde origen hasta destino"""
        if predecesores[destino] is None and destino != origen:
            return []
        
        camino = []
        nodo = destino
        while nodo is not None:
            camino.append(nodo)
            nodo = predecesores[nodo]
        
        return camino[::-1]
    
    def ejecutar_floyd_warshall(self):
        """Ejecuta el algoritmo de Floyd-Warshall"""
        try:
            self.txt_resultado_fw.delete('1.0', 'end')
            
            # Parsear aristas
            texto = self.txt_aristas_fw.get('1.0', 'end').strip()
            grafo = {}
            es_dirigido = self.var_dirigido_floyd.get()
            
            for linea in texto.split('\n'):
                if linea.strip():
                    resultado = self._parsear_arista(linea, es_dirigido)
                    if resultado:
                        u, v, peso, es_bidireccional = resultado
                        
                        # Agregar arista u -> v siempre
                        if u not in grafo:
                            grafo[u] = {}
                        grafo[u][v] = peso
                        
                        # Si es bidireccional, agregar también v -> u con el mismo peso
                        if es_bidireccional:
                            if v not in grafo:
                                grafo[v] = {}
                            grafo[v][u] = peso
            
            if not grafo:
                messagebox.showerror("Error", "No se encontraron aristas válidas")
                return
            
            # Asegurar que todos los nodos estén en el grafo
            nodos = set(grafo.keys())
            for vecinos in grafo.values():
                nodos.update(vecinos.keys())
            
            for nodo in nodos:
                if nodo not in grafo:
                    grafo[nodo] = {}
            
            # Ejecutar Floyd-Warshall
            self.txt_resultado_fw.insert('end', "=" * 60 + "\n")
            tipo_grafo = "DIRIGIDO" if es_dirigido else "NO DIRIGIDO"
            self.txt_resultado_fw.insert('end', f"ALGORITMO DE FLOYD-WARSHALL ({tipo_grafo})\n")
            self.txt_resultado_fw.insert('end', "=" * 60 + "\n\n")
            
            dist, sucesor, predecesor, nodos_lista, nodo_a_idx, iteraciones = AlgoritmosGrafos.floyd_warshall(grafo)
            
            # Mostrar iteraciones paso a paso con AMBAS MATRICES (D y S)
            self.txt_resultado_fw.insert('end', "📊 ITERACIONES PASO A PASO:\n")
            self.txt_resultado_fw.insert('end', "=" * 60 + "\n\n")
            
            for iter_data in iteraciones:
                if iter_data['k'] == 0:
                    self.txt_resultado_fw.insert('end', "🔵 ESTADO INICIAL (K=0):\n\n")
                else:
                    self.txt_resultado_fw.insert('end', f"\n{'='*60}\n")
                    self.txt_resultado_fw.insert('end', f"🔵 ITERACIÓN K={iter_data['k']} (nodo intermedio: {iter_data['nodo_intermedio']})\n")
                    self.txt_resultado_fw.insert('end', f"{'='*60}\n\n")
                
                if iter_data['cambios']:
                    self.txt_resultado_fw.insert('end', f"   📝 Cambios realizados: {len(iter_data['cambios'])}\n")
                    for cambio in iter_data['cambios'][:5]:  # Mostrar máximo 5 cambios
                        self.txt_resultado_fw.insert('end', 
                            f"      • {cambio['origen']}→{cambio['destino']}: ")
                        if cambio['dist_anterior'] == float('inf'):
                            self.txt_resultado_fw.insert('end', "∞")
                        else:
                            self.txt_resultado_fw.insert('end', f"{cambio['dist_anterior']:.1f}")
                        self.txt_resultado_fw.insert('end', 
                            f" → {cambio['dist_nueva']:.1f} (vía {cambio['via']})\n")
                    if len(iter_data['cambios']) > 5:
                        self.txt_resultado_fw.insert('end', 
                            f"      ... y {len(iter_data['cambios']) - 5} cambios más\n")
                    self.txt_resultado_fw.insert('end', "\n")
                else:
                    if iter_data['k'] > 0:
                        self.txt_resultado_fw.insert('end', "   ✓ No se realizaron cambios en esta iteración\n\n")
                
                # Mostrar MATRIZ D (Distancias)
                n = len(nodos_lista)
                self.txt_resultado_fw.insert('end', "   📐 MATRIZ D (Distancias):\n")
                self.txt_resultado_fw.insert('end', "      ")
                for nodo in nodos_lista:
                    self.txt_resultado_fw.insert('end', f"{str(nodo):>6}")
                self.txt_resultado_fw.insert('end', "\n")
                
                for i, nodo in enumerate(nodos_lista):
                    self.txt_resultado_fw.insert('end', f"   {str(nodo):>4}: ")
                    for j in range(n):
                        val = iter_data['matriz_d'][i][j]
                        if val == float('inf'):
                            self.txt_resultado_fw.insert('end', "   ∞  ")
                        else:
                            self.txt_resultado_fw.insert('end', f"{val:>6.1f}")
                    self.txt_resultado_fw.insert('end', "\n")
                
                # Mostrar MATRIZ S (Sucesores) - Estilo Profesor
                self.txt_resultado_fw.insert('end', "\n   🧭 MATRIZ S (Sucesores - siguiente nodo):\n")
                self.txt_resultado_fw.insert('end', "      ")
                for nodo in nodos_lista:
                    self.txt_resultado_fw.insert('end', f"{str(nodo):>6}")
                self.txt_resultado_fw.insert('end', "\n")
                
                for i, nodo in enumerate(nodos_lista):
                    self.txt_resultado_fw.insert('end', f"   {str(nodo):>4}: ")
                    for j in range(n):
                        val = iter_data['matriz_s'][i][j]
                        if val is None:
                            self.txt_resultado_fw.insert('end', "   -  ")
                        else:
                            self.txt_resultado_fw.insert('end', f"{str(val):>6}")
                    self.txt_resultado_fw.insert('end', "\n")
                
                # Mostrar MATRIZ P (Predecesores)
                self.txt_resultado_fw.insert('end', "\n   📍 MATRIZ P (Predecesores - nodo anterior):\n")
                self.txt_resultado_fw.insert('end', "      ")
                for nodo in nodos_lista:
                    self.txt_resultado_fw.insert('end', f"{str(nodo):>6}")
                self.txt_resultado_fw.insert('end', "\n")
                
                for i, nodo in enumerate(nodos_lista):
                    self.txt_resultado_fw.insert('end', f"   {str(nodo):>4}: ")
                    for j in range(n):
                        val = iter_data['matriz_p'][i][j]
                        if val is None:
                            self.txt_resultado_fw.insert('end', "   -  ")
                        else:
                            self.txt_resultado_fw.insert('end', f"{str(val):>6}")
                    self.txt_resultado_fw.insert('end', "\n")
                self.txt_resultado_fw.insert('end', "\n")
            
            self.txt_resultado_fw.insert('end', "=" * 60 + "\n")
            self.txt_resultado_fw.insert('end', "✅ RESULTADO FINAL\n")
            self.txt_resultado_fw.insert('end', "=" * 60 + "\n")
            self.txt_resultado_fw.insert('end', "\nMATRIZ DE DISTANCIAS FINAL:\n\n")
            
            # Imprimir matriz
            n = len(nodos_lista)
            self.txt_resultado_fw.insert('end', "      ")
            for nodo in nodos_lista:
                self.txt_resultado_fw.insert('end', f"{str(nodo):>6}")
            self.txt_resultado_fw.insert('end', "\n")
            
            for i, nodo in enumerate(nodos_lista):
                self.txt_resultado_fw.insert('end', f"{str(nodo):>4}: ")
                for j in range(n):
                    val = dist[i][j]
                    if val == float('inf'):
                        self.txt_resultado_fw.insert('end', "   ∞  ")
                    else:
                        self.txt_resultado_fw.insert('end', f"{val:>6.1f}")
                self.txt_resultado_fw.insert('end', "\n")
            
            # Guardar resultados para consultas posteriores
            self.floyd_dist = dist
            self.floyd_next = sucesor  # Matriz de sucesores para reconstruir caminos
            self.floyd_pred = predecesor  # Matriz de predecesores (alternativa)
            self.floyd_nodos = nodos_lista
            self.floyd_nodo_a_idx = nodo_a_idx
            
            # Visualizar el grafo
            self._visualizar_floyd_warshall(grafo, dist, nodos_lista)
            
            self.txt_resultado_fw.insert('end', "\n" + "="*60 + "\n")
            self.txt_resultado_fw.insert('end', "💡 TIP: Usa la sección 'Consultar Ruta Específica' arriba\n")
            self.txt_resultado_fw.insert('end', "    para ver el camino y distancia entre dos nodos.\n")
            self.txt_resultado_fw.insert('end', "="*60 + "\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar Floyd-Warshall: {str(e)}")
    
    def consultar_ruta_floyd(self):
        """Consulta la ruta y distancia específica entre dos nodos después de Floyd-Warshall"""
        try:
            # Verificar que se haya ejecutado Floyd-Warshall primero
            if not hasattr(self, 'floyd_dist') or self.floyd_dist is None:
                messagebox.showwarning("Advertencia", 
                    "Debes ejecutar Floyd-Warshall primero antes de consultar rutas.")
                return
            
            # Obtener origen y destino
            origen_str = self.entry_origen_fw.get().strip()
            destino_str = self.entry_destino_fw.get().strip()
            
            if not origen_str or not destino_str:
                messagebox.showwarning("Advertencia", 
                    "Debes especificar tanto el origen como el destino.")
                return
            
            # Intentar encontrar el nodo en floyd_nodos (puede ser str o int)
            origen = None
            destino = None
            
            # Buscar origen
            for nodo in self.floyd_nodos:
                if str(nodo) == origen_str:
                    origen = nodo
                    break
            
            # Buscar destino  
            for nodo in self.floyd_nodos:
                if str(nodo) == destino_str:
                    destino = nodo
                    break
            
            # Verificar que los nodos existan
            if origen is None or destino is None:
                nodos_disponibles = ', '.join(map(str, sorted(self.floyd_nodos)))
                messagebox.showerror("Error", 
                    f"Nodos no válidos.\nNodos disponibles: {nodos_disponibles}")
                return

            
            # Obtener índices
            i = self.floyd_nodo_a_idx[origen]
            j = self.floyd_nodo_a_idx[destino]
            
            # Obtener distancia
            distancia = self.floyd_dist[i][j]
            
            # Reconstruir camino
            if distancia == float('inf'):
                messagebox.showinfo("Resultado", 
                    f"No existe un camino de {origen} a {destino}.\nDistancia: ∞")
                return
            
            if origen == destino:
                messagebox.showinfo("Resultado", 
                    f"Origen y destino son el mismo nodo.\nDistancia: 0")
                return
            
            # Reconstruir el camino usando la matriz de sucesores
            camino = self._reconstruir_camino_floyd(origen, destino)
            
            if not camino:
                messagebox.showinfo("Resultado", 
                    f"No se pudo reconstruir el camino de {origen} a {destino}.")
                return
            
            # Mostrar resultado en una ventana emergente
            resultado = f"""
╔══════════════════════════════════════════════════════╗
║  RUTA ESPECÍFICA: {origen} → {destino}
╚══════════════════════════════════════════════════════╝

📍 ORIGEN:    {origen}
🎯 DESTINO:   {destino}
📏 DISTANCIA: {distancia:.2f}

🛣️  CAMINO COMPLETO:
    {' → '.join(map(str, camino))}

📊 DETALLES POR SEGMENTO:
"""
            
            # Calcular distancia de cada segmento
            for idx in range(len(camino) - 1):
                nodo_actual = camino[idx]
                nodo_siguiente = camino[idx + 1]
                idx_actual = self.floyd_nodo_a_idx[nodo_actual]
                idx_siguiente = self.floyd_nodo_a_idx[nodo_siguiente]
                dist_segmento = self.floyd_dist[idx_actual][idx_siguiente]
                resultado += f"    Paso {idx+1}: {nodo_actual} → {nodo_siguiente}  (distancia: {dist_segmento:.2f})\n"
            
            resultado += f"\n{'='*54}\n"
            resultado += f"✅ DISTANCIA TOTAL: {distancia:.2f}\n"
            resultado += f"{'='*54}"
            
            # Crear ventana con el resultado
            ventana_resultado = tk.Toplevel(self.root)
            ventana_resultado.title(f"Ruta: {origen} → {destino}")
            ventana_resultado.geometry("600x500")
            
            # Texto con scroll
            text_resultado = scrolledtext.ScrolledText(ventana_resultado, 
                                                       font=('Consolas', 11),
                                                       wrap='word')
            text_resultado.pack(fill='both', expand=True, padx=10, pady=10)
            text_resultado.insert('1.0', resultado)
            text_resultado.config(state='disabled')
            
            # Botón para cerrar
            ttk.Button(ventana_resultado, text="Cerrar", 
                      command=ventana_resultado.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al consultar ruta: {str(e)}")
    
    def _reconstruir_camino_floyd(self, origen, destino):
        """Reconstruye el camino entre origen y destino usando la matriz de sucesores"""
        if origen == destino:
            return [origen]
        
        i = self.floyd_nodo_a_idx[origen]
        j = self.floyd_nodo_a_idx[destino]
        
        if self.floyd_next[i][j] is None:
            return []
        
        # Reconstruir usando sucesores (siguiente nodo en el camino)
        camino = [origen]
        actual = origen
        
        while actual != destino:
            idx_actual = self.floyd_nodo_a_idx[actual]
            idx_destino = self.floyd_nodo_a_idx[destino]
            siguiente = self.floyd_next[idx_actual][idx_destino]
            
            if siguiente is None or siguiente == actual:
                return []
            
            camino.append(siguiente)
            actual = siguiente
            
            # Protección contra bucles infinitos
            if len(camino) > len(self.floyd_nodos):
                return []
        
        return camino
    
    def ejecutar_flujo_maximo(self):
        """Ejecuta el algoritmo de Ford-Fulkerson"""
        try:
            self._actualizar_status("Calculando flujo máximo...", "loading")
            self.txt_resultado_flujo.delete('1.0', 'end')
            
            # Parsear entrada
            texto = self.txt_aristas_flujo.get('1.0', 'end').strip()
            origen = self.entry_origen_flujo.get().strip()
            destino = self.entry_destino_flujo.get().strip()
            
            # Convertir a enteros si es posible
            try:
                origen = int(origen)
                destino = int(destino)
            except:
                pass
            
            grafo = {}
            nodos = set()  # Para rastrear todos los nodos
            
            for linea in texto.split('\n'):
                if linea.strip():
                    # Flujo máximo normalmente es dirigido, pero soportamos híbrido
                    resultado = self._parsear_arista(linea, es_dirigido_global=True)
                    if resultado:
                        u, v, cap, es_bidireccional = resultado
                        
                        # Convertir a enteros si es posible
                        try:
                            u = int(u)
                            v = int(v)
                        except:
                            pass
                        
                        nodos.add(u)
                        nodos.add(v)
                        
                        # Agregar arista u → v
                        if u not in grafo:
                            grafo[u] = {}
                        grafo[u][v] = cap
                        
                        # Si es bidireccional, agregar también v → u
                        if es_bidireccional:
                            if v not in grafo:
                                grafo[v] = {}
                            grafo[v][u] = cap
            
            # Asegurar que TODOS los nodos estén en el grafo (incluso sin aristas salientes)
            for nodo in nodos:
                if nodo not in grafo:
                    grafo[nodo] = {}
            
            # Asegurar que origen y destino existan
            if origen not in grafo:
                grafo[origen] = {}
            if destino not in grafo:
                grafo[destino] = {}
            
            # Ejecutar Ford-Fulkerson con iteraciones detalladas
            flujo_maximo, caminos, visitados, iteraciones = self._ford_fulkerson(grafo, origen, destino)
            
            self.txt_resultado_flujo.insert('end', "=" * 60 + "\n")
            self.txt_resultado_flujo.insert('end', "ALGORITMO DE FORD-FULKERSON\n")
            self.txt_resultado_flujo.insert('end', "=" * 60 + "\n\n")
            self.txt_resultado_flujo.insert('end', f"Origen: {origen}\n")
            self.txt_resultado_flujo.insert('end', f"Destino: {destino}\n\n")
            
            # Mostrar iteraciones paso a paso
            self.txt_resultado_flujo.insert('end', "📊 ITERACIONES PASO A PASO:\n")
            self.txt_resultado_flujo.insert('end', "=" * 60 + "\n\n")
            
            for iter_data in iteraciones:
                if iter_data['tipo'] == 'camino_encontrado':
                    self.txt_resultado_flujo.insert('end', 
                        f"🔵 RUTA DE AVANCE {iter_data['num']}:\n")
                    self.txt_resultado_flujo.insert('end', "=" * 60 + "\n")
                    self.txt_resultado_flujo.insert('end', 
                        f"   Camino: {' → '.join(map(str, iter_data['camino']))}\n\n")
                    
                    self.txt_resultado_flujo.insert('end', "   📐 Capacidades residuales en el camino:\n")
                    for u, v, cap in iter_data['aristas']:
                        self.txt_resultado_flujo.insert('end', 
                            f"      c_{u}{v} = {cap:.0f}\n")
                    
                    self.txt_resultado_flujo.insert('end', 
                        f"\n   🔹 Flujo máximo en esta ruta:\n")
                    self.txt_resultado_flujo.insert('end',
                        f"      f_{iter_data['num']} = min{{{', '.join([f'{cap:.0f}' for u, v, cap in iter_data['aristas']])}}} = {iter_data['flujo_camino']:.0f}\n\n")
                    
                    # Mostrar actualización de residuos
                    self.txt_resultado_flujo.insert('end', "   🔄 Actualización de capacidades residuales:\n")
                    
                    # Mostrar cambios en dirección del flujo (reducir)
                    self.txt_resultado_flujo.insert('end', "      Dirección del flujo (reducir capacidad):\n")
                    for u, v, cap_antes in iter_data['aristas']:
                        cap_despues = cap_antes - iter_data['flujo_camino']
                        self.txt_resultado_flujo.insert('end',
                            f"         c_{u}{v} = {cap_antes:.0f} - {iter_data['flujo_camino']:.0f} = {cap_despues:.0f}\n")
                    
                    # Mostrar cambios en dirección inversa (incrementar)
                    self.txt_resultado_flujo.insert('end', "\n      Dirección inversa (incrementar capacidad):\n")
                    for i in range(len(iter_data['camino']) - 1):
                        u, v = iter_data['camino'][i], iter_data['camino'][i + 1]
                        # Obtener capacidad residual inversa antes
                        cap_inversa_antes = iter_data['capacidades_residuales_antes'].get((v, u), 0)
                        cap_inversa_despues = cap_inversa_antes + iter_data['flujo_camino']
                        self.txt_resultado_flujo.insert('end',
                            f"         c_{v}{u} = {cap_inversa_antes:.0f} + {iter_data['flujo_camino']:.0f} = {cap_inversa_despues:.0f}\n")
                    
                    self.txt_resultado_flujo.insert('end', 
                        f"\n   � Flujo acumulado hasta ahora: {iter_data['flujo_acumulado']:.0f}\n\n")
                    
                elif iter_data['tipo'] == 'no_camino':
                    self.txt_resultado_flujo.insert('end', 
                        f"🔵 ITERACIÓN {iter_data['num']}:\n")
                    self.txt_resultado_flujo.insert('end', "=" * 60 + "\n")
                    self.txt_resultado_flujo.insert('end', 
                        f"   ❌ No se encontró ruta de avance adicional\n")
                    self.txt_resultado_flujo.insert('end', 
                        f"   ✓ Algoritmo terminado\n\n")
            
            self.txt_resultado_flujo.insert('end', "=" * 60 + "\n")
            self.txt_resultado_flujo.insert('end', "✅ RESUMEN DE RUTAS DE AVANCE\n")
            self.txt_resultado_flujo.insert('end', "=" * 60 + "\n\n")
            
            for i, (camino, flujo) in enumerate(caminos, 1):
                self.txt_resultado_flujo.insert('end', 
                    f"  Ruta {i}: {' → '.join(map(str, camino))}\n")
                self.txt_resultado_flujo.insert('end',
                    f"          f_{i} = {flujo:.0f}\n\n")
            
            # Mostrar cálculo del flujo máximo
            self.txt_resultado_flujo.insert('end', "=" * 60 + "\n")
            self.txt_resultado_flujo.insert('end', "🎯 FLUJO MÁXIMO\n")
            self.txt_resultado_flujo.insert('end', "=" * 60 + "\n\n")
            
            flujos_str = ' + '.join([f"f_{i}" for i in range(1, len(caminos) + 1)])
            flujos_valores = ' + '.join([f"{flujo:.0f}" for _, flujo in caminos])
            
            self.txt_resultado_flujo.insert('end', f"  F = {flujos_str}\n")
            self.txt_resultado_flujo.insert('end', f"  F = {flujos_valores}\n")
            self.txt_resultado_flujo.insert('end', f"  F = {flujo_maximo:.0f}\n\n")
            
            # Calcular flujo real en cada arista
            flujos = {}
            for u in grafo:
                for v in grafo[u]:
                    flujos[(u, v)] = 0
            
            # Sumar el flujo de cada camino
            for camino, flujo in caminos:
                for i in range(len(camino) - 1):
                    u, v = camino[i], camino[i + 1]
                    if (u, v) in flujos:
                        flujos[(u, v)] += flujo
            
            # Mostrar tabla de flujos
            self.txt_resultado_flujo.insert('end', "=" * 60 + "\n")
            self.txt_resultado_flujo.insert('end', "📋 FLUJO ÓPTIMO EN CADA ARCO\n")
            self.txt_resultado_flujo.insert('end', "=" * 60 + "\n\n")
            self.txt_resultado_flujo.insert('end', "  Arco     Cap. Diseño  Cap. Residual  Flujo Óptimo\n")
            self.txt_resultado_flujo.insert('end', "  (i,j)      (C̄ᵢⱼ)         (cᵢⱼ)           (α)\n")
            self.txt_resultado_flujo.insert('end', "-" * 60 + "\n")
            
            # Recopilar todas las aristas con capacidad
            todas_aristas = []
            for u in sorted(grafo.keys()):
                for v in sorted(grafo[u].keys()):
                    cap_original = grafo[u][v]
                    flujo_usado = flujos.get((u, v), 0)
                    residual = cap_original - flujo_usado
                    todas_aristas.append((u, v, cap_original, residual, flujo_usado))
            
            # Mostrar tabla ordenada
            for u, v, cap_original, residual, flujo_usado in todas_aristas:
                self.txt_resultado_flujo.insert('end', 
                    f"  ({u},{v})       {cap_original:>4.0f}           {residual:>4.0f}            {flujo_usado:>4.0f}\n")
            
            self.txt_resultado_flujo.insert('end', "-" * 60 + "\n")
            self.txt_resultado_flujo.insert('end', f"\n💡 El flujo óptimo (α) es el flujo que circula por cada arco.\n")
            self.txt_resultado_flujo.insert('end', f"   La capacidad residual (cᵢⱼ) es la capacidad restante después del flujo.\n\n")
            
            # Corte mínimo (visitados ya viene del algoritmo)
            corte = []
            cap_corte = 0
            for u in visitados:
                if u in grafo:
                    for v in grafo[u]:
                        if v not in visitados:
                            corte.append((u, v, grafo[u][v]))
                            cap_corte += grafo[u][v]
            
            self.txt_resultado_flujo.insert('end', "\n" + "=" * 60 + "\n")
            self.txt_resultado_flujo.insert('end', "🔪 CORTE MÍNIMO\n")
            self.txt_resultado_flujo.insert('end', "=" * 60 + "\n\n")
            self.txt_resultado_flujo.insert('end', f"Nodos alcanzables desde {origen}: {sorted(visitados)}\n")
            self.txt_resultado_flujo.insert('end', f"Nodos no alcanzables: {sorted(set(grafo.keys()) - visitados)}\n")
            self.txt_resultado_flujo.insert('end', "\nAristas en el corte:\n")
            for u, v, cap in corte:
                self.txt_resultado_flujo.insert('end', f"  {u} → {v}: {cap}\n")
            self.txt_resultado_flujo.insert('end', f"\nCapacidad del corte: {cap_corte}\n")
            
            # Visualizar el grafo de flujo
            self._visualizar_flujo_maximo(grafo, caminos, origen, destino, visitados)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular flujo máximo: {str(e)}\n{type(e).__name__}")
    
    def resolver_juego_suma_cero(self):
        """Resuelve un juego de suma cero"""
        try:
            from scipy.optimize import linprog
            
            self.txt_resultado_juego.delete('1.0', 'end')
            
            # Parsear matriz
            texto = self.txt_matriz_juego.get('1.0', 'end').strip()
            matriz = []
            
            for linea in texto.split('\n'):
                if linea.strip():
                    fila = [float(x) for x in linea.strip().split()]
                    matriz.append(fila)
            
            matriz = np.array(matriz)
            m, n = matriz.shape
            
            self.txt_resultado_juego.insert('end', "=" * 60 + "\n")
            self.txt_resultado_juego.insert('end', "JUEGO DE SUMA CERO\n")
            self.txt_resultado_juego.insert('end', "=" * 60 + "\n\n")
            
            self.txt_resultado_juego.insert('end', "Matriz de pagos (Jugador A):\n")
            for i, fila in enumerate(matriz):
                self.txt_resultado_juego.insert('end', f"  Estrategia {i+1}: {fila}\n")
            
            # Resolver con programación lineal
            # Jugador A (maximizar)
            c = np.zeros(m + 1)
            c[-1] = -1
            
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
                
                # Mostrar explicación del proceso
                self.txt_resultado_juego.insert('end', "\n" + "=" * 60 + "\n")
                self.txt_resultado_juego.insert('end', "📊 PROCESO DE SOLUCIÓN\n")
                self.txt_resultado_juego.insert('end', "=" * 60 + "\n\n")
                
                self.txt_resultado_juego.insert('end', "🔹 PASO 1: Formulación del problema del Jugador A\n")
                self.txt_resultado_juego.insert('end', "   Maximizar: v (valor del juego)\n")
                self.txt_resultado_juego.insert('end', f"   Variables: p₁, p₂, ..., p_{m}, v\n")
                self.txt_resultado_juego.insert('end', f"   Restricciones ({n} restricciones, una por columna):\n")
                for j in range(min(3, n)):  # Mostrar máximo 3 restricciones
                    restriccion = " + ".join([f"{matriz[i][j]:.1f}p{i+1}" for i in range(m)])
                    self.txt_resultado_juego.insert('end', f"      {restriccion} ≥ v\n")
                if n > 3:
                    self.txt_resultado_juego.insert('end', f"      ... y {n-3} restricciones más\n")
                self.txt_resultado_juego.insert('end', f"      p₁ + p₂ + ... + p_{m} = 1\n")
                self.txt_resultado_juego.insert('end', "      pᵢ ≥ 0 para todo i\n\n")
                
                self.txt_resultado_juego.insert('end', f"   ✓ Problema resuelto con método Simplex\n")
                self.txt_resultado_juego.insert('end', f"   ✓ Iteraciones del simplex: {resultado.nit if hasattr(resultado, 'nit') else 'N/A'}\n\n")
                
                # Calcular estrategia del Jugador B (columnas)
                c_b = np.zeros(n + 1)
                c_b[-1] = 1
                
                A_ub_b = []
                b_ub_b = []
                for i in range(m):
                    fila = [matriz[i][j] for j in range(n)] + [-1]
                    A_ub_b.append(fila)
                    b_ub_b.append(0)
                
                A_eq_b = [[1] * n + [0]]
                b_eq_b = [1]
                
                bounds_b = [(0, None)] * n + [(None, None)]
                
                resultado_b = linprog(c_b, A_ub=A_ub_b, b_ub=b_ub_b, A_eq=A_eq_b, 
                                     b_eq=b_eq_b, bounds=bounds_b, method='highs')
                
                estrategia_b = resultado_b.x[:-1] if resultado_b.success else None
                
                self.txt_resultado_juego.insert('end', "🔹 PASO 2: Formulación del problema del Jugador B\n")
                self.txt_resultado_juego.insert('end', "   Minimizar: v (valor del juego)\n")
                self.txt_resultado_juego.insert('end', f"   Variables: q₁, q₂, ..., q_{n}, v\n")
                self.txt_resultado_juego.insert('end', f"   Restricciones ({m} restricciones, una por fila):\n")
                for i in range(min(3, m)):  # Mostrar máximo 3 restricciones
                    restriccion = " + ".join([f"{matriz[i][j]:.1f}q{j+1}" for j in range(n)])
                    self.txt_resultado_juego.insert('end', f"      {restriccion} ≤ v\n")
                if m > 3:
                    self.txt_resultado_juego.insert('end', f"      ... y {m-3} restricciones más\n")
                self.txt_resultado_juego.insert('end', f"      q₁ + q₂ + ... + q_{n} = 1\n")
                self.txt_resultado_juego.insert('end', "      qⱼ ≥ 0 para todo j\n\n")
                
                if resultado_b.success:
                    self.txt_resultado_juego.insert('end', f"   ✓ Problema resuelto con método Simplex\n")
                    self.txt_resultado_juego.insert('end', f"   ✓ Iteraciones del simplex: {resultado_b.nit if hasattr(resultado_b, 'nit') else 'N/A'}\n\n")
                
                # Mostrar resultados
                self.txt_resultado_juego.insert('end', "=" * 60 + "\n")
                self.txt_resultado_juego.insert('end', "✅ SOLUCIÓN ÓPTIMA\n")
                self.txt_resultado_juego.insert('end', "=" * 60 + "\n\n")
                
                # Jugador A
                self.txt_resultado_juego.insert('end', "🎮 ESTRATEGIA ÓPTIMA JUGADOR A (Filas):\n")
                self.txt_resultado_juego.insert('end', "-" * 60 + "\n")
                for i, prob in enumerate(estrategia_a):
                    if prob > 0.001:
                        self.txt_resultado_juego.insert('end', 
                            f"  ✓ Estrategia {i+1}: {prob:.4f} = {prob*100:.2f}%\n")
                    else:
                        self.txt_resultado_juego.insert('end', 
                            f"    Estrategia {i+1}: 0.0000 = 0.00% (no usar)\n")
                
                # Jugador B
                if estrategia_b is not None:
                    self.txt_resultado_juego.insert('end', "\n🎯 ESTRATEGIA ÓPTIMA JUGADOR B (Columnas):\n")
                    self.txt_resultado_juego.insert('end', "-" * 60 + "\n")
                    for j, prob in enumerate(estrategia_b):
                        if prob > 0.001:
                            self.txt_resultado_juego.insert('end', 
                                f"  ✓ Estrategia {j+1}: {prob:.4f} = {prob*100:.2f}%\n")
                        else:
                            self.txt_resultado_juego.insert('end', 
                                f"    Estrategia {j+1}: 0.0000 = 0.00% (no usar)\n")
                
                # Valor del juego
                self.txt_resultado_juego.insert('end', f"\n{'='*60}\n")
                self.txt_resultado_juego.insert('end', f"💰 VALOR DEL JUEGO: {valor_juego:.4f}\n")
                self.txt_resultado_juego.insert('end', f"{'='*60}\n\n")
                
                # Interpretación
                if valor_juego > 0:
                    self.txt_resultado_juego.insert('end', 
                        "📊 INTERPRETACIÓN:\n")
                    self.txt_resultado_juego.insert('end',
                        f"El juego favorece al Jugador A con ganancia esperada de {valor_juego:.4f}\n")
                elif valor_juego < 0:
                    self.txt_resultado_juego.insert('end', 
                        "📊 INTERPRETACIÓN:\n")
                    self.txt_resultado_juego.insert('end',
                        f"El juego favorece al Jugador B con ganancia esperada de {abs(valor_juego):.4f}\n")
                else:
                    self.txt_resultado_juego.insert('end', 
                        "📊 INTERPRETACIÓN:\n")
                    self.txt_resultado_juego.insert('end',
                        "El juego es justo (equilibrado). Ambos jugadores tienen ganancia esperada 0.\n")
                
                # Valor esperado para cada estrategia pura de A
                self.txt_resultado_juego.insert('end', "\n📈 VALORES ESPERADOS POR ESTRATEGIA PURA:\n")
                self.txt_resultado_juego.insert('end', "-" * 60 + "\n")
                self.txt_resultado_juego.insert('end', "Si el Jugador A usa estrategia pura contra estrategia óptima de B:\n")
                for i in range(m):
                    valor_esp = sum(matriz[i][j] * estrategia_b[j] for j in range(n)) if estrategia_b is not None else 0
                    self.txt_resultado_juego.insert('end', 
                        f"  Estrategia {i+1}: {valor_esp:.4f}\n")
                
                # Visualizar con gráficos
                self._visualizar_estrategias_juego(estrategia_a, estrategia_b, valor_juego, matriz)
                
            else:
                self.txt_resultado_juego.insert('end', "\n❌ No se pudo resolver el juego.\n")
                self.txt_resultado_juego.insert('end', "Verifica que la matriz sea correcta.\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver el juego: {str(e)}")
    
    def _visualizar_dijkstra(self, grafo, origen, distancias, predecesores):
        """Visualiza el grafo completo y el Shortest Path Tree (SPT) con mejoras visuales"""
        # Crear nueva ventana
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Dijkstra - Rutas más cortas desde {origen}")
        ventana.geometry("1500x800")
        
        # Detectar si el grafo es dirigido
        es_dirigido = self.var_dirigido_dijkstra.get()
        
        # Crear grafo de NetworkX (dirigido o no dirigido)
        if es_dirigido:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        
        for u in grafo:
            for v, peso in grafo[u].items():
                G.add_edge(u, v, weight=peso)
        
        # Calcular tamaños dinámicos
        n_nodos = G.number_of_nodes()
        node_size = self._calcular_tamano_nodos(n_nodos)
        font_size = self._calcular_tamano_fuente(n_nodos)
        font_size_edges = max(7, font_size - 2)
        arrow_size = max(15, 25 - n_nodos)
        
        # Crear figura con 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        # Layout inteligente (compartido entre ambas visualizaciones)
        pos = self._calcular_layout_inteligente(G)
        
        # ============================================
        # SUBPLOT 1: Grafo completo con caminos destacados
        # ============================================
        
        # Construir el Shortest Path Tree
        spt_edges = []
        for nodo in G.nodes():
            if nodo != origen and predecesores.get(nodo) is not None:
                pred = predecesores[nodo]
                spt_edges.append((pred, nodo))
        
        # Dibujar todos los nodos con colores semánticos
        node_colors = []
        for node in G.nodes():
            if node == origen:
                node_colors.append('#27AE60')  # Verde para origen
            elif distancias.get(node, float('inf')) == float('inf'):
                node_colors.append('#95A5A6')  # Gris para inalcanzables
            else:
                node_colors.append('#3498DB')  # Azul para alcanzables
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=node_size, ax=ax1,
                              edgecolors='#2C3E50', linewidths=2)
        
        # Separar aristas
        edges_spt = []
        edges_other = []
        
        for u, v in G.edges():
            if (u, v) in spt_edges or (not es_dirigido and (v, u) in spt_edges):
                edges_spt.append((u, v))
            else:
                edges_other.append((u, v))
        
        # Dibujar aristas normales (no en SPT)
        if es_dirigido:
            if edges_other:
                nx.draw_networkx_edges(G, pos, edgelist=edges_other, 
                                      edge_color='#BDC3C7', width=1.5, 
                                      arrows=True, arrowsize=arrow_size, 
                                      style='dashed', ax=ax1,
                                      min_source_margin=15, min_target_margin=15)
            # Dibujar aristas del SPT
            if edges_spt:
                nx.draw_networkx_edges(G, pos, edgelist=edges_spt, 
                                      edge_color='#E74C3C', width=3.5,
                                      arrows=True, arrowsize=arrow_size + 5, ax=ax1,
                                      min_source_margin=15, min_target_margin=15)
        else:
            if edges_other:
                nx.draw_networkx_edges(G, pos, edgelist=edges_other, 
                                      edge_color='#BDC3C7', width=1.5,
                                      style='dashed', ax=ax1)
            # Dibujar aristas del SPT
            if edges_spt:
                nx.draw_networkx_edges(G, pos, edgelist=edges_spt, 
                                      edge_color='#E74C3C', width=3.5, ax=ax1)
        
        # Etiquetas de nodos
        nx.draw_networkx_labels(G, pos, font_size=font_size, font_weight='bold', ax=ax1)
        
        # Etiquetas de pesos con fondo
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=font_size_edges, ax=ax1,
                                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                                             edgecolor='none', alpha=0.85))
        
        ax1.set_title(f"Grafo Completo\n(Aristas del SPT en rojo)", 
                     fontsize=14, fontweight='bold', pad=20)
        ax1.axis('off')
        
        # Leyenda para subplot 1
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch
        leyenda1 = [
            Patch(facecolor='#27AE60', edgecolor='#2C3E50', label=f'Origen: {origen}'),
            Patch(facecolor='#3498DB', edgecolor='#2C3E50', label='Nodos alcanzables'),
            Patch(facecolor='#95A5A6', edgecolor='#2C3E50', label='Nodos inalcanzables'),
            Line2D([0], [0], color='#E74C3C', linewidth=3.5, label='Aristas del SPT'),
            Line2D([0], [0], color='#BDC3C7', linewidth=1.5, linestyle='--', label='Otras aristas')
        ]
        ax1.legend(handles=leyenda1, loc='upper left', fontsize=8, framealpha=0.9)
        
        # ============================================
        # SUBPLOT 2: Solo el Shortest Path Tree (SPT)
        # ============================================
        
        # Crear grafo solo con el SPT
        if es_dirigido:
            SPT = nx.DiGraph()
        else:
            SPT = nx.Graph()
        
        # Agregar nodos alcanzables
        for nodo in G.nodes():
            if nodo == origen or distancias.get(nodo, float('inf')) != float('inf'):
                SPT.add_node(nodo)
        
        # Agregar aristas del SPT con sus pesos
        for pred, nodo in spt_edges:
            peso = grafo[pred][nodo]
            SPT.add_edge(pred, nodo, weight=peso)
        
        # Dibujar nodos del SPT
        node_colors_spt = []
        for node in SPT.nodes():
            if node == origen:
                node_colors_spt.append('#27AE60')  # Verde para origen
            else:
                node_colors_spt.append('#3498DB')  # Azul para otros
        
        nx.draw_networkx_nodes(SPT, pos, node_color=node_colors_spt, 
                              node_size=node_size, ax=ax2,
                              edgecolors='#2C3E50', linewidths=2)
        
        # Dibujar aristas del SPT con flechas más visibles
        if es_dirigido:
            nx.draw_networkx_edges(SPT, pos, edge_color='#E74C3C', 
                                  width=3.5, arrows=True, arrowsize=arrow_size + 5, ax=ax2,
                                  min_source_margin=15, min_target_margin=15)
        else:
            nx.draw_networkx_edges(SPT, pos, edge_color='#E74C3C', 
                                  width=3.5, ax=ax2)
        
        # Etiquetas de nodos
        nx.draw_networkx_labels(SPT, pos, font_size=font_size, font_weight='bold', ax=ax2)
        
        # Etiquetas de pesos (solo aristas del SPT) con fondo
        spt_edge_labels = nx.get_edge_attributes(SPT, 'weight')
        nx.draw_networkx_edge_labels(SPT, pos, spt_edge_labels, font_size=font_size_edges, ax=ax2,
                                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                                             edgecolor='none', alpha=0.85))
        
        # Calcular peso total del SPT
        peso_total_spt = sum(grafo[pred][nodo] for pred, nodo in spt_edges)
        
        # Agregar información sobre distancias y peso total
        info_text = f"[o] Nodo origen: {origen}\n"
        info_text += f"[+] Nodos alcanzables: {len(SPT.nodes()) - 1}\n"
        info_text += f"[-] Aristas en SPT: {len(spt_edges)}\n"
        info_text += f"{'─' * 22}\n"
        info_text += f"[$] Peso Total SPT: {peso_total_spt:.1f}\n"
        info_text += f"{'─' * 22}\n\n"
        info_text += "Distancias desde origen:\n"
        for nodo in sorted(SPT.nodes(), key=str):
            if nodo != origen:
                dist = distancias.get(nodo, float('inf'))
                info_text += f"  {origen}→{nodo}: {dist:.1f}\n"
        
        ax2.text(0.02, 0.98, info_text, transform=ax2.transAxes,
                fontsize=9, verticalalignment='top', family='monospace',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF9E7', 
                         edgecolor='#F39C12', alpha=0.95))
        
        ax2.set_title(f"Shortest Path Tree (SPT)\n(Solo aristas del árbol)", 
                     fontsize=14, fontweight='bold', pad=20)
        ax2.axis('off')
        
        fig.tight_layout()
        
        # Frame para botones
        frame_botones = ttk.Frame(ventana)
        frame_botones.pack(side='bottom', fill='x', padx=10, pady=5)
        
        ttk.Label(frame_botones, text="🛠️ Opciones:").pack(side='left', padx=5)
        ttk.Button(frame_botones, text="🔄 Regenerar Layout", 
                  command=lambda: self._regenerar_dijkstra(ventana, grafo, origen, distancias, predecesores)).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="💾 Guardar Imagen", 
                  command=lambda: self._guardar_figura(fig, ventana, f"dijkstra_{origen}")).pack(side='left', padx=5)
        
        # Mostrar en ventana
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self._actualizar_status("Visualización de Dijkstra creada", "success")
    
    def _regenerar_dijkstra(self, ventana, grafo, origen, distancias, predecesores):
        """Regenera la visualización de Dijkstra con un layout diferente"""
        ventana.destroy()
        import time
        time.sleep(0.1)  # Pequeña pausa para evitar conflictos
        self._visualizar_dijkstra(grafo, origen, distancias, predecesores)
    
    def _visualizar_floyd_warshall(self, grafo, dist, nodos_lista):
        """Visualiza el grafo con todas las distancias mínimas - Versión mejorada"""
        # Crear nueva ventana
        ventana = tk.Toplevel(self.root)
        ventana.title("Floyd-Warshall - Todas las distancias")
        ventana.geometry("1100x800")
        
        # Crear grafo de NetworkX (dirigido)
        G = nx.DiGraph()
        for u in grafo:
            for v, peso in grafo[u].items():
                G.add_edge(u, v, weight=peso)
        
        # Calcular tamaños dinámicos
        n_nodos = G.number_of_nodes()
        node_size = self._calcular_tamano_nodos(n_nodos)
        font_size = self._calcular_tamano_fuente(n_nodos)
        font_size_edges = max(7, font_size - 2)
        arrow_size = max(15, 25 - n_nodos)
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 9))
        
        # Layout inteligente
        pos = self._calcular_layout_inteligente(G)
        
        # Dibujar nodos con borde
        nx.draw_networkx_nodes(G, pos, node_color='#AED6F1', 
                              node_size=node_size, ax=ax,
                              edgecolors='#2980B9', linewidths=2)
        
        # Detectar aristas bidireccionales (con posibles pesos diferentes)
        aristas_bidireccionales = set()
        aristas_simples = []
        
        for u in grafo:
            for v in grafo[u]:
                if v in grafo and u in grafo[v]:
                    # Es bidireccional
                    if (v, u) not in aristas_bidireccionales:
                        aristas_bidireccionales.add((u, v))
                else:
                    # Es unidireccional
                    aristas_simples.append((u, v))
        
        # Dibujar aristas simples (unidireccionales) rectas
        if aristas_simples:
            nx.draw_networkx_edges(G, pos, edgelist=aristas_simples,
                                  edge_color='#7F8C8D', width=2.5, 
                                  arrows=True, arrowsize=arrow_size,
                                  connectionstyle='arc3,rad=0', ax=ax,
                                  min_source_margin=15, min_target_margin=15)
        
        # Dibujar aristas bidireccionales con curvas para evitar superposición
        if aristas_bidireccionales:
            # Separar en dos listas para las dos direcciones
            aristas_ida = list(aristas_bidireccionales)
            aristas_vuelta = [(v, u) for u, v in aristas_bidireccionales]
            
            # Dibujar con diferentes curvaturas y colores
            nx.draw_networkx_edges(G, pos, edgelist=aristas_ida,
                                  edge_color='#3498DB', width=2.5, 
                                  arrows=True, arrowsize=arrow_size,
                                  connectionstyle='arc3,rad=0.15', ax=ax,
                                  min_source_margin=15, min_target_margin=15)
            
            nx.draw_networkx_edges(G, pos, edgelist=aristas_vuelta,
                                  edge_color='#E74C3C', width=2.5, 
                                  arrows=True, arrowsize=arrow_size,
                                  connectionstyle='arc3,rad=0.15', ax=ax,
                                  min_source_margin=15, min_target_margin=15)
        
        # Etiquetas de nodos
        nx.draw_networkx_labels(G, pos, font_size=font_size, font_weight='bold', ax=ax)
        
        # Para aristas curvas, dibujar etiquetas manualmente en la posición correcta
        for u in grafo:
            for v, peso in grafo[u].items():
                # Calcular posición de la etiqueta
                x1, y1 = pos[u]
                x2, y2 = pos[v]
                
                # Si es bidireccional, desplazar la etiqueta hacia el lado curvo
                if (u, v) in aristas_bidireccionales or (v, u) in aristas_bidireccionales:
                    # Punto medio
                    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                    # Vector perpendicular para el desplazamiento
                    dx, dy = x2 - x1, y2 - y1
                    length = (dx**2 + dy**2)**0.5
                    if length > 0:
                        # Normalizar y desplazar perpendicularmente
                        perpx, perpy = -dy / length, dx / length
                        offset = 0.08  # Desplazamiento
                        
                        # Determinar el lado según la dirección
                        if (u, v) in aristas_bidireccionales:
                            label_x = mx + perpx * offset
                            label_y = my + perpy * offset
                        else:
                            label_x = mx - perpx * offset
                            label_y = my - perpy * offset
                        
                        ax.text(label_x, label_y, f"{peso}", fontsize=font_size_edges,
                               ha='center', va='center',
                               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                                        edgecolor='none', alpha=0.9))
                else:
                    # Arista simple, etiqueta en el medio
                    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                    ax.text(mx, my, f"{peso}", fontsize=font_size_edges,
                           ha='center', va='center',
                           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                                    edgecolor='none', alpha=0.9))
        
        # Determinar tipo de grafo para el título
        es_dirigido = self.var_dirigido_floyd.get()
        tipo_grafo = "Dirigido" if es_dirigido else "No Dirigido"
        ax.set_title(f"Floyd-Warshall - Grafo {tipo_grafo}\n(Ver matriz en resultados)", 
                    fontsize=14, fontweight='bold', pad=15)
        ax.axis('off')
        
        # Agregar información de distancias más cortas
        n = len(nodos_lista)
        info_text = "[*] Resumen del Grafo:\n"
        info_text += f"{'─' * 22}\n"
        info_text += f"Nodos: {', '.join(map(str, nodos_lista))}\n"
        info_text += f"Total de nodos: {n}\n"
        info_text += f"Total de pares: {n * n}\n"
        
        # Contar caminos finitos
        finitos = sum(1 for i in range(n) for j in range(n) 
                     if dist[i][j] != float('inf') and i != j)
        info_text += f"Caminos encontrados: {finitos}\n"
        info_text += f"{'─' * 22}\n"
        info_text += "[i] Consulta rutas especificas\n   en el panel izquierdo"
        
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
               fontsize=9, verticalalignment='top', family='monospace',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF9E7', 
                        edgecolor='#F39C12', alpha=0.95))
        
        # Agregar leyenda mejorada
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch
        leyenda_elementos = [
            Patch(facecolor='#AED6F1', edgecolor='#2980B9', linewidth=2, label=f'Nodos ({n} total)')
        ]
        if aristas_bidireccionales:
            leyenda_elementos.append(
                Line2D([0], [0], color='#3498DB', linewidth=2.5, label='Arista dirección →'))
            leyenda_elementos.append(
                Line2D([0], [0], color='#E74C3C', linewidth=2.5, label='Arista dirección ←'))
        if aristas_simples:
            leyenda_elementos.append(
                Line2D([0], [0], color='#7F8C8D', linewidth=2.5, label='Arista unidireccional'))
        
        ax.legend(handles=leyenda_elementos, loc='lower right', fontsize=8, 
                 framealpha=0.9, fancybox=True)
        
        fig.tight_layout()
        
        # Frame para botones
        frame_botones_fw = ttk.Frame(ventana)
        frame_botones_fw.pack(side='bottom', fill='x', padx=10, pady=5)
        
        ttk.Label(frame_botones_fw, text="🛠️ Opciones:").pack(side='left', padx=5)
        ttk.Button(frame_botones_fw, text="🔄 Regenerar Layout", 
                  command=lambda: self._regenerar_floyd_warshall(ventana, grafo, dist, nodos_lista)).pack(side='left', padx=5)
        ttk.Button(frame_botones_fw, text="💾 Guardar Imagen", 
                  command=lambda: self._guardar_figura(fig, ventana, "floyd_warshall")).pack(side='left', padx=5)
        
        # Mostrar en ventana
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.status_bar.config(text="✅ Visualización de Floyd-Warshall creada")
    
    def _regenerar_floyd_warshall(self, ventana, grafo, dist, nodos_lista):
        """Regenera la visualización de Floyd-Warshall"""
        ventana.destroy()
        import time
        time.sleep(0.1)
        self._visualizar_floyd_warshall(grafo, dist, nodos_lista)
    
    def _visualizar_estrategias_juego(self, estrategia_a, estrategia_b, valor_juego, matriz):
        """Visualiza las estrategias óptimas con gráficos"""
        try:
            # Crear figura con múltiples subgráficos
            fig = plt.figure(figsize=(14, 10))
            
            # 1. Gráfico de barras para Jugador A
            ax1 = plt.subplot(2, 2, 1)
            estrategias_a_idx = [f"E{i+1}" for i in range(len(estrategia_a))]
            colores_a = ['#2ecc71' if p > 0.001 else '#ecf0f1' for p in estrategia_a]
            barras_a = ax1.bar(estrategias_a_idx, estrategia_a, color=colores_a, alpha=0.8, edgecolor='black')
            ax1.set_title('🎮 Estrategia Óptima Jugador A', fontsize=12, fontweight='bold')
            ax1.set_xlabel('Estrategias (Filas)', fontsize=10)
            ax1.set_ylabel('Probabilidad', fontsize=10)
            ax1.set_ylim(0, 1)
            ax1.grid(axis='y', alpha=0.3)
            
            # Añadir valores en las barras
            for barra in barras_a:
                altura = barra.get_height()
                if altura > 0.001:
                    ax1.text(barra.get_x() + barra.get_width()/2., altura,
                            f'{altura:.3f}\n{altura*100:.1f}%',
                            ha='center', va='bottom', fontsize=9, fontweight='bold')
            
            # 2. Gráfico de barras para Jugador B
            if estrategia_b is not None:
                ax2 = plt.subplot(2, 2, 2)
                estrategias_b_idx = [f"E{j+1}" for j in range(len(estrategia_b))]
                colores_b = ['#3498db' if p > 0.001 else '#ecf0f1' for p in estrategia_b]
                barras_b = ax2.bar(estrategias_b_idx, estrategia_b, color=colores_b, alpha=0.8, edgecolor='black')
                ax2.set_title('🎯 Estrategia Óptima Jugador B', fontsize=12, fontweight='bold')
                ax2.set_xlabel('Estrategias (Columnas)', fontsize=10)
                ax2.set_ylabel('Probabilidad', fontsize=10)
                ax2.set_ylim(0, 1)
                ax2.grid(axis='y', alpha=0.3)
                
                # Añadir valores en las barras
                for barra in barras_b:
                    altura = barra.get_height()
                    if altura > 0.001:
                        ax2.text(barra.get_x() + barra.get_width()/2., altura,
                                f'{altura:.3f}\n{altura*100:.1f}%',
                                ha='center', va='bottom', fontsize=9, fontweight='bold')
            
            # 3. Mapa de calor de la matriz de pagos
            ax3 = plt.subplot(2, 2, 3)
            im = ax3.imshow(matriz, cmap='RdYlGn', aspect='auto', interpolation='nearest')
            ax3.set_title('🎲 Matriz de Pagos', fontsize=12, fontweight='bold')
            ax3.set_xlabel('Estrategias Jugador B', fontsize=10)
            ax3.set_ylabel('Estrategias Jugador A', fontsize=10)
            
            # Añadir valores en las celdas
            for i in range(len(matriz)):
                for j in range(len(matriz[0])):
                    texto = ax3.text(j, i, f'{matriz[i][j]:.1f}',
                                   ha="center", va="center", color="black", fontsize=10, fontweight='bold')
            
            # Etiquetas de ejes
            ax3.set_xticks(range(len(matriz[0])))
            ax3.set_yticks(range(len(matriz)))
            ax3.set_xticklabels([f'E{j+1}' for j in range(len(matriz[0]))])
            ax3.set_yticklabels([f'E{i+1}' for i in range(len(matriz))])
            
            # Barra de color
            plt.colorbar(im, ax=ax3, label='Ganancia para A')
            
            # 4. Resumen del juego
            ax4 = plt.subplot(2, 2, 4)
            ax4.axis('off')
            
            # Texto del resumen
            resumen = f"""
📊 RESUMEN DEL JUEGO

💰 Valor del Juego: {valor_juego:.4f}

🎮 Jugador A (Filas):
"""
            for i, prob in enumerate(estrategia_a):
                if prob > 0.001:
                    resumen += f"   ✓ E{i+1}: {prob*100:.1f}%\n"
            
            if estrategia_b is not None:
                resumen += "\n🎯 Jugador B (Columnas):\n"
                for j, prob in enumerate(estrategia_b):
                    if prob > 0.001:
                        resumen += f"   ✓ E{j+1}: {prob*100:.1f}%\n"
            
            resumen += "\n📈 Interpretación:\n"
            if valor_juego > 0:
                resumen += f"   El juego favorece a A\n   Ganancia esperada: {valor_juego:.4f}"
            elif valor_juego < 0:
                resumen += f"   El juego favorece a B\n   Ganancia esperada: {abs(valor_juego):.4f}"
            else:
                resumen += "   Juego equilibrado\n   Ambos jugadores empatan"
            
            ax4.text(0.1, 0.95, resumen, transform=ax4.transAxes,
                    fontsize=11, verticalalignment='top',
                    family='monospace',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo visualizar: {str(e)}")
    
    def _ford_fulkerson(self, grafo, origen, destino):
        """Implementación del algoritmo Ford-Fulkerson para flujo máximo con iteraciones
        Usa DFS con estrategia Greedy (prioriza arcos de mayor capacidad)"""
        from collections import defaultdict, deque
        
        # Crear grafo residual
        residual = defaultdict(lambda: defaultdict(int))
        for u in grafo:
            for v in grafo[u]:
                residual[u][v] = grafo[u][v]
                if v not in residual:
                    residual[v] = defaultdict(int)
                if u not in residual[v]:
                    residual[v][u] = 0
        
        # Lista para guardar iteraciones
        iteraciones = []
        
        def dfs_greedy_camino(source, sink, num_iter):
            """Busca un camino aumentante usando DFS con estrategia Greedy
            Prioriza los arcos de mayor capacidad primero"""
            
            nodos_explorados = []
            
            def dfs_recursivo(current, visited, path):
                """Búsqueda recursiva en profundidad con estrategia greedy"""
                visited.add(current)
                nodos_explorados.append(current)
                
                # Si llegamos al sumidero, devolvemos el camino
                if current == sink:
                    return path + [sink]
                
                # Encontrar vecinos no visitados con capacidad positiva
                vecinos_validos = []
                for vecino in residual[current]:
                    if vecino not in visited and residual[current][vecino] > 0:
                        capacidad = residual[current][vecino]
                        vecinos_validos.append((vecino, capacidad))
                
                # Ordenar vecinos por capacidad descendente (estrategia Greedy)
                vecinos_validos.sort(key=lambda x: x[1], reverse=True)
                
                # Intentar avanzar por el camino de mayor capacidad primero
                for vecino, _ in vecinos_validos:
                    camino_encontrado = dfs_recursivo(vecino, visited.copy(), path + [current])
                    if camino_encontrado is not None:
                        return camino_encontrado
                
                # Retroceso: ningún vecino lleva al sumidero
                return None
            
            camino = dfs_recursivo(source, set(), [])
            return camino, nodos_explorados
        
        flujo_total = 0
        caminos_encontrados = []
        num_iteracion = 0
        
        # Encontrar caminos aumentantes usando DFS Greedy
        while True:
            num_iteracion += 1
            camino, nodos_explorados = dfs_greedy_camino(origen, destino, num_iteracion)
            
            if not camino:
                # No hay más caminos aumentantes
                iteraciones.append({
                    'num': num_iteracion,
                    'tipo': 'no_camino',
                    'nodos_explorados': nodos_explorados,
                    'flujo_acumulado': flujo_total
                })
                break
            
            # Encontrar flujo mínimo (cuello de botella) en el camino
            aristas_camino = []
            flujo_minimo = float('inf')
            for i in range(len(camino) - 1):
                u, v = camino[i], camino[i + 1]
                cap_residual = residual[u][v]
                aristas_camino.append((u, v, cap_residual))
                flujo_minimo = min(flujo_minimo, cap_residual)
            
            # Guardar estado antes de actualizar
            capacidades_antes = {(u, v): residual[u][v] for u in residual for v in residual[u] if residual[u][v] > 0}
            
            # Actualizar grafo residual
            for i in range(len(camino) - 1):
                u, v = camino[i], camino[i + 1]
                residual[u][v] -= flujo_minimo
                residual[v][u] += flujo_minimo
            
            flujo_total += flujo_minimo
            caminos_encontrados.append((camino, flujo_minimo))
            
            # Registrar iteración
            iteraciones.append({
                'num': num_iteracion,
                'tipo': 'camino_encontrado',
                'camino': camino,
                'aristas': aristas_camino,
                'flujo_camino': flujo_minimo,
                'flujo_acumulado': flujo_total,
                'nodos_explorados': nodos_explorados,
                'capacidades_residuales_antes': capacidades_antes
            })
        
        # Encontrar nodos visitables desde origen en grafo residual (corte mínimo)
        visitados = {origen}
        cola = deque([origen])
        while cola:
            u = cola.popleft()
            for v in residual[u]:
                if v not in visitados and residual[u][v] > 0:
                    visitados.add(v)
                    cola.append(v)
        
        return flujo_total, caminos_encontrados, visitados, iteraciones
    
    def _visualizar_flujo_maximo(self, grafo, caminos, origen, destino, visitados):
        """Visualiza el grafo de flujo máximo con flujos en las aristas - Versión mejorada"""
        # Calcular flujo real en cada arista
        flujos = {}
        for u in grafo:
            for v in grafo[u]:
                flujos[(u, v)] = 0
        
        # Sumar el flujo de cada camino
        for camino, flujo in caminos:
            for i in range(len(camino) - 1):
                u, v = camino[i], camino[i + 1]
                if (u, v) in flujos:
                    flujos[(u, v)] += flujo
        
        # Crear nueva ventana
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Flujo Máximo: {origen} → {destino}")
        ventana.geometry("1100x800")
        
        # Crear grafo de NetworkX (dirigido)
        G = nx.DiGraph()
        for u in grafo:
            for v, cap in grafo[u].items():
                flujo_arista = flujos.get((u, v), 0)
                G.add_edge(u, v, capacity=cap, flow=flujo_arista)
        
        # Calcular tamaños dinámicos
        n_nodos = G.number_of_nodes()
        node_size = self._calcular_tamano_nodos(n_nodos)
        font_size = self._calcular_tamano_fuente(n_nodos)
        font_size_edges = max(7, font_size - 1)
        arrow_size = max(15, 25 - n_nodos)
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 9))
        
        # Layout inteligente
        pos = self._calcular_layout_inteligente(G)
        
        # Colorear nodos según el corte mínimo
        node_colors = []
        for node in G.nodes():
            if node == origen:
                node_colors.append('#2ECC71')  # Verde brillante para origen
            elif node == destino:
                node_colors.append('#E74C3C')  # Rojo para destino
            elif node in visitados:
                node_colors.append('#AED6F1')  # Azul claro - Lado del origen
            else:
                node_colors.append('#F9E79F')  # Amarillo - Lado del destino
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=node_size, ax=ax,
                              edgecolors='#2C3E50', linewidths=2)
        
        # Dibujar aristas con diferentes colores según si cruzan el corte
        edges_corte = []
        edges_saturadas = []
        edges_con_flujo = []
        edges_sin_flujo = []
        
        for u, v in G.edges():
            flujo_arista = flujos.get((u, v), 0)
            cap_arista = grafo[u][v]
            
            if u in visitados and v not in visitados:
                edges_corte.append((u, v))
            elif flujo_arista >= cap_arista - 0.01:  # Saturada
                edges_saturadas.append((u, v))
            elif flujo_arista > 0:
                edges_con_flujo.append((u, v))
            else:
                edges_sin_flujo.append((u, v))
        
        # Aristas sin flujo (gris, discontinuas)
        if edges_sin_flujo:
            nx.draw_networkx_edges(G, pos, edgelist=edges_sin_flujo, 
                                  edge_color='#BDC3C7', width=1.5, 
                                  arrows=True, arrowsize=arrow_size, ax=ax, 
                                  style='dashed',
                                  min_source_margin=15, min_target_margin=15)
        
        # Aristas con flujo parcial (azul)
        if edges_con_flujo:
            nx.draw_networkx_edges(G, pos, edgelist=edges_con_flujo, 
                                  edge_color='#3498DB', width=2.5, 
                                  arrows=True, arrowsize=arrow_size, ax=ax,
                                  min_source_margin=15, min_target_margin=15)
        
        # Aristas saturadas (verde oscuro)
        if edges_saturadas:
            nx.draw_networkx_edges(G, pos, edgelist=edges_saturadas, 
                                  edge_color='#27AE60', width=3.5, 
                                  arrows=True, arrowsize=arrow_size + 3, ax=ax,
                                  min_source_margin=15, min_target_margin=15)
        
        # Aristas del corte en rojo (muy gruesas y destacadas)
        if edges_corte:
            nx.draw_networkx_edges(G, pos, edgelist=edges_corte, 
                                  edge_color='#C0392B', width=4.5, 
                                  arrows=True, arrowsize=arrow_size + 8, ax=ax,
                                  min_source_margin=15, min_target_margin=15)
        
        # Etiquetas de nodos
        nx.draw_networkx_labels(G, pos, font_size=font_size, font_weight='bold', ax=ax)
        
        # Etiquetas de aristas mostrando flujo/capacidad con fondo
        edge_labels = {}
        for u, v in G.edges():
            flujo_arista = flujos.get((u, v), 0)
            cap_arista = grafo[u][v]
            edge_labels[(u, v)] = f"{flujo_arista:.0f}/{cap_arista:.0f}"
        
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=font_size_edges, ax=ax,
                                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                                             edgecolor='none', alpha=0.9))
        
        # Calcular flujo total
        flujo_total = sum(flujos.get((origen, v), 0) for v in grafo.get(origen, {}).keys())
        
        ax.set_title(f"Flujo Máximo: {flujo_total:.0f} unidades\n{origen} → {destino}", 
                    fontsize=14, fontweight='bold', pad=15)
        ax.axis('off')
        
        # Leyenda mejorada con más información
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch
        
        leyenda_elementos = [
            Patch(facecolor='#2ECC71', edgecolor='#2C3E50', linewidth=2, label=f'Origen: {origen}'),
            Patch(facecolor='#E74C3C', edgecolor='#2C3E50', linewidth=2, label=f'Destino: {destino}'),
            Patch(facecolor='#AED6F1', edgecolor='#2C3E50', linewidth=2, label='Lado origen (S)'),
            Patch(facecolor='#F9E79F', edgecolor='#2C3E50', linewidth=2, label='Lado destino (T)'),
            Line2D([0], [0], color='#C0392B', linewidth=4.5, label='[X] Corte minimo'),
            Line2D([0], [0], color='#27AE60', linewidth=3.5, label='Arista saturada'),
            Line2D([0], [0], color='#3498DB', linewidth=2.5, label='Con flujo parcial'),
            Line2D([0], [0], color='#BDC3C7', linewidth=1.5, linestyle='--', label='Sin flujo'),
        ]
        ax.legend(handles=leyenda_elementos, loc='upper right', fontsize=8, 
                 framealpha=0.95, fancybox=True, ncol=1)
        
        # Cuadro de resumen
        resumen = f"[*] RESUMEN\n{'─' * 20}\n"
        resumen += f"Flujo maximo: {flujo_total:.0f}\n"
        resumen += f"Caminos usados: {len(caminos)}\n"
        resumen += f"Aristas del corte: {len(edges_corte)}\n"
        resumen += f"Aristas saturadas: {len(edges_saturadas)}\n"
        
        ax.text(0.02, 0.98, resumen, transform=ax.transAxes,
               fontsize=9, verticalalignment='top', family='monospace',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF9E7', 
                        edgecolor='#F39C12', alpha=0.95))
        
        fig.tight_layout()
        
        # Frame para botones
        frame_botones_flujo = ttk.Frame(ventana)
        frame_botones_flujo.pack(side='bottom', fill='x', padx=10, pady=5)
        
        ttk.Label(frame_botones_flujo, text="🛠️ Opciones:").pack(side='left', padx=5)
        ttk.Button(frame_botones_flujo, text="🔄 Regenerar Layout", 
                  command=lambda: self._regenerar_flujo_maximo(ventana, grafo, caminos, origen, destino, visitados)).pack(side='left', padx=5)
        ttk.Button(frame_botones_flujo, text="💾 Guardar Imagen", 
                  command=lambda: self._guardar_figura(fig, ventana, f"flujo_maximo_{origen}_{destino}")).pack(side='left', padx=5)
        
        # Mostrar en ventana
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self._actualizar_status("Visualización de Flujo Máximo creada", "success")
    
    def _regenerar_flujo_maximo(self, ventana, grafo, caminos, origen, destino, visitados):
        """Regenera la visualización de Flujo Máximo"""
        ventana.destroy()
        import time
        time.sleep(0.1)
        self._visualizar_flujo_maximo(grafo, caminos, origen, destino, visitados)
    
    def crear_pestaña_programacion_lineal(self):
        """Pestaña para Programación Lineal General"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Programación Lineal")
        
        # Frame principal con scroll
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        titulo = ttk.Label(main_frame, text="📊 Programación Lineal General", 
                          font=('Arial', 16, 'bold'))
        titulo.pack(pady=10)
        
        # Instrucciones
        instrucciones = """
📘 INSTRUCCIONES:
• Este módulo resuelve problemas generales de Programación Lineal
• Soporta maximización y minimización con restricciones
• Variables pueden ser continuas, enteras o binarias
• Muestra solución óptima, valor objetivo y análisis de sensibilidad

FORMATO DE ENTRADA:
• Función objetivo: coeficientes separados por espacios (ej: "3 5 2" para 3x₁ + 5x₂ + 2x₃)
• Restricciones: coeficiente₁ coeficiente₂ ... tipo valor
  Tipos: <= (menor o igual), >= (mayor o igual), = (igualdad)
  Ejemplo: "2 3 4 <= 10" significa 2x₁ + 3x₂ + 4x₃ ≤ 10
        """
        lbl_instr = ttk.Label(main_frame, text=instrucciones, justify='left', 
                             font=('Consolas', 10))
        lbl_instr.pack(pady=5)
        
        # Frame de entrada
        entrada_frame = ttk.LabelFrame(main_frame, text="Configuración del Problema", padding=10)
        entrada_frame.pack(fill='both', expand=True, pady=10)
        
        # Tipo de problema
        tipo_frame = ttk.Frame(entrada_frame)
        tipo_frame.pack(fill='x', pady=5)
        
        ttk.Label(tipo_frame, text="Tipo de problema:", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        self.var_tipo_pl = tk.StringVar(value="max")
        ttk.Radiobutton(tipo_frame, text="Maximizar", variable=self.var_tipo_pl, 
                       value="max").pack(side='left', padx=10)
        ttk.Radiobutton(tipo_frame, text="Minimizar", variable=self.var_tipo_pl, 
                       value="min").pack(side='left', padx=10)
        
        # Número de variables
        num_vars_frame = ttk.Frame(entrada_frame)
        num_vars_frame.pack(fill='x', pady=5)
        
        ttk.Label(num_vars_frame, text="Número de variables:", 
                 font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        self.var_num_vars = tk.StringVar(value="2")
        ttk.Entry(num_vars_frame, textvariable=self.var_num_vars, width=10).pack(side='left', padx=5)
        
        # Función objetivo
        obj_frame = ttk.LabelFrame(entrada_frame, text="Función Objetivo", padding=10)
        obj_frame.pack(fill='x', pady=10)
        
        ttk.Label(obj_frame, text="Coeficientes (separados por espacios):", 
                 font=('Arial', 10)).pack(anchor='w')
        self.txt_objetivo_pl = tk.Text(obj_frame, height=2, font=('Consolas', 11))
        self.txt_objetivo_pl.pack(fill='x', pady=5)
        self.txt_objetivo_pl.insert('1.0', "3 5")  # Ejemplo por defecto
        
        # Restricciones
        rest_frame = ttk.LabelFrame(entrada_frame, text="Restricciones", padding=10)
        rest_frame.pack(fill='both', expand=True, pady=10)
        
        ttk.Label(rest_frame, text="Una restricción por línea (formato: coef₁ coef₂ ... tipo valor):", 
                 font=('Arial', 10)).pack(anchor='w')
        
        # Frame con scrollbar para restricciones
        scroll_rest = ttk.Scrollbar(rest_frame)
        scroll_rest.pack(side='right', fill='y')
        
        self.txt_restricciones_pl = tk.Text(rest_frame, height=8, font=('Consolas', 11),
                                           yscrollcommand=scroll_rest.set)
        self.txt_restricciones_pl.pack(fill='both', expand=True)
        scroll_rest.config(command=self.txt_restricciones_pl.yview)
        
        # Ejemplo por defecto
        ejemplo_restricciones = """2 1 <= 10
1 2 <= 8
1 0 <= 4"""
        self.txt_restricciones_pl.insert('1.0', ejemplo_restricciones)
        
        # Tipo de variables
        tipo_vars_frame = ttk.Frame(entrada_frame)
        tipo_vars_frame.pack(fill='x', pady=5)
        
        ttk.Label(tipo_vars_frame, text="Tipo de variables:", 
                 font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        self.var_tipo_variables = tk.StringVar(value="continuas")
        ttk.Radiobutton(tipo_vars_frame, text="Continuas", 
                       variable=self.var_tipo_variables, value="continuas").pack(side='left', padx=5)
        ttk.Radiobutton(tipo_vars_frame, text="Enteras", 
                       variable=self.var_tipo_variables, value="enteras").pack(side='left', padx=5)
        ttk.Radiobutton(tipo_vars_frame, text="Binarias (0-1)", 
                       variable=self.var_tipo_variables, value="binarias").pack(side='left', padx=5)
        
        # Botones
        botones_frame = ttk.Frame(entrada_frame)
        botones_frame.pack(fill='x', pady=10)
        
        ttk.Button(botones_frame, text="🚀 Resolver", 
                  command=self.resolver_pl).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="📋 Ejemplo 1 (Maximizar)", 
                  command=self.cargar_ejemplo_pl1).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="📋 Ejemplo 2 (Minimizar)", 
                  command=self.cargar_ejemplo_pl2).pack(side='left', padx=5)
        ttk.Button(botones_frame, text="🗑️ Limpiar", 
                  command=self.limpiar_pl).pack(side='left', padx=5)
        
        # Área de resultados
        resultado_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
        resultado_frame.pack(fill='both', expand=True, pady=10)
        
        scroll_res = ttk.Scrollbar(resultado_frame)
        scroll_res.pack(side='right', fill='y')
        
        self.txt_resultado_pl = tk.Text(resultado_frame, height=15, font=('Consolas', 11),
                                        yscrollcommand=scroll_res.set)
        self.txt_resultado_pl.pack(fill='both', expand=True)
        scroll_res.config(command=self.txt_resultado_pl.yview)
    
    def cargar_ejemplo_pl1(self):
        """Carga ejemplo de maximización"""
        self.var_tipo_pl.set("max")
        self.var_num_vars.set("2")
        self.txt_objetivo_pl.delete('1.0', 'end')
        self.txt_objetivo_pl.insert('1.0', "3 5")
        self.txt_restricciones_pl.delete('1.0', 'end')
        self.txt_restricciones_pl.insert('1.0', """2 1 <= 10
1 2 <= 8
1 0 <= 4
0 1 <= 5""")
        self.var_tipo_variables.set("continuas")
        messagebox.showinfo("Ejemplo", "Ejemplo cargado:\nMaximizar Z = 3x₁ + 5x₂\nSujeto a restricciones mostradas")
    
    def cargar_ejemplo_pl2(self):
        """Carga ejemplo de minimización"""
        self.var_tipo_pl.set("min")
        self.var_num_vars.set("2")
        self.txt_objetivo_pl.delete('1.0', 'end')
        self.txt_objetivo_pl.insert('1.0', "2 3")
        self.txt_restricciones_pl.delete('1.0', 'end')
        self.txt_restricciones_pl.insert('1.0', """1 1 >= 4
2 1 >= 6
0 1 >= 1""")
        self.var_tipo_variables.set("continuas")
        messagebox.showinfo("Ejemplo", "Ejemplo cargado:\nMinimizar Z = 2x₁ + 3x₂\nSujeto a restricciones mostradas")
    
    def limpiar_pl(self):
        """Limpia los campos de PL"""
        self.txt_objetivo_pl.delete('1.0', 'end')
        self.txt_restricciones_pl.delete('1.0', 'end')
        self.txt_resultado_pl.delete('1.0', 'end')
        self.var_num_vars.set("2")
    
    def resolver_pl(self):
        """Resuelve el problema de Programación Lineal"""
        try:
            self.txt_resultado_pl.delete('1.0', 'end')
            
            # Obtener datos
            tipo = self.var_tipo_pl.get()
            num_vars = int(self.var_num_vars.get())
            
            # Función objetivo
            obj_text = self.txt_objetivo_pl.get('1.0', 'end').strip()
            c = list(map(float, obj_text.split()))
            
            if len(c) != num_vars:
                raise ValueError(f"Se esperaban {num_vars} coeficientes en la función objetivo, se encontraron {len(c)}")
            
            # Si es maximización, negamos los coeficientes
            if tipo == "max":
                c = [-x for x in c]
            
            # Restricciones
            rest_text = self.txt_restricciones_pl.get('1.0', 'end').strip()
            lineas = [l.strip() for l in rest_text.split('\n') if l.strip()]
            
            A_ub = []
            b_ub = []
            A_eq = []
            b_eq = []
            
            for i, linea in enumerate(lineas, 1):
                partes = linea.split()
                if len(partes) < num_vars + 2:
                    raise ValueError(f"Restricción {i} incompleta. Formato: coef₁ ... coefₙ tipo valor")
                
                coeficientes = list(map(float, partes[:num_vars]))
                tipo_rest = partes[num_vars]
                valor = float(partes[num_vars + 1])
                
                if tipo_rest == '<=':
                    A_ub.append(coeficientes)
                    b_ub.append(valor)
                elif tipo_rest == '>=':
                    A_ub.append([-x for x in coeficientes])
                    b_ub.append(-valor)
                elif tipo_rest == '=':
                    A_eq.append(coeficientes)
                    b_eq.append(valor)
                else:
                    raise ValueError(f"Tipo de restricción inválido en línea {i}: '{tipo_rest}'. Use <=, >= o =")
            
            # Configurar bounds según tipo de variables
            tipo_vars = self.var_tipo_variables.get()
            if tipo_vars == "continuas":
                bounds = [(0, None)] * num_vars
            elif tipo_vars == "enteras":
                bounds = [(0, None)] * num_vars
            elif tipo_vars == "binarias":
                bounds = [(0, 1)] * num_vars
            
            # Resolver
            A_ub_array = np.array(A_ub) if A_ub else None
            b_ub_array = np.array(b_ub) if b_ub else None
            A_eq_array = np.array(A_eq) if A_eq else None
            b_eq_array = np.array(b_eq) if b_eq else None
            
            # Para variables enteras/binarias usamos método 'highs'
            metodo = 'highs'
            integrality = None
            if tipo_vars in ["enteras", "binarias"]:
                integrality = np.ones(num_vars)
            
            resultado = linprog(c, A_ub=A_ub_array, b_ub=b_ub_array, 
                              A_eq=A_eq_array, b_eq=b_eq_array, 
                              bounds=bounds, method=metodo, integrality=integrality)
            
            # Mostrar resultados
            self.txt_resultado_pl.insert('end', "=" * 70 + "\n")
            self.txt_resultado_pl.insert('end', "PROBLEMA DE PROGRAMACIÓN LINEAL\n")
            self.txt_resultado_pl.insert('end', "=" * 70 + "\n\n")
            
            # Mostrar problema
            self.txt_resultado_pl.insert('end', f"📝 {'MAXIMIZAR' if tipo == 'max' else 'MINIMIZAR'}:\n")
            obj_str = " + ".join([f"{abs(c[i]):.2f}x{i+1}" if tipo == 'max' else f"{c[i]:.2f}x{i+1}" 
                                 for i in range(num_vars)])
            self.txt_resultado_pl.insert('end', f"   Z = {obj_str}\n\n")
            
            self.txt_resultado_pl.insert('end', "📋 SUJETO A:\n")
            # Recrear restricciones para mostrar
            for linea in lineas:
                partes = linea.split()
                coefs = partes[:num_vars]
                tipo_r = partes[num_vars]
                valor = partes[num_vars + 1]
                rest_str = " + ".join([f"{coefs[i]}x{i+1}" for i in range(num_vars)])
                self.txt_resultado_pl.insert('end', f"   {rest_str} {tipo_r} {valor}\n")
            
            self.txt_resultado_pl.insert('end', f"\n   xᵢ ≥ 0  ∀i")
            if tipo_vars == "enteras":
                self.txt_resultado_pl.insert('end', " (enteras)")
            elif tipo_vars == "binarias":
                self.txt_resultado_pl.insert('end', " (binarias: 0 o 1)")
            self.txt_resultado_pl.insert('end', "\n\n")
            
            # Mostrar proceso de solución
            self.txt_resultado_pl.insert('end', "=" * 70 + "\n")
            self.txt_resultado_pl.insert('end', "📊 PROCESO DE SOLUCIÓN\n")
            self.txt_resultado_pl.insert('end', "=" * 70 + "\n\n")
            
            self.txt_resultado_pl.insert('end', "🔹 MÉTODO UTILIZADO:\n")
            if tipo_vars == "continuas":
                self.txt_resultado_pl.insert('end', "   • Algoritmo: Método Simplex Revisado (HiGHS)\n")
                self.txt_resultado_pl.insert('end', "   • Tipo: Problema de programación lineal continua\n")
            else:
                self.txt_resultado_pl.insert('end', "   • Algoritmo: Branch & Bound con Simplex (HiGHS)\n")
                self.txt_resultado_pl.insert('end', f"   • Tipo: Problema de programación lineal {tipo_vars}\n")
            
            self.txt_resultado_pl.insert('end', f"\n🔹 FORMULACIÓN ESTÁNDAR:\n")
            self.txt_resultado_pl.insert('end', f"   • Variables: {num_vars}\n")
            self.txt_resultado_pl.insert('end', f"   • Restricciones de desigualdad: {len(A_ub) if A_ub else 0}\n")
            self.txt_resultado_pl.insert('end', f"   • Restricciones de igualdad: {len(A_eq) if A_eq else 0}\n")
            self.txt_resultado_pl.insert('end', f"   • Variables de holgura agregadas: {len(A_ub) if A_ub else 0}\n\n")
            
            if resultado.success:
                self.txt_resultado_pl.insert('end', "🔹 PROCESO SIMPLEX:\n")
                self.txt_resultado_pl.insert('end', f"   ✓ Iteraciones realizadas: {resultado.nit if hasattr(resultado, 'nit') else 'N/A'}\n")
                self.txt_resultado_pl.insert('end', f"   ✓ Estado: {resultado.message}\n")
                if tipo_vars in ["enteras", "binarias"]:
                    self.txt_resultado_pl.insert('end', "   ✓ Se aplicó ramificación y acotamiento (Branch & Bound)\n")
                self.txt_resultado_pl.insert('end', "   ✓ Solución óptima encontrada\n\n")
            
            if resultado.success:
                self.txt_resultado_pl.insert('end', "=" * 70 + "\n")
                self.txt_resultado_pl.insert('end', "✅ SOLUCIÓN ÓPTIMA ENCONTRADA\n")
                self.txt_resultado_pl.insert('end', "=" * 70 + "\n\n")
                
                # Valor óptimo
                valor_opt = -resultado.fun if tipo == "max" else resultado.fun
                self.txt_resultado_pl.insert('end', f"💰 VALOR ÓPTIMO: Z* = {valor_opt:.4f}\n\n")
                
                # Variables
                self.txt_resultado_pl.insert('end', "📊 VALORES DE LAS VARIABLES:\n")
                self.txt_resultado_pl.insert('end', "-" * 70 + "\n")
                for i, val in enumerate(resultado.x):
                    self.txt_resultado_pl.insert('end', f"   x{i+1} = {val:.4f}\n")
                
                # Análisis
                self.txt_resultado_pl.insert('end', "\n" + "=" * 70 + "\n")
                self.txt_resultado_pl.insert('end', "📈 ANÁLISIS\n")
                self.txt_resultado_pl.insert('end', "=" * 70 + "\n")
                self.txt_resultado_pl.insert('end', f"• Iteraciones: {resultado.nit if hasattr(resultado, 'nit') else 'N/A'}\n")
                self.txt_resultado_pl.insert('end', f"• Estado: {resultado.message}\n")
                
                # Variables básicas y no básicas
                self.txt_resultado_pl.insert('end', "\n🔍 VARIABLES EN LA SOLUCIÓN:\n")
                basicas = [i+1 for i, val in enumerate(resultado.x) if val > 0.0001]
                no_basicas = [i+1 for i, val in enumerate(resultado.x) if val <= 0.0001]
                
                if basicas:
                    self.txt_resultado_pl.insert('end', f"   Básicas (≠ 0): {', '.join([f'x{i}' for i in basicas])}\n")
                if no_basicas:
                    self.txt_resultado_pl.insert('end', f"   No básicas (= 0): {', '.join([f'x{i}' for i in no_basicas])}\n")
                
                # Visualizar
                self._visualizar_solucion_pl(resultado.x, c, tipo, tipo_vars)
                
            else:
                self.txt_resultado_pl.insert('end', "=" * 70 + "\n")
                self.txt_resultado_pl.insert('end', "❌ NO SE ENCONTRÓ SOLUCIÓN ÓPTIMA\n")
                self.txt_resultado_pl.insert('end', "=" * 70 + "\n\n")
                self.txt_resultado_pl.insert('end', f"Mensaje: {resultado.message}\n\n")
                self.txt_resultado_pl.insert('end', "Posibles causas:\n")
                self.txt_resultado_pl.insert('end', "• El problema no tiene solución factible\n")
                self.txt_resultado_pl.insert('end', "• El problema es no acotado\n")
                self.txt_resultado_pl.insert('end', "• Las restricciones son inconsistentes\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver: {str(e)}")
            self.txt_resultado_pl.insert('end', f"\n❌ ERROR: {str(e)}\n")
    
    def _visualizar_solucion_pl(self, x, c, tipo, tipo_vars):
        """Visualiza la solución del problema de PL"""
        try:
            fig = plt.figure(figsize=(12, 5))
            
            # Gráfico de barras con valores de variables
            ax1 = plt.subplot(1, 2, 1)
            variables = [f'x{i+1}' for i in range(len(x))]
            colores = ['#3498db' if val > 0.0001 else '#ecf0f1' for val in x]
            barras = ax1.bar(variables, x, color=colores, alpha=0.8, edgecolor='black')
            ax1.set_title('📊 Valores de las Variables', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Valor', fontsize=10)
            ax1.grid(axis='y', alpha=0.3)
            
            # Añadir valores
            for barra in barras:
                altura = barra.get_height()
                if altura > 0.0001:
                    ax1.text(barra.get_x() + barra.get_width()/2., altura,
                            f'{altura:.3f}',
                            ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            # Contribución a la función objetivo
            ax2 = plt.subplot(1, 2, 2)
            c_original = [-val for val in c] if tipo == "max" else c
            contribuciones = [x[i] * c_original[i] for i in range(len(x))]
            colores2 = ['#2ecc71' if cont > 0 else '#e74c3c' if cont < 0 else '#ecf0f1' 
                       for cont in contribuciones]
            barras2 = ax2.bar(variables, contribuciones, color=colores2, alpha=0.8, edgecolor='black')
            ax2.set_title('💰 Contribución a la Función Objetivo', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Contribución', fontsize=10)
            ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
            ax2.grid(axis='y', alpha=0.3)
            
            # Añadir valores
            for barra in barras2:
                altura = barra.get_height()
                if abs(altura) > 0.0001:
                    ax2.text(barra.get_x() + barra.get_width()/2., altura,
                            f'{altura:.3f}',
                            ha='center', va='bottom' if altura > 0 else 'top', 
                            fontsize=10, fontweight='bold')
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"No se pudo visualizar: {str(e)}")

def main():
    root = tk.Tk()
    app = AplicacionGrafos(root)
    root.mainloop()

if __name__ == "__main__":
    main()
