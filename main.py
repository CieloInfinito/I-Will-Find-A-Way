import tkinter as tk
from tkinter import messagebox
import heapq
import numpy as np
import time
from PIL import Image, ImageTk
import os
import sys

# Configuración de colores y pesos
TERRAIN = {
    "grass": {"color": "green", "weight": 1},
    "water": {"color": "blue", "weight": 5},
    "wall": {"color": "black", "weight": float('inf')},
    "air": {"color": "white", "weight": 0},
    "path": {"color": "orange", "weight": 0},
    "start": {"color": "yellow", "weight": 0},
    "goal": {"color": "red", "weight": 0}
}

# Configuración de idiomas
LANGUAGES = {
    "es": {
        "title": "Encontraré un camino",
        "find_path": "Encontrar camino",
        "clear_selection": "Borrar selección",
        "fill_grid": "Llenar la cuadrícula con hierba",
        "allow_diagonal": "Permitir diagonales",
        "error_title": "Error",
        "error_message": "Debe seleccionar un punto de inicio y meta",
        "no_path": "No se encontró un camino",
        "terrain": {"grass": "Hierba", "water": "Agua", "wall": "Muro", "air": "Aire"}
    },
    "en": {
        "title": "I Will Find a Way",
        "find_path": "Find Path",
        "clear_selection": "Clear Selection",
        "fill_grid": "Fill Grid with Grass",
        "allow_diagonal": "Allow Diagonals",
        "error_title": "Error",
        "error_message": "You must select a start and goal point",
        "no_path": "No path found",
        "terrain": {"grass": "Grass", "water": "Water", "wall": "Wall", "air": "Air"}
    }
}

GRID_SIZE = 10   # Tamaño de la cuadrícula
CELL_SIZE = 50   # Tamaño de cada celda en píxeles
DELAY = 0.1      # Retraso en segundos para visualizar la búsqueda

