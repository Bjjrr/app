"""
Seleção de imagens da galeria do dispositivo.

Usa `plyer.filechooser`, que no Android abre o seletor nativo do
sistema (Storage Access Framework) com suporte a seleção múltipla,
sem exigir nenhuma API externa nem conexão com a internet.
"""
from plyer import filechooser

from utils.constants import SUPPORTED_EXTENSIONS


def pick_images(on_selection):
    """
    Abre o seletor nativo de imagens.

    `on_selection` é chamado com a lista de caminhos escolhidos
    (lista vazia caso o usuário cancele).
    """
    ext_filters = [f"*{ext}" for ext in SUPPORTED_EXTENSIONS]

    def _callback(selection):
        if not selection:
            on_selection([])
            return
        valid = [p for p in selection if p.lower().endswith(SUPPORTED_EXTENSIONS)]
        on_selection(valid)

    filechooser.open_file(
        multiple=True,
        filters=[("Imagens", ext_filters)],
        on_selection=_callback,
    )
