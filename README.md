# Electric Vehicle Charger Placement

Objective: 
- Minimize Costs

Constraints:
- Minimize distance between nearby chargers (nearby is flexible)
- One charger per zone (number per zone is flexible)

Inputs:
- Existing charger information: name / lat / long
- Build site information: zone / sector / lat / long

Outputs: Map of charger network
- Yellow: existing chargers
- Red: selected build sites for new chargers
- Blue: non-selected build sites for new chargers

Additional future variations (to be implemented):

- Objective: Minimize travel time between nearby chargers
- Constraint: Prefer high traffic locations

{ Final Small Scale Program notes:
- uses functions from visualization.py & utilities.py to
work with objectives and constraints of the project
- uses D-Wave's LeapHybridSolver as solver for the program
- returned output from solver stored in soln.txt file
- soln_.txt is plotted as the final visual output -> soln_map.png }

![soln](soln_map.png)
