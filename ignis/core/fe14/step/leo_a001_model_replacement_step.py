from ignis.core.randomization_step import RandomizationStep


class LeoA001ModelReplacementStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.randomize_join_order

    def name(self) -> str:
        return "Leo A001 Model Replacement Step"

    def run(self, gd, user_config, dependencies):
        characters = dependencies.characters
        rom2 = gd.node("rom2").rid
        rom3 = gd.node("rom3").rid
        rom4 = gd.node("rom4").rid
        if replacement_pid := characters.get_replacement("PID_レオン"):
            replacement = characters.to_rid(replacement_pid)
            replacement_primary_class = gd.rid(replacement, "class_1")
            replacement_jid = gd.key(replacement_primary_class)
            replacement_aid = gd.string(replacement, "aid")
            if replacement_aid and replacement_jid:
                body_rid = gd.list_key_to_rid(rom2, "specs", replacement_jid)
                source_rid = gd.list_key_to_rid(rom3, "specs", replacement_aid)
                dest_rid = gd.list_key_to_rid(rom4, "specs", "AID_法衣裏返しレオン")
                if body_rid and source_rid and dest_rid:
                    gd.copy(source_rid, dest_rid, [])
                    gd.copy(
                        body_rid,
                        dest_rid, [
                            "body_model",
                            "body_texture",
                            "outer_clothing_model",
                            "outer_clothing_texture",
                            "accessory1_model",
                            "accessory1_texture",
                            "accessory2_model",
                            "accessory2_texture",
                            "accessory3_model",
                            "accessory3_texture",
                        ]
                    )
                    gd.set_string(dest_rid, "name", "AID_法衣裏返しレオン")
                    gd.set_store_dirty("rom4", True)
