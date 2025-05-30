from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, \
    QVBoxLayout, QSpacerItem, QSizePolicy, QCheckBox
from PySide6.QtGui import QFont, QPixmap, Qt
import os
from data.pokemon_obj import PokemonData

class PokemonListItem(QWidget):
    def __init__(self, pokemon_data: PokemonData, parent=None):
        super(PokemonListItem, self).__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(6)

        # Name Label
        name_label = QLabel(pokemon_data.name)
        name_label.setFont(QFont("Arial", 12, QFont.Bold))
        name_label.setFixedWidth(120)
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)

        # Types
        types_layout = QHBoxLayout()
        for pokemon_type in pokemon_data.types:
            type_icon = QLabel()
            svg_path = os.path.join("assets", "icons", f"{pokemon_type.lower()}.svg")
            pixmap = QPixmap(svg_path)
            if not pixmap.isNull():
                type_icon.setPixmap(pixmap.scaled(36, 36))
            else:
                type_icon.setText(pokemon_type)
            types_layout.addWidget(type_icon)

        types_layout.setAlignment(Qt.AlignCenter)
        types_widget = QWidget()
        types_widget.setLayout(types_layout)
        types_widget.setFixedWidth(100)
        layout.addWidget(types_widget)

        # Abilities
        abilities_layout = QHBoxLayout()

        base_abilities_layout = QVBoxLayout()
        for ability in pokemon_data.base_abilities:
            ability_label = QLabel(ability)
            ability_label.setFixedWidth(100)
            base_abilities_layout.addWidget(ability_label)
        abilities_layout.addLayout(base_abilities_layout)

        hidden_abilities_layout = QVBoxLayout()
        for ability in pokemon_data.hidden_abilities:
            ability_label = QLabel(ability)
            ability_label.setFixedWidth(100)
            hidden_abilities_layout.addWidget(ability_label)
        abilities_layout.addLayout(hidden_abilities_layout)

        abilities_layout.setAlignment(Qt.AlignCenter)
        abilities_widget = QWidget()
        abilities_widget.setLayout(abilities_layout)
        abilities_widget.setFixedWidth(200)
        layout.addWidget(abilities_widget)

        # Stats
        for stat in pokemon_data.stats + [sum(pokemon_data.stats)]:  # Include BST
            stat_label = QLabel(str(stat))
            stat_label.setFixedWidth(30)
            layout.addWidget(stat_label)

        self.setLayout(layout)

class SettingsPokemonListItem(QWidget):
    def __init__(self, pokemon_data: PokemonData, parent=None):
        super(SettingsPokemonListItem, self).__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignLeft)

        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox)

        num_label = QLabel(str(pokemon_data[0]))
        num_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(num_label)

        name_label = QLabel(pokemon_data[1])
        name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(name_label)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)

        self.setLayout(layout)