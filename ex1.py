import operator
import sys

import search
import random
import math
import itertools
from collections import deque
ids = ["307951384", "322995358"]


def dict_to_tuples(dict, key):
    if key == 'clients':
        dict_paths = {}
        for name in dict.keys():
            dict_paths[name] = dict[name]['path']
        return [tuple([tuple(dict.keys()),
                       tuple([tuple([tuple(dict[name]['path'][0]), dict[name]['packages']]) for name in dict.keys()])]),
                dict_paths]
    else:
        return tuple([tuple(dict.keys()), tuple(dict.values())])


def move(state, action):
    to_change = list(state)
    drones_location = list(to_change[0][1])
    drone_num = to_change[0][0].index(action[1])
    drone_location = list(drones_location[drone_num])
    drone_location[0] = action[2][0]
    drone_location[1] = action[2][1]
    drones_location[drone_num] = tuple(drone_location)

    to_change[0] = tuple([to_change[0][0], tuple(drones_location)])

    return tuple(to_change)


def pick_up(state, action):
    to_change = list(state)
    orders = list(to_change[3])
    drone_num = to_change[0][0].index(action[1])
    package_num = to_change[1][0].index(action[2])
    drone_orders = list(orders[drone_num])
    drone_orders[0] += 1
    drone_orders[drone_orders[0]] = action[2]
    orders[drone_num] = tuple(drone_orders)
    to_change[3] = tuple(orders)
    packages = list(to_change[1])
    packages_keys = list(packages[0])
    packages_keys.remove(action[2])
    packages_locations = list(packages[1])
    del packages_locations[package_num]
    packages = [tuple(packages_keys), tuple(packages_locations)]
    to_change[1] = tuple(packages)
    return tuple(to_change)


def deliver(state, action):
    to_change = list(state)
    orders = list(to_change[3])
    drone_num = to_change[0][0].index(action[1])
    client_num = to_change[2][0].index(action[2])
    drone_orders = list(orders[drone_num])
    drone_orders[drone_orders[0]] = ""
    drone_orders[0] -= 1
    orders[drone_num] = tuple(drone_orders)
    to_change[3] = tuple(orders)
    clients = list(to_change[2])
    client = list(clients[1][client_num])
    client_packages = list(client[1])
    client_packages.remove(action[3])
    clients_values = list(clients[1])
    clients_keys = list(clients[0])
    if len(client_packages) == 0:
        clients_values.pop(client_num)
        clients_keys.pop(client_num)

    else:
        client = [tuple(tuple(client[0])), tuple(client_packages)]
        clients_values[client_num] = tuple(client)
    to_change[2] = tuple([tuple(clients_keys), tuple(clients_values)])
    return tuple(to_change)