def heuristic_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic_euclidean(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def get_path(relative_path):
    """ Devuelve la ruta correcta para archivos en el ejecutable """
    if getattr(sys, 'frozen', False):  # Si está congelado en un .exe
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class IWillFindAWayApp:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap(get_path("icon.ico"))
        self.root.title("I Will Find a Way")
        self.grid = [[TERRAIN["grass"]["weight"] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.start = None
        self.goal = None
        self.algorithm = "A*"
        self.heuristic_type = "Manhattan"  # Seleccionada inicialmente
        self.allow_diagonal = tk.BooleanVar(value=False)
        self.selected_terrain = "grass"
        self.language = "en"  # Idioma predeterminado
        self.canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_grid()

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        self.algorithm_menu = tk.OptionMenu(control_frame, tk.StringVar(value=self.algorithm), "A*", "Dijkstra", command=self.set_algorithm)
        self.algorithm_menu.pack(side=tk.LEFT, padx=5)

        self.heuristic_menu = tk.OptionMenu(control_frame, tk.StringVar(value=self.heuristic_type), "Manhattan", "Euclidiana", command=self.set_heuristic)
        self.heuristic_menu.pack(side=tk.LEFT, padx=5)

        self.diagonal_check = tk.Checkbutton(control_frame, text="Allow Diagonals", variable=self.allow_diagonal, command=self.toggle_diagonal)
        self.diagonal_check.pack(side=tk.LEFT, padx=5)

        self.terrain_var = tk.StringVar()
        self.terrain_var.set(LANGUAGES[self.language]["terrain"][self.selected_terrain])
        self.terrain_menu = tk.OptionMenu(control_frame, self.terrain_var, *self.get_terrain_labels(), command=self.set_terrain)
        self.terrain_menu.pack(side=tk.LEFT, padx=5)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.find_button = tk.Button(button_frame, text="Find Path", command=self.find_path)
        self.find_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(button_frame, text="Clear Selection", command=self.clear_selection)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.fill_grass_button = tk.Button(button_frame, text="Fill Grid with Grass", command=self.fill_with_grass)
        self.fill_grass_button.pack(side=tk.LEFT, padx=5)

        self.language_frame = tk.Frame(root)
        self.language_frame.pack(pady=10)

        flag_es_path = get_path("flag_es.png")
        flag_en_path = get_path("flag_en.png")
        self.flag_es = ImageTk.PhotoImage(Image.open(flag_es_path).resize((50, 30)))
        self.flag_en = ImageTk.PhotoImage(Image.open(flag_en_path).resize((50, 30)))

        self.es_button = tk.Button(self.language_frame, image=self.flag_es, command=lambda: self.change_language("es"))
        self.es_button.pack(side=tk.LEFT, padx=5)
        
        self.en_button = tk.Button(self.language_frame, image=self.flag_en, command=lambda: self.change_language("en"))
        self.en_button.pack(side=tk.LEFT, padx=5)

    def update_language(self):
        self.root.title(LANGUAGES[self.language]["title"])

    def update_terrain_menu(self):
        """ Actualiza el menú desplegable de terrenos al cambiar el idioma """
        self.terrain_menu['menu'].delete(0, 'end')  # Borra opciones actuales
        for label in self.get_terrain_labels():
            self.terrain_menu['menu'].add_command(label=label, command=lambda value=label: self.set_terrain(value))
        # Actualiza la selección actual traducida
        self.terrain_var.set(LANGUAGES[self.language]["terrain"][self.selected_terrain])

    def update_texts(self):
        self.find_button.config(text=LANGUAGES[self.language]["find_path"])
        self.clear_button.config(text=LANGUAGES[self.language]["clear_selection"])
        self.fill_grass_button.config(text=LANGUAGES[self.language]["fill_grid"])
        self.diagonal_check.config(text=LANGUAGES[self.language]["allow_diagonal"])
        self.update_terrain_menu()

    def change_language(self, lang):
        self.language = lang
        self.update_language()
        self.update_texts()
    
    def set_terrain(self, value):
        for key, label in LANGUAGES[self.language]["terrain"].items():
            if label == value:
                self.selected_terrain = key
                break
    
    def get_terrain_labels(self):
        return list(LANGUAGES[self.language]["terrain"].values())
    
    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                color = TERRAIN["grass"]["color"]
                if (i, j) == self.start:
                    color = TERRAIN["start"]["color"]
                elif (i, j) == self.goal:
                    color = TERRAIN["goal"]["color"]
                elif self.grid[i][j] == TERRAIN["water"]["weight"]:
                    color = TERRAIN["water"]["color"]
                elif self.grid[i][j] == TERRAIN["wall"]["weight"]:
                    color = TERRAIN["wall"]["color"]
                elif self.grid[i][j] == TERRAIN["air"]["weight"]:
                    color = TERRAIN["air"]["color"]
                self.canvas.create_rectangle(j * CELL_SIZE, i * CELL_SIZE,
                                             (j+1) * CELL_SIZE, (i+1) * CELL_SIZE,
                                             fill=color, outline="white")
    
    def draw_cell(self, cell, color):
        i, j = cell
        self.canvas.create_rectangle(j * CELL_SIZE, i * CELL_SIZE,
                                     (j+1) * CELL_SIZE, (i+1) * CELL_SIZE,
                                     fill=color, outline="white")

    def on_click(self, event):
        row, col = event.y // CELL_SIZE, event.x // CELL_SIZE
        if (row, col) == self.start:
            self.start = None
        elif (row, col) == self.goal:
            self.goal = None
        elif not self.start:
            self.start = (row, col)
        elif not self.goal:
            self.goal = (row, col)
        elif (row, col) != self.start and (row, col) != self.goal:
            self.grid[row][col] = TERRAIN[self.selected_terrain]["weight"]
        self.draw_grid()

    def set_algorithm(self, value):
        self.algorithm = value

    def set_heuristic(self, value):
        self.heuristic_type = value
        self.draw_grid()  

    def toggle_diagonal(self):
        # Ahora solo actualizamos la visualización sin modificar la heurística
        self.draw_grid()  

    def clear_selection(self):
        self.start = None
        self.goal = None
        self.draw_grid()

    def fill_with_grass(self):
        self.grid = [[TERRAIN["grass"]["weight"] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.draw_grid()

    def find_path(self):
        if not self.start or not self.goal:
            messagebox.showerror(LANGUAGES[self.language]["error_title"], LANGUAGES[self.language]["error_message"])
            return

        self.draw_grid()
        path = self.calculate_path(self.grid, self.start, self.goal, self.algorithm)
        if path:
            for row, col in path[:-1]:
                self.canvas.create_rectangle(col * CELL_SIZE, row * CELL_SIZE,
                                             (col+1) * CELL_SIZE, (row+1) * CELL_SIZE,
                                             fill=TERRAIN["path"]["color"], outline="white")
            self.canvas.update()
        else:
            messagebox.showerror("Error", "No se encontró un camino")

    def calculate_path(self, grid, start, goal, algorithm):
        rows, cols = len(grid), len(grid[0])
        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        # Selección de la función heurística según el menú
        if self.heuristic_type == "Manhattan":
            heuristic = heuristic_manhattan
        else:
            heuristic = heuristic_euclidean
        
        # Selección de direcciones basada en el checkbox (diagonales permitidas o no)
        if self.allow_diagonal.get():
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Para Dijkstra se ignora la heurística (equivalente a h(n)=0)
        if algorithm == "Dijkstra":
            effective_heuristic = lambda a, b: 0
        else:
            effective_heuristic = heuristic

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == goal:
                break

            if current != start and current != goal:
                self.draw_cell(current, "light gray")
                self.canvas.update()
                time.sleep(DELAY)

            x, y = current
            for dx, dy in directions:
                neighbor = (x + dx, y + dy)
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                    new_cost = cost_so_far[current] + grid[neighbor[0]][neighbor[1]]
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        priority = new_cost + effective_heuristic(neighbor, goal)
                        heapq.heappush(frontier, (priority, neighbor))
                        came_from[neighbor] = current
                        if neighbor != start and neighbor != goal:
                            self.draw_cell(neighbor, "cyan")
            self.canvas.update()
            time.sleep(DELAY)

        path = []
        current = goal
        while current and current != start:
            path.append(current)
            current = came_from.get(current)
        return path[::-1] if current == start else []

if __name__ == "__main__":
    root = tk.Tk()
    app = IWillFindAWayApp(root)
    root.mainloop()