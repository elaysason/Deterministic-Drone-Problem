# Deterministic-Drone-Problem
In this problem we are the head of a delivery agency and try to deliver the packages in the shortest time possible. Our clients are operating in a deterministic manner.

1. [General](#General)
    - [Program Structure](https://github.com/elaysason/Deterministic-Drone-Problem/blob/main/README.md#program-structure)  
2. [Installation](#Installation)
4. [Footnote](#footnote)

## General
The environment is a rectangular grid with passable and non passable points for drone passage.Moreover, there are packages lying in different locations
around the grid. The packages can be picked up by drones and delivered to clients.Clients can move on a pre-determined and known path, and each client has a list of required
packages. The goal is the deliver to most packages possible.
### Program Structure

1. ex1.py - implements the specific problem, the soultion would be applied here.
2. check.py - the file that includes some wrappers and inputs
3. search.py - a file that has implementations of different search algorithms (including
GBFS, A* and many more)
4. utils.py - the file that contains some utility functions.

### Installation
1.Open the terminal

2.Clone the project by:
```
    $ git clone https://github.com/elaysason/Deterministic-Drone-Problem.git
```
3.Run the check.py file by:
```
    $ python3 check.py
```
