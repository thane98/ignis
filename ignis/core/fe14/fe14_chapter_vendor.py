from ignis.model.fe14_route import FE14Route

from ignis.model.fe14_user_config import FE14UserConfig

from ignis.model.fe14_game_config import FE14GameConfig


class FE14ChapterVendor:
    def __init__(self, gd, game_config: FE14GameConfig, user_config: FE14UserConfig):
        self.gd = gd
        self.game_config = game_config
        self.user_config = user_config

        self.chapters = list(
            map(lambda c: (FE14Route.ALL, c), game_config.global_chapters)
        )
        for route, route_chapters in game_config.route_chapters.items():
            if route in user_config.routes:
                self.chapters.extend(map(lambda c: (route, c), route_chapters))

        rid, field_id = gd.table("chapters")
        self.cid_to_rid = gd.key_to_rid_mapping(rid, field_id)

    def enabled_chapters(self):
        return self.chapters

    def to_rid(self, cid):
        return self.cid_to_rid.get(cid)
