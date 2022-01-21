from PySide6 import QtGui
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QCheckBox,
    QVBoxLayout,
    QGroupBox,
    QRadioButton,
    QSpinBox,
    QFormLayout,
)


class Ui_FE14UserConfigForm(QWidget):
    def __init__(self):
        super().__init__()

        self.birthright_check_box = QCheckBox("Birthright")
        self.birthright_check_box.setChecked(True)
        self.conquest_check_box = QCheckBox("Conquest")
        self.conquest_check_box.setChecked(True)
        self.revelation_check_box = QCheckBox("Revelation")
        self.revelation_check_box.setChecked(True)
        route_box_layout = QVBoxLayout()
        route_box_layout.setSpacing(0)
        route_box_layout.setContentsMargins(5, 5, 5, 5)
        route_box_layout.setAlignment(QtGui.Qt.AlignTop)
        route_box_layout.addWidget(self.birthright_check_box)
        route_box_layout.addWidget(self.conquest_check_box)
        route_box_layout.addWidget(self.revelation_check_box)
        route_box = QGroupBox("Routes")
        route_box.setLayout(route_box_layout)

        self.anna_check_box = QCheckBox("Anna")
        self.anna_check_box.setChecked(True)
        self.amiibo_check_box = QCheckBox("Amiibo Units")
        self.amiibo_check_box.setChecked(True)
        self.children_check_box = QCheckBox("Children")
        self.children_check_box.setChecked(True)
        self.player_check_box = QCheckBox("Corrin (EXPERIMENTAL)")
        characters_box_layout = QVBoxLayout()
        characters_box_layout.setSpacing(0)
        characters_box_layout.setContentsMargins(5, 5, 5, 5)
        characters_box_layout.setAlignment(QtGui.Qt.AlignTop)
        characters_box_layout.addWidget(self.anna_check_box)
        characters_box_layout.addWidget(self.amiibo_check_box)
        characters_box_layout.addWidget(self.children_check_box)
        characters_box_layout.addWidget(self.player_check_box)
        characters_box = QGroupBox("Optional Characters")
        characters_box.setLayout(characters_box_layout)

        passes_layout = QFormLayout()
        passes_layout.setContentsMargins(0, 0, 0, 0)
        passes_layout.setAlignment(QtGui.Qt.AlignTop)
        self.passes_spin_box = QSpinBox()
        self.passes_spin_box.setRange(5, 40)
        self.passes_spin_box.setValue(20)
        passes_layout.addRow("Passes", self.passes_spin_box)

        self.weighted_redistribute_stats_radio = QRadioButton("Weighted Redistribute")
        self.weighted_redistribute_stats_radio.setChecked(True)
        self.redistribute_stats_radio = QRadioButton("Redistribute")
        self.shuffle_stats_radio = QRadioButton("Shuffle")
        self.no_stats_radio = QRadioButton("None")
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(0)
        stats_layout.setContentsMargins(5, 5, 5, 5)
        stats_layout.setAlignment(QtGui.Qt.AlignTop)
        stats_layout.addLayout(passes_layout)
        stats_layout.addWidget(self.weighted_redistribute_stats_radio)
        stats_layout.addWidget(self.redistribute_stats_radio)
        stats_layout.addWidget(self.shuffle_stats_radio)
        stats_layout.addWidget(self.no_stats_radio)
        stats_box = QGroupBox("Stat Randomization")
        stats_box.setLayout(stats_layout)

        self.randomize_join_order_check_box = QCheckBox("Randomize Join Order")
        self.randomize_join_order_check_box.setChecked(True)
        self.same_sex_only_check_box = QCheckBox("Same-Sex Swaps Only")
        self.same_sex_only_check_box.setChecked(True)
        self.mix_generations_check_box = QCheckBox("Mix Generations")
        self.mix_generations_check_box.setChecked(True)
        self.corrinsexuals_pool_check_box = QCheckBox(
            'Use a Separate Pool for "Corrinsexuals"'
        )
        join_order_layout = QVBoxLayout()
        join_order_layout.setSpacing(0)
        join_order_layout.setContentsMargins(5, 5, 5, 5)
        join_order_layout.setAlignment(QtGui.Qt.AlignTop)
        join_order_layout.addWidget(self.randomize_join_order_check_box)
        join_order_layout.addWidget(self.same_sex_only_check_box)
        join_order_layout.addWidget(self.mix_generations_check_box)
        join_order_layout.addWidget(self.corrinsexuals_pool_check_box)
        join_order_box = QGroupBox("Join Order Randomization")
        join_order_box.setLayout(join_order_layout)

        self.randomize_personal_skills_check_box = QCheckBox(
            "Randomize Personal Skills"
        )
        self.randomize_personal_skills_check_box.setChecked(True)
        self.randomize_equip_skills_check_box = QCheckBox("Randomize Equip Skills")
        self.randomize_equip_skills_check_box.setChecked(True)
        self.include_all_skills_check_box = QCheckBox(
            "Include ALL Skills in the Skill Pool"
        )
        self.include_all_skills_check_box.setChecked(False)

        skills_layout = QVBoxLayout()
        skills_layout.setSpacing(0)
        skills_layout.setContentsMargins(5, 5, 5, 5)
        skills_layout.setAlignment(QtGui.Qt.AlignTop)
        skills_layout.addWidget(self.randomize_personal_skills_check_box)
        skills_layout.addWidget(self.randomize_equip_skills_check_box)
        skills_layout.addWidget(self.include_all_skills_check_box)
        skills_box = QGroupBox("Skills")
        skills_box.setLayout(skills_layout)

        self.randomize_classes_check_box = QCheckBox("Randomize Classes")
        self.randomize_classes_check_box.setChecked(True)
        self.randomize_chest_items_check_box = QCheckBox("Randomize Chest Items")
        self.randomize_chest_items_check_box.setChecked(True)
        self.unlock_hero_battles_check_box = QCheckBox("Unlock Hero Battles")
        self.unlock_hero_battles_check_box.setChecked(True)
        self.add_anna_check_box = QCheckBox(
            "Add Anna (or her replacement) to Castle Join"
        )
        self.add_anna_check_box.setChecked(True)
        self.add_sprite_fix_box = QCheckBox("Add Moonling's Generic Songstress Sprite")
        self.add_sprite_fix_box.setChecked(True)
        self.animation_fixes_check_box = QCheckBox("Apply Animation Fixes")
        self.feral_dragon_head_fix_check_box = QCheckBox("Feral Dragon Head Fix")
        self.feral_dragon_head_fix_check_box.setChecked(True)
        combat_and_misc_layout = QVBoxLayout()
        combat_and_misc_layout.setSpacing(0)
        combat_and_misc_layout.setContentsMargins(5, 5, 5, 5)
        combat_and_misc_layout.setAlignment(QtGui.Qt.AlignTop)
        combat_and_misc_layout.addWidget(self.randomize_classes_check_box)
        combat_and_misc_layout.addWidget(self.randomize_chest_items_check_box)
        combat_and_misc_layout.addWidget(self.unlock_hero_battles_check_box)
        combat_and_misc_layout.addWidget(self.add_anna_check_box)
        combat_and_misc_layout.addWidget(self.add_sprite_fix_box)
        combat_and_misc_layout.addWidget(self.animation_fixes_check_box)
        combat_and_misc_layout.addWidget(self.feral_dragon_head_fix_check_box)
        combat_and_misc_box = QGroupBox("Classes and Misc.")
        combat_and_misc_box.setLayout(combat_and_misc_layout)

        self.seed_input = QSpinBox()
        self.seed_input.setRange(-2147483648, 2147483647)
        seed_layout = QVBoxLayout()
        seed_layout.setContentsMargins(5, 5, 5, 5)
        seed_layout.addWidget(self.seed_input)
        seed_box = QGroupBox("RNG Seed")
        seed_box.setLayout(seed_layout)

        grid = QGridLayout()
        grid.setSpacing(2)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(route_box, 0, 0)
        grid.addWidget(characters_box, 1, 0)
        grid.addWidget(join_order_box, 0, 1)
        grid.addWidget(stats_box, 1, 1)
        grid.addWidget(skills_box, 0, 2, 1, 1)
        grid.addWidget(combat_and_misc_box, 1, 2, 1, 1)
        grid.addWidget(seed_box, 2, 0, 1, 3)

        self.setLayout(grid)
