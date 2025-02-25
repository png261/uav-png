from .Swarm import Swarm
from .Map import Map


class SwarmManager:
    def __init__(self):
        self.uavs = []  # List of all UAVs
        self.swarms = []  # List of all swarms

    def add_uav(self, uav):
        swarm = Swarm([uav], uav.x, uav.y)  # Each UAV starts as its own swarm
        self.swarms.append(swarm)
        uav.swarm = swarm
        self.uavs.append(uav)

    def handle_events(self, ground_map: Map):
        for swarm in self.swarms:
            swarm.handle_events(ground_map)

    def update(self):
        for swarm in self.swarms:
            swarm.update()

        # Check for nearby swarms and merge them
        for i, swarm1 in enumerate(self.swarms):
            for j, swarm2 in enumerate(self.swarms):
                if i >= j:
                    continue
                if swarm1.is_near(swarm2) and swarm2.is_near(swarm1):
                    swarm1.merge(swarm2)
                    self.swarms.remove(swarm2)
                    # Update UAV references to the merged swarm
                    for uav in swarm2.uavs:
                        uav.swarm = swarm1

    def draw(self):
        for swarm in self.swarms:
            swarm.draw()
