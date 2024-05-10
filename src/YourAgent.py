# Custom imports to assist in interfacing with the simulator
from src.DriveInterface import DriveInterface
from src.DriveState import DriveState
from src.Constants import DriveMove, SensorData
from collections import deque


class YourAgent(DriveInterface):

    def __init__(self, game_id: int, is_advanced_mode: bool):
        """
        Constructor for YourAgent

        Arguments:
        game_id -- a unique value passed to the player drive, you do not have to do anything with it, but will have access.
        is_advanced_mode -- boolean to indicate if 
        """
        self.game_id  = game_id
        self.need_to_find_target_pod = is_advanced_mode
        

    # This is the main function the simulator will call each turn 
    def get_next_move(self, sensor_data: dict) -> DriveMove:
        """
        Main function for YourAgent. The simulator will call this function each loop of the simulation to see what your agent's
        next move would be. You will have access to data about the field, your robot's location, other robots' locations and more
        in the sensor_data dict arguemnt.

        Arguments:
        sensor_data -- a dict with state information about other objects in the game. The structure of sensor_data is shown below:
            sensor_data = {
                SensorData.FIELD_BOUNDARIES: [[-1, -1], [-1, 0], ...],  
                SensorData.DRIVE_LOCATIONS: [[x1, y1], [x2, y2], ...], 
                SensorData.POD_LOCATIONS: [[x1, y1], [x2, y2], ...],
                SensorData.PLAYER_LOCATION: [x, y],
                SensorData.GOAL_LOCATION: [x, y], (Advanced Mode)
                SensorData.TARGET_POD_LOCATION: [x, y], # Only used for Advanced mode
                SensorData.DRIVE_LIFTED_POD_PAIRS: [[drive_id_1, pod_id_1], [drive_id_2, pod_id_2], ...] (Only used in Advanced mode for seeing which pods are currently lifted by drives)

            }
            

        Returns:
        DriveMove - return value must be one of the enum values in the DriveMove class:
            DriveMove.NONE – Do nothing
            DriveMove.UP – Move 1 tile up (positive y direction)
            DriveMove.DOWN – Move 1 tile down (negative y direction)
            DriveMove.RIGHT – Move 1 tile right (positive x direction)
            DriveMove.LEFT – Move 1 tile left (negative x direction)
            
            (Advanced mode only)
            DriveMove.LIFT_POD – If a pod is in the same tile, pick it up. The pod will now move with the drive until it is dropped
            DriveMove.DROP_POD – If a pod is in the same tile, drop it. The pod will now stay in this position until it is picked up

        """
        raise Exception('get_next_move in YourAgent not implemented')
    
    def get_next_move(self, sensor_data: dict) -> DriveMove:
        # Extract relevant information from sensor_data
        field_boundaries = sensor_data.get(SensorData.FIELD_BOUNDARIES)
        drive_locations = sensor_data.get(SensorData.DRIVE_LOCATIONS)
        pod_locations = sensor_data.get(SensorData.POD_LOCATIONS)
        player_location = sensor_data.get(SensorData.PLAYER_LOCATION)
        goal_location = sensor_data.get(SensorData.GOAL_LOCATION)
        
        # Implement your logic to decide the next move
        
        # Example: Move towards the goal if no obstacles are in the way
        if player_location[0] < goal_location[0]:
            return DriveMove.RIGHT
        elif player_location[0] > goal_location[0]:
            return DriveMove.LEFT
        elif player_location[1] < goal_location[1]:
            return DriveMove.UP
        elif player_location[1] > goal_location[1]:
            return DriveMove.DOWN
        else:
            return DriveMove.NONE
        
    def bfs_solve_path_to_goal(self, sensor_data: dict, goal: list[int]):
        # Breadth-First Search solver to find a path between SensorData.PLAYER_LOCATION and the goal argument
        # Stores solved path as a list of DriveState(s) in the self.path variable
        start_state = sensor_data[SensorData.PLAYER_LOCATION]

        queue = deque([DriveState(x=start_state[0], y=start_state[1])])
        visited_states = set()
        parent_map = {}  # To track the parent state for each state

        while queue:
            curr_state = queue.popleft()

            if curr_state.x == goal[0] and curr_state.y == goal[1]:
                # Reconstruct the path from the parent_map
                self.path = [curr_state]
                parent = parent_map.get(curr_state)
                while parent:
                    self.path.insert(0, parent)
                    parent = parent_map.get(parent)
                return

            visited_states.add(curr_state)

            for next_state in self.list_all_next_possible_states(curr_state):
                if next_state not in visited_states and self.is_state_in_bounds(next_state, sensor_data):
                    queue.append(next_state)
                    visited_states.add(next_state)
                    parent_map[next_state] = curr_state

        print('WARN Could not find solution from BFS solver')
            

