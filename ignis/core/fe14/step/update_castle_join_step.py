from ignis.core.randomization_step import RandomizationStep


class UpdateCastleJoinStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return user_config.randomize_join_order or user_config.add_anna_to_castle_join

    def name(self) -> str:
        return "Update Castle Join"

    def run(self, gd, user_config, dependencies):
        chapters = dependencies.chapters
        characters = dependencies.characters

        table_rid, table_field_id = gd.table("castlejoin")

        # Add Anna to castle join if necessary
        if user_config.add_anna_to_castle_join and not gd.key_to_rid(
            "castlejoin", "PID_アンナ"
        ):
            # Sanity check: Is Anna in the character pool?
            if not characters.to_rid("PID_アンナ"):
                return

            # Okay, now we can add her.
            rid = gd.list_add(table_rid, table_field_id)
            gd.set_rid(rid, "character", characters.to_rid("PID_アンナ"))
            gd.set_rid(rid, "birthright_chapter", chapters.to_rid("CID_A007"))
            gd.set_rid(rid, "conquest_chapter", chapters.to_rid("CID_B007"))
            gd.set_rid(rid, "revelation_chapter", chapters.to_rid("CID_C007"))
            gd.set_int(rid, "required_building_1", -1)
            gd.set_int(rid, "required_building_2", -1)
            gd.set_int(rid, "required_building_3", -1)

        # Apply swaps
        for rid in gd.items(table_rid, table_field_id):
            pid = gd.key(gd.rid(rid, "character"))
            if replacement_pid := characters.get_replacement(pid):
                character_rid = characters.to_rid(replacement_pid)
                gd.set_rid(rid, "character", character_rid)

        gd.set_store_dirty("castle_join", True)
