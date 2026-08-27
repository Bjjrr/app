"""
Botão com cantos arredondados e cor de fundo customizável, usado em
toda a interface para manter a identidade visual moderna do app.
"""
from kivy.uix.button import Button
from kivy.properties import ListProperty


class RoundedButton(Button):
    """Botão com cantos arredondados e `bg_color` configurável."""

    bg_color = ListProperty([0.13, 0.42, 0.87, 1])
