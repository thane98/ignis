import csv
import os
from types import SimpleNamespace
from zipfile import ZipFile

from ignis.core.randomization_step import RandomizationStep


DATA_FILE = "Data/Misc/gen1data.csv"
HAIR_TEXTURES_ARCHIVE = "Data/Misc/Gen1ModelHair.zip"
PORTRAIT_HAIR_ARCHIVE = "Data/Misc/Gen1PortraitHair.zip"
SPRITES_ARCHIVE = "Data/Misc/Gen1Sprites.zip"
SPRITE_FILES = [
    "赤0.bch.lz",
    "赤1.bch.lz",
    "緑0.bch.lz",
    "緑1.bch.lz",
    "紫0.bch.lz",
    "紫1.bch.lz",
    "青0.bch.lz",
    "青1.bch.lz",
]


class AddCrossGenerationAssetsStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return (
            user_config.randomize_join_order
            and user_config.randomize_children
            and user_config.mix_generations
        )

    def name(self) -> str:
        return "Add Cross Generation Assets"

    def run(self, gd, user_config, dependencies):
        characters = dependencies.characters
        output_path = dependencies.output_path
        gen1data = self._load_gen1data()

        dirty = False
        targets = characters.get_gen1_to_gen2_swaps()

        with ZipFile(HAIR_TEXTURES_ARCHIVE, "r") as hair_textures, ZipFile(
            PORTRAIT_HAIR_ARCHIVE, "r"
        ) as portrait_hair, ZipFile(SPRITES_ARCHIVE, "r") as sprites:
            for char in targets:
                data = gen1data.get(char.pid)
                if not (data and data.portrait == "TRUE" and data.sprite == "TRUE"):
                    continue
                dirty = True

                self._update_portrait_data(gd, characters, char)
                self._export_portrait_hair(output_path, data, portrait_hair)
                self._export_hair_texture(output_path, data, hair_textures)
                self._export_sprites(output_path, data, sprites)
        if dirty:
            gd.set_store_dirty("facedata", True)

    @staticmethod
    def _update_portrait_data(gd, characters, char):
        rid = characters.to_rid(char.pid)
        fid = gd.string(rid, "fid")
        st_rid = gd.key_to_rid("portraits", f"FSID_ST_{fid[4:]}")
        gd.set_string(st_rid, "hair_file", char.pid[4:] + "_st")
        bu_rid = gd.key_to_rid("portraits", f"FSID_BU_{fid[4:]}")
        gd.set_string(bu_rid, "hair_file", char.pid[4:] + "_bu")

    @staticmethod
    def _export_portrait_hair(output_path, data, portrait_hair: ZipFile):
        path = os.path.join(output_path, "face", "hair")
        portrait_hair.extract(
            f"{data.japanese}_st/髪0.bch.lz",
            path
        )
        portrait_hair.extract(
            f"{data.japanese}_bu/髪0.bch.lz",
            path
        )

    @staticmethod
    def _export_hair_texture(output_path, data, hair_textures: ZipFile):
        gender = data.gender[0].upper()
        member = f"uHair_{gender}_ch{data.ch}_0_cl0n.bch.lz"
        path = os.path.join(output_path, "bu")
        hair_textures.extract(member, path)
        if data.name in {"Peri"}:
            member = f"uHair_{gender}_ch{data.ch}_0.bch.lz"
            path = os.path.join(output_path, "bu")
            hair_textures.extract(member, path)

    @staticmethod
    def _export_sprites(output_path, data, sprites: ZipFile):
        for f in SPRITE_FILES:
            member = data.japanese + "/" + f
            path = os.path.join(output_path, "unit", "Head")
            sprites.extract(member, path)

    @staticmethod
    def _load_gen1data():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            rows = list(map(lambda r: SimpleNamespace(**r), csv.DictReader(f)))
        return {"PID_" + row.japanese: row for row in rows}
