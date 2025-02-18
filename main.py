import tkinter as tk
from tkinter import messagebox
import heapq
import numpy as np

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

GRID_SIZE = 10  # Tamaño de la cuadrícula
CELL_SIZE = 50  # Tamaño de cada celda en píxeles

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("I Will Find a Way")
        self.grid = [[TERRAIN["grass"]["weight"] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.start = None
        self.goal = None
        self.algorithm = "A*"
        self.selected_terrain = "grass"
        
        self.canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.draw_grid()
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.algorithm_menu = tk.OptionMenu(button_frame, tk.StringVar(value=self.algorithm), "A*", "Dijkstra", command=self.set_algorithm)
        self.algorithm_menu.pack(side=tk.LEFT, padx=5)
        
        self.terrain_menu = tk.OptionMenu(button_frame, tk.StringVar(value=self.selected_terrain), "grass", "water", "wall", "air", command=self.set_terrain)
        self.terrain_menu.pack(side=tk.LEFT, padx=5)
        
        self.find_button = tk.Button(button_frame, text="Find Path", command=self.find_path)
        self.find_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tk.Button(button_frame, text="Clear Selection", command=self.clear_selection)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.fill_grass_button = tk.Button(button_frame, text="Fill Grid with Grass", command=self.fill_with_grass)
        self.fill_grass_button.pack(side=tk.LEFT, padx=5)
        
    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                color = "green"
                if (i, j) == self.start:
                    color = "yellow"
                elif (i, j) == self.goal:
                    color = "red"
                elif self.grid[i][j] == TERRAIN["water"]["weight"]:
                    color = "blue"
                elif self.grid[i][j] == TERRAIN["wall"]["weight"]:
                    color = "black"
                elif self.grid[i][j] == TERRAIN["air"]["weight"]:
                    color = "white"
                self.canvas.create_rectangle(j * CELL_SIZE, i * CELL_SIZE, (j+1) * CELL_SIZE, (i+1) * CELL_SIZE, fill=color, outline="white")
    
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
    
    def set_terrain(self, value):
        self.selected_terrain = value
    
    def clear_selection(self):
        self.start = None
        self.goal = None
        self.draw_grid()
    
    def fill_with_grass(self):
        self.grid = [[TERRAIN["grass"]["weight"] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.draw_grid()
    
    def find_path(self):
        if not self.start or not self.goal:
            messagebox.showerror("Error", "Debe seleccionar un punto de inicio y meta")
            return
        
        path = self.calculate_path(self.grid, self.start, self.goal, self.algorithm)
        if path:
            for row, col in path:
                self.canvas.create_rectangle(col * CELL_SIZE, row * CELL_SIZE, (col+1) * CELL_SIZE, (row+1) * CELL_SIZE, fill="orange", outline="white")
        else:
            messagebox.showerror("Error", "No se encontró un camino")
    
    def calculate_path(self, grid, start, goal, algorithm):
        rows, cols = len(grid), len(grid[0])
        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}
        
        while frontier:
            current_priority, current = heapq.heappop(frontier)
            
            if current == goal:
                break
            
            x, y = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                    new_cost = cost_so_far[current] + grid[neighbor[0]][neighbor[1]]
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        priority = new_cost + (heuristic(neighbor, goal) if algorithm == "A*" else 0)
                        heapq.heappush(frontier, (priority, neighbor))
                        came_from[neighbor] = current
        
        # Reconstrucción del camino
        path = []
        current = goal
        while current and current != start:
            path.append(current)
            current = came_from.get(current)
        if current == start:
            path.reverse()
            return path
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()
