from math import sqrt


class StreetNode:
    def __init__(self, name, lights, position, congestion):
        self.name = name
        self.straight = None
        self.left = None
        self.right = None
        self.lights = lights
        self.congestion = congestion
        self.position = position
        self.max_travel_distance = 586.1679

        self.cost_to_goal = 0

    def to_a_string(self):
        s1 = "name: %s" % self.name
        if self.straight is not None:
            s2 = "straight: %s" % self.straight.name
        else:
            s2 = "None"
        if self.left is not None:
            s3 = "left: %s" % self.left.name
        else:
            s3 = "None"
        if self.right is not None:
            s4 = "right: %s" % self.right.__class__.__name__
        else:
            s4 = "None"
        s5 = "lights: %s" % str(self.lights)
        s6 = "congestion: %s" % str(self.congestion)
        s7 = "position: %s" % self.position
        return s1, s2, s3, s4, s5, s6, s7

    def get_connected(self):
        connected = []
        if self.straight is not None:
            connected.append(self.straight)
        if self.left is not None:
            connected.append(self.left)
        if self.right is not None:
            connected.append(self.right)
        return connected

    def cost_to_road(self, road):
        return int(
            (road.congestion / 7 * 1000)
            + (self.calculate_distance(self.position, road.position) * 1000)
        )

    def calculate_distance(self, pos1, pos2):
        # distance between two vectors
        return sqrt((pow((pos1["x"] - pos2["x"]), 2) + pow((pos1["y"] - pos2["y"]), 2))) / self.max_travel_distance
        # expressed as a number between 0 and 1
        # print((sqrt((pow((pos1["x"] - pos2["x"]), 2) + pow((pos1["y"] - pos2["y"]), 2)))) / main.max_travel_distance)
