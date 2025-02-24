# I Will Find a Way

A Python graphical application to visualize and compare the **A\*** and **Dijkstra** pathfinding algorithms in real time. This tool lets you experiment with different heuristic functions and movement configurations (with or without diagonals), making it a valuable resource for learning and analyzing these algorithms.

---

## Features

- **Algorithm Comparison:**  
  - **A\***: Uses a heuristic function to guide the search toward the goal, reducing unnecessary exploration in large graphs.
  - **Dijkstra:** Considers only the accumulated cost, expanding nodes uniformly in all directions.

- **Customizable Configuration:**  
  - Select the heuristic function: Manhattan or Euclidean.
  - Control diagonal movement exclusively via a checkbox.
  - Interactively edit the terrain by modifying cells to create obstacles, water, air, etc.
  - Set start and goal points directly on the grid with mouse clicks.

- **Real-Time Visualization:**  
  - **Expanded Nodes:** Displayed in light gray.
  - **Nodes Added to the Frontier:** Highlighted in cyan.
  - **Final Path:** Shown in orange.

---

## Installation and Requirements

### Requirements

- Python 3.x
- Libraries:
  - Tkinter (typically included with Python)
  - NumPy

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/i-will-find-a-way.git
   ```
2. Navigate to the project directory:
   ```bash
   cd i-will-find-a-way
   ```
3. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```
4. Install NumPy (if not already installed):
   ```bash
   pip install numpy
   ```

---

## Usage

1. Run the main script:
   ```bash
   python pathfinding_app.py
   ```
2. Interact with the interface:
   - **Set Start and Goal Points:** Click on the grid to designate these points.
   - **Edit the Terrain:** Choose the terrain type (grass, water, wall, air) from the menu and click on the grid cells to modify them.
   - **Configure the Algorithm:** Select between **A\*** and **Dijkstra** using the dropdown menu.
   - **Choose the Heuristic:** Select between **Manhattan** and **Euclidean**.  
     _Note:_ The heuristic only affects the cost estimation; the "Allow Diagonals" option exclusively controls the movement directions.
   - **Visualize the Search:** Click the "Find Path" button to initiate the real-time visualization of the search process.
   - **Other Options:**  
     - "Clear Selection" resets the start and goal points.
     - "Fill Grid with Grass" fills the grid with grass terrain.

---

## Project Structure

- **pathfinding_app.py:**  
  The main application code, which implements the graphical interface, search algorithm logic, and real-time visualization.

- **README.md:**  
  Documentation and usage guide for the project.

---

## Contributing

Contributions are welcome! If you'd like to suggest improvements, add features, or fix bugs, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

---

## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Notes and Suggestions

- **Visualization Optimization:**  
  Adjust the `DELAY` parameter to modify the speed of updates during the search visualization.

- **Future Extensions:**  
  - Add performance statistics (e.g., the number of nodes expanded, total cost).
  - Implement additional search algorithms or optimization techniques.
  - Enhance the graphical interface for a more intuitive user experience.

---

_Enjoy exploring and comparing pathfinding with **I Will Find a Way**!_
