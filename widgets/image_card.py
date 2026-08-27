"""
Card visual que representa uma imagem selecionada: miniatura, nome do
arquivo, botões de mover (subir/descer) e botão de remover.
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty


class ImageCard(BoxLayout):
    """Widget de card exibindo a miniatura + nome de uma imagem."""

    image_path = StringProperty("")
    image_name = StringProperty("")
    on_remove = ObjectProperty(None)  # callback(path) chamado ao remover

    def remove_pressed(self):
        if self.on_remove:
            self.on_remove(self.image_path)