class DroneProblem(search.Problem):
    """This class implements a medical problem according to problem description file"""

    def __init__(self, initial):
        """Don't forget to implement the goal test
        You should change the initial to your own representation.
        search.Problem.__init__(self, initial) creates the root node"""
        prob_path = []
        i = 0
        for row in initial['map']:
            for j in range(len(row)):
                if row[j] == "I":
                    prob_path.append((i, j))
            i += 1
        self.prob_path = (prob_path)
        self.map_size = (len(initial['map']), len(initial['map'][0]))
        self.step = 0
        list_clients = dict_to_tuples(initial['clients'], 'clients')
        self.paths = list_clients[1]
        initial = (
            dict_to_tuples(initial['drones'], 'drones'), dict_to_tuples(initial['packages'], 'packages'),
            list_clients[0], tuple(tuple(row) for row in ([[0, "", ""]] * len(initial['drones']))))
        search.Problem.__init__(self, initial)

    def actions(self, state):
        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""
        Alldrones_actions = []
        All_comb = []
        drones_pos = state[0][1]  # drone_pos==((3,3),(1,0))
        packs_pos = state[1][1]
        clients_path = state[2][1]
        on_drone_pacs = state[3]
        clients_names = state[2][0]
        drones_names = state[0][0]
        packs_names = state[1][0]
        drone_num = 0
        for point in drones_pos:
            drone_actions = []
            x_pos = point[0]
            y_pos = point[1]
            name_indice = 0
            # movments check
            if (x_pos + 1, y_pos) not in self.prob_path and (x_pos + 1 <= self.map_size[0] - 1):  # move right
                drone_actions.append(("move", drones_names[drone_num], (x_pos + 1, y_pos)))
            if (x_pos - 1, y_pos) not in self.prob_path and (x_pos - 1 >= 0):  # move left
                drone_actions.append(("move", drones_names[drone_num], (x_pos - 1, y_pos)))
            if (x_pos, y_pos + 1) not in self.prob_path and (y_pos + 1 <= self.map_size[1] - 1):  # move up
                drone_actions.append(("move", drones_names[drone_num], (x_pos, y_pos + 1)))
            if (x_pos, y_pos - 1) not in self.prob_path and (y_pos - 1 >= 0):  # move down
                drone_actions.append(("move", drones_names[drone_num], (x_pos, y_pos - 1)))
            # check for pickup
            if ((x_pos, y_pos) in packs_pos) and (on_drone_pacs[drone_num][0] < 2):
                for pac in range(len(packs_pos)):
                    if packs_pos[pac] == (x_pos, y_pos):
                        drone_actions.append(("pick up", drones_names[drone_num], packs_names[pac]))
            # check for delivery

            for client_pos in clients_path:
                if ((x_pos, y_pos) == client_pos[0]) and (on_drone_pacs[drone_num][0] > 0):
                    if on_drone_pacs[drone_num][1] in client_pos[1]:
                        drone_actions.append(("deliver", drones_names[drone_num], clients_names[name_indice],
                                              on_drone_pacs[drone_num][1]))
                    if on_drone_pacs[drone_num][2] in client_pos[1]:
                        drone_actions.append(("deliver", drones_names[drone_num], clients_names[name_indice],
                                              on_drone_pacs[drone_num][2]))
                name_indice += 1

            drone_actions.append(("wait", drones_names[drone_num]))
            drone_num += 1
            Alldrones_actions.append(drone_actions)

        for act in itertools.product(*Alldrones_actions):
            All_comb.append(act)
            # check for same drones pickup
        if len(drones_pos) > 1:
            for comb in All_comb:
                if (len(comb[0]) < 3) or (len(comb[1]) < 3):
                    continue
                else:
                    if (comb[0][0] == 'pick up') and (comb[1][0] == 'pick up'):
                        if (comb[0][2] == comb[1][2]):
                            All_comb.remove(comb)
        return All_comb

    def update_state(self, state):
        to_change = list(state)
        clients_values = list(state[2][1])
        clients_keys = state[2][0]
        i = 0
        for c_value in clients_values:
            path_len = len(self.paths[clients_keys[i]])
            cur_location = self.paths[state[2][0][i]][self.step % path_len]
            c_list = list(c_value[0])
            c_list[0] = cur_location[0]
            c_list[1] = cur_location[1]
            clients_values[i] = tuple([tuple(c_list), c_value[1]])
            i += 1
        to_change[2] = tuple([clients_keys, tuple(clients_values)])
        return tuple(to_change)

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        cur_state = state

        for act in action:
            if act[0] == 'move':
                cur_state = move(cur_state, act)
            elif act[0] == 'pick up':
                cur_state = pick_up(cur_state, act)
            elif act[0] == 'deliver':
                cur_state = deliver(cur_state, act)
        self.step += 1
        cur_state = self.update_state(cur_state)
        return cur_state

    def goal_test(self, state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""
        client_name = state[2][0]
        if len(client_name) == 0:
            return True
        return False

    def distance_in_map(self, state, source, destination):
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        q = deque()
        q.append([source[0], source[1], 0])
        visited = set()

        while q:
            x, y, dist = q.popleft()
            if x == destination[0] and y == destination[1]:
                return dist
            if tuple([x, y]) in self.prob_path:
                continue

            for direction in directions:
                new_point = [x + direction[0], y + direction[1]]
                if 0 <= new_point[0] < self.map_size[0] and 0 <= new_point[1] < self.map_size[1] and (
                        new_point[0], new_point[1]) not in visited:
                    q.append([new_point[0], new_point[1], dist + 1])
                    visited.add((new_point[0], new_point[1]))
        return sys.maxsize

    def dict_min(self, dict_values):
        min_val = sys.maxsize
        for value in dict_values:
            if value < min_val:
                min_val = value
        return min_val

    def closet_drone(self, state, package_location):
        min = sys.maxsize
        i = 0
        for drone_location in state[0][1]:
            cur_value = self.distance_in_map(state, list(package_location), list(drone_location))
            if cur_value < min:
                min = cur_value
            i += 1
        return min

    def package_location(self, state, package):
        if package in state[1][0]:
            package_num = state[1][0].index(package)
            return state[1][1][package_num]
        else:
            for i, drone_orders in enumerate(state[3]):
                return state[0][1][i]

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state,
        state can be accessed via node.state)
        and returns a goal distance estimate"""
        state = node.state
        if self.goal_test(state):
            return 0
        distance = 0
        for client_value in state[2][1]:
            for package in client_value[1]:
                package_loc = self.package_location(state, package)
                if package_loc == client_value[0] and (node.action[0] == 'wait' or node.action[0] == 'move'):
                    return 10000
                closest = self.closet_drone(state, package_loc)
                distance += closest ** 2
                distance += len(client_value[1]) ** 4
        distance += len(state[1][0]) * 2 + len(self.prob_path) ** 5
        return distance


    """Feel free to add your own functions
    (-2, -2, None) means there was a timeout"""


def create_drone_problem(game):
    return DroneProblem(game)
