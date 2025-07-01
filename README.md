# 🤖 RescueBot-MST-AStar

An intelligent and interactive grid-based pathfinding simulator where a **rescue robot** navigates around obstacles to reach all targets using **A* search** enhanced with a **Minimum Spanning Tree (MST)** heuristic.

Developed using **Python and Pygame**, this project visually demonstrates informed search techniques and is perfect for students, educators, and AI enthusiasts.

---

## 📌 What This Project Does

- Simulates a 5x5 grid with customizable robot, targets, and obstacles.
- Robot finds shortest path visiting **all targets**, avoiding obstacles.
- Uses **A* Search Algorithm** with an **MST-based heuristic**.
- Animates robot movement in real-time.
- Console logs each robot step.

---

## 🧠 Features

✅ Visual 5x5 interactive grid  
✅ Place one robot, multiple targets, and obstacles  
✅ Animated pathfinding with step-by-step logs  
✅ A* with MST heuristic for multi-goal search  
✅ Easy-to-use interface with keyboard and mouse  

---

## 🎮 Controls

| Key        | Action                            |
|------------|------------------------------------|
| `R`        | Place the **Robot** (only one)     |
| `T`        | Place a **Target** (multiple allowed) |
| `O`        | Place an **Obstacle**              |
| `C`        | Clear a cell (set to empty)        |
| `Enter`    | Start the robot simulation         |
| Mouse      | Select grid cell based on mode     |

> ⚠️ You **must** place 1 robot and **at least** 1 target before pressing Enter.

---

## 📦 Requirements

- Python 3.x  
- Pygame (`pip install pygame`)

---

## 🚀 How to Run

1. Install dependencies:
```bash
pip install pygame

FAQ & Common Questions
Q: Can I place more than one robot?
🅰️ No. Only one robot is allowed. Placing a new one removes the previous.

Q: What if I forget to place a robot or target?
🅰️ The program will show an error and exit. You must place 1 robot and 1+ targets.

Q: Can I make the grid bigger?
🅰️ Yes, but you'll need to change GRID_SIZE and adjust the code layout accordingly.

Q: How is this different from normal A*?
🅰️ It uses a MST-based heuristic, making it smarter for visiting multiple targets.

