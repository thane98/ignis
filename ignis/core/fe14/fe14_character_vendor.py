import ctypes
from random import Random

from ignis.core.fe14 import fe14_utils

from ignis.core.fe14.fe14_character_shuffler import FE14CharacterShuffler
from ignis.core.fe14.fe14_classes_vendor import FE14ClassesVendor
from ignis.core.fe14.fe14_skills_vendor import FE14SkillsVendor
from ignis.model.fe14_character_info import FE14CharacterInfo
from ignis.model.fe14_character_report import FE14CharacterReport
from ignis.model.fe14_user_config import FE14UserConfig

from ignis.model.fe14_game_config import FE14GameConfig


_BITFLAG_SWAPS = [
    ("bitflags_1", 0b00000000),
    ("bitflags_2", 0b00000000),
    ("bitflags_3", 0b00000000),
    ("bitflags_4", 0b11000000),
    ("bitflags_5", 0b00001011),
    ("bitflags_6", 0b01000000),
    ("bitflags_7", 0b00011001),
    ("bitflags_8", 0b01100000),
]
_MALE_CORRIN = "PID_プレイヤー男"
_FEMALE_CORRIN = "PID_プレイヤー女"

_MALE_KANA = "PID_カンナ男"
_FEMALE_KANA = "PID_カンナ女"


