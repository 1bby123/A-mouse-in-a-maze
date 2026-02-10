# A-mouse-in-a-maze
**Github Repo for Robotics Assessment 1**
---
### Submission
I have provided both the VEX VR file as well as the Python code itself in a separate file. If you are unable to open the VEX file in the online IDE, you can just paste the provided code
into a new IDE session and it should run without issues.

Below is an unlisted youtube link to my commentary video.

[![Robotics Video](https://img.youtube.com/vi/--SRiHePCRU/0.jpg)](https://www.youtube.com/watch?v=--SRiHePCRU)

---

Here is a description of the tasks I attempted in this assignment:


### 1. Move along the corridors without straying past the walls.
   
   The code contains a check to ensure the robot is always within the bounds of the maze. This is done by converting the maze into an 8x8 grid and checking if the index of the next square is within that converted maze. The
   robot uses the front eye as a sensor for walls, rather than the bumper. This bypasses the fake wall trap that is present in one of the mazes. The robot checks for walls within a 250mm range, as that is the distance of each
   cell. It also records walls it has detected in a dictionary, which is used by the print maze function to print the walls to the console.


### 2. Find its way out of the maze.
   
   The robot stores a path variable containing the list of coordinates from the start square to the target square. It then follows those coordinates with a green pen, marking the path out of the maze.


### 3. Escape the maze by the fastest possible route.
   
   As the robot explores the maze, it records all the squares it has visited. Once it reaches the target square, it stops appending coordinates to the path variable, as that marks an unoptimized path
   from start to finish. The robot however continues to map the maze. The code takes this path and optimizes it by pruning the dead ends from the path using a stack.
   The robot iterates through the path list, adding it to both a stack and a set. if any given coordinates are in the set, this means they are also in the stack, which then means
   that coordinates in between those two are essentially a loop. The robot will remove all coordinates between the first instance and second instance of the same coordinate and repeat this process for the entire path.
   The output will be a path from start to finish with all dead ends removed. This approach is possible here because in dynamic wall maze, it is given that there is always just one path out of the maze. A set is used to ensure $O(1)$
   complexity for coordinate lookup. Rather than iterating through the whole stack every time, the robot can just check the set.


### 4. Find the quickest route out of the maze (20%)
   
   This is an extension of requirement number 3. The unoptimized path is stored once the robot reaches the target square. Once the robot returns home, a function is called that optimizes the path by pruning dead ends.
   
### 5. Map the maze (20%)
   
   Depth-First-Search is used to map the entire maze. The robot begins at the starting square, at this stage every cell is marked as univisted. The robot checks all four sides for unvisited squares and visits the first one it sees.
   That square then gets marked as visited. If the robot reaches a dead end, it will then backtrack to the previous square. This becomes the new starting square, meaning the robot will perform the checks for a new unvisited square again. It
   will keep backtracking like this until it reaches a cell in which there is an unvisited path. This process repeats until all cells have been visited. I considered a recursive approach, however I decided to stick with the stack-based approach
   to avoid any stack overflow related issues, since the robot may have limited memory. The recursive approach would have been more elegant to program however each stack frame would be heavier, because it must store the local variables every time.
   By using a stack, I only need to store row and column inside a tuple for every frame, making it much lighter.


### 6. Return to home (20%)
    
   The beauty of Depth-First Search and backtracking, is that when the robot reaches the final unvisited square, it will backtrack all the way to the start. This happens on it's own as a core feature of the algorithm. This is essentially the
   reason I opted to go for DFS and not the Flood Fill algorithm, which is the standard in competitions such as Micromouse.


### 7. Print the Maze
    
   After walking the optimal path and reaching the end, the program outputs an ASCII representation of the maze to the console, marking the walls, start square and end square. This fulfills the requirement of a stored, viewable solution.

---

All required tasks have been implemented in this submission.

I confirm that no AI tools were used in the preparation or completion of this assessment. This submission
aligns with AITS 1 of the Artificial Intelligence Transparency Scale (AITS).

---

Below are some references I used that helped me conduct research and draw insipration for my solution:

  * **Veritasium (2023). The Fastest Maze-Solving Competition On Earth. YouTube. Available at: https://www.youtube.com/watch?v=ZMQbHMgK2rw [Accessed 16 Sep. 2023].**
   * **www.youtube.com. (n.d.). Search A Maze For Any Path - Depth First Search Fundamentals (Similar To ‘The Maze’ on Leetcode). [online] Available at: https://www.youtube.com/watch?v=W9F8fDQj7Ok [Accessed 31 Dec. 2022].**
   * **Michael Backus (2015). Dynamic Programming / Flood Fill Algorithm. [online] YouTube. Available at: https://www.youtube.com/watch?v=Zwh-QNlsurI [Accessed 7 Nov. 2025].**

‌

‌
‌
