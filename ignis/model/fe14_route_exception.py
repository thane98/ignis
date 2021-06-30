from ignis.model.fe14_route import FE14Route


class FE14RouteException(Exception):
    def __init__(self, route: FE14Route):
        super().__init__()
        self.route = route
