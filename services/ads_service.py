"""
Integração com Google AdMob usando a biblioteca `kivmob`.

IMPORTANTE: os IDs usados aqui (importados de utils/constants.py) são
os IDs DE TESTE OFICIAIS do Google. Veja o README.md, seção "Trocando
para IDs reais", antes de publicar o app.

Regras seguidas nesta implementação (para não violar as políticas do
AdMob e não arriscar bloqueio da conta):
  - Nenhum clique automático em anúncios.
  - Nenhuma impressão artificial.
  - O interstitial só é solicitado a ser exibido em um momento
    específico do fluxo (após gerar um PDF) — nunca a cada clique do
    usuário na interface.
"""
from kivy.utils import platform
from kivy.clock import Clock

from utils.constants import BANNER_AD_UNIT_ID, INTERSTITIAL_AD_UNIT_ID


class AdsService:
    def __init__(self):
        self.kivmob = None
        self._interstitial_ready = False

    def initialize(self):
        """Inicializa o SDK do AdMob (somente em Android)."""
        if platform != "android":
            return

        from kivmob import KivMob

        self.kivmob = KivMob()
        self.kivmob.new_banner(BANNER_AD_UNIT_ID, top_pos=False)
        self.kivmob.new_interstitial(INTERSTITIAL_AD_UNIT_ID)

        self.kivmob.set_on_interstitial_load(self._on_interstitial_loaded)

        self.kivmob.request_banner()
        self.kivmob.request_interstitial()

    def _on_interstitial_loaded(self):
        self._interstitial_ready = True

    def show_banner(self):
        if self.kivmob:
            self.kivmob.show_banner()

    def destroy_banner(self):
        if self.kivmob:
            self.kivmob.destroy_banner()

    def show_interstitial_after_pdf(self):
        """
        Exibe o interstitial de teste logo após a geração de um PDF.
        Não é chamado em nenhum outro ponto da interface, para não
        interromper o usuário a cada clique.
        """
        if self.kivmob and self._interstitial_ready:
            self.kivmob.show_interstitial()
            self._interstitial_ready = False
            # Pré-carrega o próximo interstitial para uso futuro.
            Clock.schedule_once(lambda dt: self.kivmob.request_interstitial(), 1)
