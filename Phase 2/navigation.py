import heapq
import itertools

class Node:
    def __init__(self, name):
        self.name = name

        self.forward = None
        self.right = None
        self.back = None
        self.left = None

    def directions(self):
        dirs = [self.forward, self.right, self.back, self.left]
        return [edge for edge in dirs if edge is not None]

    def __repr__(self):
        return f"Node({self.name})"


def dijkstra_nav(start, destination):
    count = itertools.count() #this stops heapq from breaking when 2 paths are of equal distance
    pq = [(0, next(count), start, [start])] #creates the priority queue
    visited = set() #makes a list to store visited nodes

    while pq:
        dist, _, node, path = heapq.heappop(pq) #grabs the next node

        #if we have already visited the node, skip it
        if node in visited:
            continue
        #otherwise, add it to the visited list
        visited.add(node)

        #if the node is the destination, return the path and distance
        if node == destination:
            return dist, path

        #checks all directions from the current node
        for edge_dist, neighbor in node.directions():
            if neighbor not in visited:
                heapq.heappush(pq, (dist + edge_dist, next(count), neighbor, path + [neighbor]))

    return None

def build_map():
    #simply builds a sample map
    h1 = Node("Hallway 1")
    h2 = Node("Hallway 2")
    h3 = Node("Hallway 3")
    h4 = Node("Hallway 4")
    h5 = Node("Hallway 5")
    r101 = Node("Room 101")
    r102 = Node("Room 102")
    r103 = Node("Room 103")

    h1.forward = (50, h2)
    h2.back = (50, h1)

    h2.forward = (40, h3)
    h3.back = (40, h2)

    h3.right = (50, h4)
    h4.left = (50, h3)

    h4.back = (20, h5)
    h5.forward = (20, h4)

    h2.right = (20, h5)
    h5.left = (20, h2)

    h2.left = (5, r101)
    r101.right = (5, h2)

    h3.forward = (5, r102)
    r102.back = (5, h3)

    h4.right = (5, r103)
    r103.left = (5, h4)

    return {
        "Hallway 1": h1,
        "Hallway 2": h2,
        "Hallway 3": h3,
        "Hallway 4": h4,
        "Hallway 5": h5,
        "Room 101": r101,
        "Room 102": r102,
        "Room 103": r103
    }

def voice_navigation(route):
    #creates the script from the created route
    instructions = []

    for i in range(len(route) - 1):
        current = route[i]

        for direction, edge in {
            "forward": current.forward,
            "right": current.right,
            "back": current.back,
            "left": current.left
        }.items():
            if edge and edge[1] == route[i+1]:
                dist = edge[0]
                instructions.append(
                    f"Go {direction} {dist} feet to {route[i+1].name}."
                )
                break

    return instructions