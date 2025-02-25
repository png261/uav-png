class Cluster:
    def __init__(self, centroid: [float, float], radius: float, important_score: int):
        self.centroid = centroid
        self.radius = radius
        self.important_score = important_score

    def draw(self):
        from .Game import Game
        from .engine.TextManager import TextManager

        Game().getWindow().draw_circle(self.centroid, 20, "red")
        Game().getWindow().draw_circle(self.centroid, self.radius, "red", 2)

        TextManager().print(
            window=Game().getWindow(),
            text=str(self.important_score),
            position=self.centroid,
            color="black",
            font_size=30,
        )

    def update(self):
        pass

    def handle_events(self):
        pass

    def clean(self):
        pass