class FE14CharactersVendor:
    def __init__(
        self,
        gd,
        game_config: FE14GameConfig,
        user_config: FE14UserConfig,
        skills: FE14SkillsVendor,
        classes: FE14ClassesVendor,
        rand: Random,
    ):
        self.gd = gd
        self.game_config = game_config
        self.user_config = user_config
        self.skills = skills
        self.classes = classes
        self.rand = rand

        # Used to refer to the original character's data to prevent
        # evaluation order impacting results.
        self.originals = {}

        # Used for preserving state across randomizing steps.
        self.character_skills = {}
        self.character_classes = {}
        self.character_bitflags = {}
        self.character_aliases = {}

        # Filter out characters based on user config
        characters = list(
            filter(
                lambda c: self._should_include_character(c, user_config),
                self.game_config.characters,
            )
        )

        # Cache some mappings for faster access
        rid, field_id = gd.table("characters")
        self.pid_to_rid = gd.key_to_rid_mapping(rid, field_id)
        self.enabled_pids = [c.pid for c in characters]

        # Update class levels based on what's in the ROM
        for c in characters:
            rid = self.pid_to_rid[c.pid]
            primary_class = gd.rid(rid, "class_1")
            c.class_level = classes.get_class_level(primary_class)

        # Create the swaps list
        # If join order randomization is disabled, use an identity mapping
        if user_config.randomize_join_order:
            shuffler = FE14CharacterShuffler(user_config, rand)
            self.swaps = shuffler.shuffle(characters)
        else:
            self.swaps = list(zip(characters, characters))
        self.pid_to_replacement = {r.pid: c.pid for c, r in self.swaps}

        # Cache originals.
        for character in characters:
            rid = gd.new_instance("Person")
            gd.copy(self.pid_to_rid[character.pid], rid, [])
            self.originals[character.pid] = rid

        # Build aid to rid mapping so we can match while going over person files
        self.aid_to_rid = {}
        for character in characters:
            rid = self.to_rid(character.pid)
            if aid := gd.string(rid, "aid"):
                if aid not in self.aid_to_rid:
                    self.aid_to_rid[aid] = rid

    def get_parent(self, rid):
        parent = self.gd.rid(rid, "parent")
        if parent:
            replacement = self.get_replacement(self.gd.key(parent))
            if replacement:
                return self.to_rid(replacement)
        return None

    def default_character(self):
        rid, field_id = self.gd.table("characters")
        return self.gd.list_get(rid, field_id, 0)

    def get_global_character(self, pid, aid=None):
        if aid and aid in self.aid_to_rid:
            replacement = self.get_replacement(self.gd.key(self.aid_to_rid[aid]))
            self.character_aliases[pid] = replacement
            return self.aid_to_rid[aid]
        if pid in self.enabled_pids:
            return self.to_rid(pid)
        if pid in self.character_aliases:
            return self.to_rid(self.character_aliases[pid])
        if pid.startswith("PID_A_"):
            return self._handover_to_global_character(
                pid, "GameData/Person/A_HANDOVER.bin.lz"
            )
        if pid.startswith("PID_B_"):
            return self._handover_to_global_character(
                pid, "GameData/Person/B_HANDOVER.bin.lz"
            )
        if pid.startswith("PID_C_"):
            return self._handover_to_global_character(
                pid, "GameData/Person/C_HANDOVER.bin.lz"
            )
        return None

    def to_rid(self, pid):
        return self.pid_to_rid[pid]

    def get_replacement(self, pid):
        return self.pid_to_replacement.get(pid)

    def get_original(self, pid):
        return self.originals[pid]

    def get_character_personal_skill(self, aid):
        if aid in self.character_skills:
            return self.character_skills[aid]
        else:
            skill = self.skills.random_personal_skill()
            self.character_skills[aid] = skill
            return skill

    def get_character_class_set(
        self, aid, gender=None, level=None, staff_only_ban=False
    ):
        if aid in self.character_classes:
            return self.character_classes[aid]
        elif not gender or not level:
            raise ValueError("Need character info to generate a class set.")
        else:
            class_set = self.classes.random_class_set(gender, level, staff_only_ban)
            self.character_classes[aid] = class_set
            return class_set

    def get_character_bitflags(self, aid, char=None, replacing=None):
        if aid in self.character_bitflags:
            return self.character_bitflags[aid]
        elif not char or not replacing:
            raise ValueError("Need character info to generate bitflags.")
        else:
            bitflags = {}
            for f, m in _BITFLAG_SWAPS:
                new_bits = self.gd.int(replacing, f) & m
                char_bits = self.gd.int(char, f) & (~m)
                bitflags[f] = char_bits | new_bits
            self.character_bitflags[aid] = bitflags
            return bitflags

    def get_dialogue_replacements(self):
        replacements = {}
        for character, replacing in self.swaps:
            char_rid = self.pid_to_rid[character.pid]
            replacing_rid = self.pid_to_rid[replacing.pid]
            char_fid = self.gd.string(char_rid, "fid")
            replacing_fid = self.gd.string(replacing_rid, "fid")
            char_name = self.gd.display(char_rid)
            replacing_name = self.gd.display(replacing_rid)
            if char_fid and replacing_fid:
                replacements[replacing_fid[4:]] = char_fid[4:]
            replacements[replacing_name] = char_name
            replacements[replacing_name.upper()] = char_name.upper()
            replacements[replacing.voice_set] = character.voice_set
        return replacements

    def get_script_replacements(self):
        replacements = {}
        for character, replacing in self.swaps:
            char_rid = self.pid_to_rid[character.pid]
            replacing_rid = self.pid_to_rid[replacing.pid]
            char_aid = self.gd.string(char_rid, "aid")
            replacing_aid = self.gd.string(replacing_rid, "aid")
            if char_aid and replacing_aid:
                replacements[replacing_aid[4:]] = char_aid[4:]
            replacements[replacing.pid] = character.pid
        return replacements

    def generate_character_reports(self):
        reports = list(
            map(lambda t: self._generate_report_for_character(t[0], t[1]), self.swaps)
        )
        return [
            self._generate_report_for_mu(_MALE_CORRIN, "Corrin (M)"),
            self._generate_report_for_mu(_FEMALE_CORRIN, "Corrin (F)"),
            *reports,
        ]

    def _generate_report_for_mu(self, pid, name):
        char_rid = self.to_rid(pid)
        primary_class_name = self.gd.display(self.gd.rid(char_rid, "class_1"))
        secondary_class_name = self.gd.display(self.gd.rid(char_rid, "class_2"))
        reclass_1_name = self.gd.display(self.gd.rid(char_rid, "reclass_1"))
        reclass_2_name = self.gd.display(self.gd.rid(char_rid, "reclass_2"))
        personal_skill_name = self.gd.display(
            self.gd.rid(char_rid, "personal_skill_normal")
        )
        equipped_skills = fe14_utils.get_equipped_skill_names(
            self.gd, self.skills, char_rid
        )
        bases = self.bytes_to_signed_int_list(self.gd.bytes(char_rid, "bases"))
        growths = self.bytes_to_signed_int_list(self.gd.bytes(char_rid, "growths"))
        modifiers = self.bytes_to_signed_int_list(self.gd.bytes(char_rid, "modifiers"))
        level = self.gd.int(char_rid, "level")
        internal_level = self.gd.int(char_rid, "internal_level")
        return FE14CharacterReport(
            name,
            None,
            primary_class_name,
            secondary_class_name,
            [reclass_1_name, reclass_2_name],
            personal_skill_name,
            equipped_skills,
            bases,
            growths,
            modifiers,
            level,
            internal_level,
        )

    def _generate_report_for_character(self, character, replacing):
        char_rid = self.to_rid(character.pid)
        replacing_rid = self.to_rid(replacing.pid)
        name = self.gd.display(char_rid)
        replacing_name = self.gd.display(replacing_rid)
        primary_class_name = self.gd.display(self.gd.rid(char_rid, "class_1"))
        secondary_class_name = self.gd.display(self.gd.rid(char_rid, "class_2"))
        reclass_1_name = self.gd.display(self.gd.rid(char_rid, "reclass_1"))
        reclass_2_name = self.gd.display(self.gd.rid(char_rid, "reclass_2"))
        personal_skill_name = self.gd.display(
            self.gd.rid(char_rid, "personal_skill_normal")
        )
        equipped_skills = fe14_utils.get_equipped_skill_names(
            self.gd, self.skills, char_rid
        )
        bases = self.bytes_to_signed_int_list(self.gd.bytes(char_rid, "bases"))
        growths = self.bytes_to_signed_int_list(self.gd.bytes(char_rid, "growths"))
        modifiers = self.bytes_to_signed_int_list(self.gd.bytes(char_rid, "modifiers"))
        level = self.gd.int(char_rid, "level")
        internal_level = self.gd.int(char_rid, "internal_level")
        # add markers in the report to distinguish between male and female kana
        for (kana_pid, suffix) in [(_MALE_KANA, " (M)"), (_FEMALE_KANA, " (F)")]:
            if char_rid == self.to_rid(kana_pid):
                name += suffix
            if replacing_rid == self.to_rid(kana_pid):
                replacing_name += suffix
        return FE14CharacterReport(
            name,
            replacing_name,
            primary_class_name,
            secondary_class_name,
            [reclass_1_name, reclass_2_name],
            personal_skill_name,
            equipped_skills,
            bases,
            growths,
            modifiers,
            level,
            internal_level,
        )

    def _handover_to_global_character(self, pid, key):
        if self.gd.file_exists(key, False):
            rid = self.gd.multi_open("person", key)
            return self.gd.list_key_to_rid(rid, "people", pid)
        else:
            return None

    @staticmethod
    def bytes_to_signed_int_list(buffer):
        return list(map(lambda b: ctypes.c_int8(b).value, buffer))

    @staticmethod
    def _should_include_character(c: FE14CharacterInfo, user_config: FE14UserConfig):
        if not user_config.include_anna_in_character_pool and "anna" in c.flags:
            return False
        if (
            not user_config.include_amiibo_units_in_character_pool
            and "amiibo" in c.flags
        ):
            return False
        if not user_config.randomize_children and c.generation == 2:
            return False
        return bool(len(set(user_config.routes).intersection(c.routes)))
