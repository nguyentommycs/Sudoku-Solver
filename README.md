# Sudoku-Solver

Fill in the grid by clicking on the square and pressing a number on your keyboard. Use **delete** to erase a square.

Press **Space** to solve the puzzle while showing the process. The display will take a bit of time but it's cool to watch!

Press **Enter** to solve the puzzle instantly. There won't be any animation here, but this drastically reduces the amount of time. 

If you enter a puzzle that doesn't have a solution, the final grid will simply return to the initial state.



### Installation


1. Clone the repo
   ```sh
   git clone https://github.com/nguyentommycs/Sudoku-Solver.git
   ```
2. Create a virtual environment
   ```sh
   python -m venv env
   ```
3. Activate the virtual environment

   For Windows:
   ```sh
   env\Scripts\activate.bat
   ```
   For Linux:
   ```sh
   source env/bin/activate
   ```
4. Install pygame
   ```sh
   pip install pygame
   ```
5. Run the solver
   ```js
   python Game.py
   ```


