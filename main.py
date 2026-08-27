"""
Imagem → PDF
------------
Aplicativo Android (Python + Kivy) para converter imagens em um único
arquivo PDF, 100% local no aparelho (sem servidores/APIs externas).

Ponto de entrada da aplicação.
"""
import os

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform

from screens.main_screen import MainScreen
from services.ads_service import AdsService
from utils.constants import COLOR_BACKGROUND, APP_NAME

KV_PATH = os.path.join(os.path.dirname(__file__), "kv", "main_screen.kv")


class ImagemParaPdfApp(App):
    """Classe principal do aplicativo."""

    title = APP_NAME

    def build(self):
        Window.clearcolor = COLOR_BACKGROUND
        Builder.load_file(KV_PATH)

        # Inicializa o serviço de anúncios (AdMob).
        # ATENÇÃO: usa exclusivamente IDs DE TESTE do Google
        # (ver utils/constants.py) enquanto o app estiver em
        # desenvolvimento.
        self.ads_service = AdsService()
        if platform == "android":
            self.ads_service.initialize()

        self.main_screen = MainScreen(ads_service=self.ads_service)
        return self.main_screen

    def on_start(self):
        # Solicita as permissões de armazenamento/fotos necessárias,
        # de acordo com a versão do Android do aparelho.
        from services.permissions_service import request_storage_permissions
        request_storage_permissions()

        if platform == "android":
            self.ads_service.show_banner()

    def on_stop(self):
        if platform == "android":
            self.ads_service.destroy_banner()


if __name__ == "__main__":
    ImagemParaPdfApp().run()
