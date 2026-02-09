# A-mouse-in-a-maze
Github Repo for Robotics Assessment 1

Here is a description of the tasks I attempted in this assignment:


1. Move along the corridors without straying past the walls.
   
   The code contains a check to ensure the robot is always within the bounds of the maze. This is done by converting the maze into an 8x8 grid and checking if the index of the next square is within that converted maze. The
   robot uses the front eye as a sensor for walls, rather than the bumper. This bypasses the fake wall trap that is present in one of the mazes. The robot checks for walls within a 250mm range, as that is the distance of each
   cell. It also records walls it has detected in a dictionary, which is used by the print maze function to print the walls to the console.


3. Find its way out of the maze.
   
   The robot stores a path variable containing the list of coordinates from the start square to the target square. It then follows those coordinates with a green pen, marking the path out of the maze.


4. Escape the maze by the fastest possible route.
   
   As the robot explores the maze, it records all the squares it has visited. Once it reaches the target square, it stops appending coordinates to the path variable, as that marks an unoptimized path
   from start to finish. The robot however continues to map the maze. The code takes this path and optimizes it by pruning the dead ends from the path using a stack.
   The robot iterates through the path list, adding it to both a stack and a set. if any given coordinates are in the set, this means they are also in the stack, which then means
   that coordinates in between those two are essentially a loop. The robot will remove all coordinates between the first instance and second instance of the same coordinate and repeat this process for the entire path.
   The output will be a path from start to finish with all dead ends removed. This approach is possible here because in dynamic wall maze, it is given that there is always just one path out of the maze. A set is used to ensure O(1)
   complexity for coordinate lookup. Rather than iterating through the whole stack every time, the robot can just check the set.


5. Find the quickest route out of the maze (20%)
   
   This is an extension of requirement number 3. The unoptimized path is stored once the robot reaches the target square. Once the robot returns home, a function is called that optimizes the path by pruning dead ends.
   
6. Map the maze (20%)
   
   Depth-First-Search is used to map the entire maze. The robot begins at the starting square, at this stage every cell is marked as univisted. The robot checks all four sides for unvisited squares and visits the first one it sees.
   That square then gets marked as visited. If the robot reaches a dead end, it will then backtrack to the previous square. This becomes the new starting square, meaning the robot will perform the checks for a new unvisited square again. It
   will keep backtracking like this until it reaches a cell in which there is an unvisited path. This process repeats until all cells have been visited.


7. Return to home (20%)
    
   The beauty of Depth-First Search and backtracking, is that when the robot reaches the final unvisited square, it will backtrack all the way to the start. This happens on it's own as a core feature of the algorithm. This is essentially the
   reason I opted to go for DFS and not the Flood Fill algorithm, which is the standard in competitions such as Micromouse.


8. Print the Maze
    
   After walking the optimal path and reaching the end, the program outputs an ASCII representation of the maze to the console, marking the walls, start square and end square. This fulfills the requirement of a stored, viewable solution.


All required tasks have been implemented in this submission.

