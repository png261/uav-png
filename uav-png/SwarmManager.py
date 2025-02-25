from .Swarm import Swarm
from .GroundMap import GroundMap


class SwarmManager:
    def __init__(self):
        self.uavs = []
        self.swarms = []

    def add_uav(self, uav):
        swarm = Swarm([uav], uav.pos)
        self.swarms.append(swarm)
        uav.swarm = swarm
        self.uavs.append(uav)

    def handle_events(self, ground_map: GroundMap):
        for swarm in self.swarms:
            swarm.handle_events(ground_map)

    def update(self):
        for swarm in self.swarms:
            swarm.update()

        for i, swarm1 in enumerate(self.swarms):
            for j, swarm2 in enumerate(self.swarms):
                if i >= j:
                    continue
                if swarm1.is_near(swarm2) and swarm2.is_near(swarm1):
                    swarm1.merge(swarm2)
                    self.swarms.remove(swarm2)
                    for uav in swarm2.uavs:
                        uav.swarm = swarm1

    def draw(self):
        for swarm in self.swarms:
            swarm.draw()

    def clean(self):
        for swarm in self.swarms:
            swarm.clean()

        for uav in self.uavs:
            uav.clean()
