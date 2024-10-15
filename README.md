This readme is AI generated.

Minesweeper Bot and Trainer

This project is a Minesweeper game implemented in Python, featuring a built-in bot and training tools to enhance your Minesweeper skills. 
The game allows you to play interactively, visualize safe moves, and calculate the probabilities of each cell being a mine. With an advanced automatic mode, the bot can play the game for you, providing insights into optimal strategies. Don't make the window to large or it will take a very long time to compute. The code is total spaghetti as this is an old project of mine.

Features:

Interactive Gameplay: Play Minesweeper with customizable grid sizes and mine counts.

Iterate Function: An "Iterate" button that reveals safe squares and displays the probability of each unknown cell being a mine.

Advanced Bot: A fully automatic mode that is considered one of the best publicly available Minesweeper bots.

Training Aid: Helps improve your decision-making by analyzing the board and suggesting optimal moves.

Customizable Difficulty: Adjust the grid size and number of mines to match your preferred difficulty level.

Flagging System: Right-click to flag or unflag cells you suspect contain mines.

Visual Indicators: Cells are color-coded based on their status and mine probability.

Getting Started:
Prerequisites
Python 3.x: Ensure you have Python 3 installed on your system.
Required Modules:
tkinter: Standard GUI library for Python (usually included).
colour: For color handling (may need to be installed separately).
Installation
Download the Script

Download the minesweeper.py file to your local machine.

Install Required Modules

If you don't have the colour module installed, you can install it using pip:
pip install colour

Running the Game
Navigate to the directory containing minesweeper.py and run:

python minesweeper.py

A window titled "Minesweeper" should appear, and you're ready to play!

How to Play

Controls

Left-Click on a Cell: Reveal what's underneath the cell.

Right-Click on a Cell: Flag or unflag a cell you suspect contains a mine.

Iterate Button: Click to have the bot analyze the board, suggesting safe moves or displaying mine probabilities.

Settings Button: Adjust the number of rows, columns, and mines to customize your game.

Restart Button: Start a new game with the current settings.

Simulate Game Button: Let the bot play the game automatically from start to finish.

Using the Bot

Iterate Function: When unsure of your next move, click the Iterate button. The bot will:

Highlight light green cells that are safe to click.

Highlight pink cells that are definitely mines.

Display the probability (as a percentage) of each unknown cell being a mine.

Automatic Mode: Click the Simulate Game button to have the bot play a bunch of games automatically, you can see how it does in print output only.

Strategic Guessing: If there are no safe moves, use the probabilities to make an informed guess.

Settings

Most settings ate in the actual code itself unfortunately, their description are in the code, sorry it is not obvious.

Known Issues

Alive Chance Counter Inaccuracy: The "Alive Chance" displayed after each game does not accurately reflect the true survival probability.

Iterate Function After Game Over: You can continue to click the Iterate button even after the game has ended, which may cause unexpected behavior.

Improvements, please contribute to the codebase. I likely will not.

Code Refactoring: Restructure the codebase to utilize classes and functions, potentially splitting it into multiple files for better organization.

Performance Optimization: Enhance computation time for probability calculations, possibly by implementing graph-based algorithms.

Sandbox Mode: Introduce a mode where you can place mines manually and modify the map to simulate different scenarios.

Probability Verification: Implement tests to verify the correctness of the calculated probabilities.

Enhanced User Interface: Develop a comprehensive settings page and a game launch screen for improved user experience.

Improved Guessing Strategy: Refine the bot's logic to avoid clicking on cells with the lowest mine probability if revealing them provides no new information.

Contributing

Contributions are welcome! If you'd like to improve the game, fix bugs, or add new features:

Fork the repository.

Create a new branch for your feature or bug fix.

Commit your changes with clear messages.

Submit a pull request for review.

Please ensure your code adheres to the project's coding standards and is well-documented. LOL, chatgpt wrote that the coding standards are basically non existant.

License

I guess this project is licensed under the MIT License.

Acknowledgments

Original Author: Russell Gokemeijer, Russellgoke@gmail.com


Troubleshooting, first ensure that all dependencies are installed:

Tkinter: Typically included with Python installations. If not, install via your system's package manager.

Colour Module: Install using:

pip install colour

Game Window Not Appearing: Verify that tkinter is installed and properly configured.

Module Not Found Error for colour: Install the colour module using pip.

Unexpected Behavior: If the game behaves unexpectedly after changes, consider restarting the game or resetting to default settings.

Recursion Limit Reached: For larger grids, you may encounter a recursion limit error. Increase the recursion limit by adding sys.setrecursionlimit(1000) at the beginning of the script.

By following this guide, you should be able to run and enjoy the Minesweeper bot and trainer. Whether you're looking to improve your skills or simply enjoy a game of Minesweeper, this project offers a rich set of features to enhance your experience.
