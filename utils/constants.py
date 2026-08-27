"""
Constantes globais do aplicativo: cores, textos e IDs de anúncios.
"""

# ---------------------------------------------------------------------------
# CORES
# ---------------------------------------------------------------------------
COLOR_BACKGROUND = (0.96, 0.97, 0.98, 1)       # fundo claro
COLOR_PRIMARY = (0.13, 0.42, 0.87, 1)          # azul principal
COLOR_PRIMARY_DARK = (0.09, 0.32, 0.70, 1)
COLOR_SUCCESS = (0.18, 0.72, 0.46, 1)          # verde - ações de sucesso
COLOR_DANGER = (0.87, 0.22, 0.22, 1)           # vermelho - excluir
COLOR_CARD = (1, 1, 1, 1)
COLOR_TEXT_PRIMARY = (0.12, 0.14, 0.18, 1)
COLOR_TEXT_SECONDARY = (0.45, 0.48, 0.53, 1)

# ---------------------------------------------------------------------------
# APP
# ---------------------------------------------------------------------------
APP_NAME = "Imagem → PDF"
DEFAULT_PDF_NAME = "imagens_convertidas.pdf"
SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

# ---------------------------------------------------------------------------
# ADMOB — IDS DE TESTE OFICIAIS DO GOOGLE
# ---------------------------------------------------------------------------
# Os IDs abaixo são os IDs DE TESTE OFICIAIS publicados pelo Google
# (https://developers.google.com/admob/android/test-ads) e podem ser
# usados livremente durante o desenvolvimento, sem risco de bloqueio
# da conta AdMob.
#
# ANTES DE PUBLICAR O APP NA GOOGLE PLAY, troque os 3 valores abaixo
# pelos IDs REAIS gerados no seu painel do AdMob (https://apps.admob.com):
#
#   1) ADMOB_APP_ID            -> troque AQUI e também no buildozer.spec
#                                  (chave android.meta_data, veja o README)
#   2) BANNER_AD_UNIT_ID       -> troque AQUI
#   3) INTERSTITIAL_AD_UNIT_ID -> troque AQUI
#
# NUNCA use IDs reais durante testes/desenvolvimento: clicar nos
# próprios anúncios reais (mesmo sem querer) pode banir sua conta
# AdMob permanentemente.
# ---------------------------------------------------------------------------

ADMOB_APP_ID = "ca-app-pub-3940256099942544~3347511713"             # ID de teste (App)
BANNER_AD_UNIT_ID = "ca-app-pub-3940256099942544/6300978111"        # ID de teste (Banner)
INTERSTITIAL_AD_UNIT_ID = "ca-app-pub-3940256099942544/1033173712"  # ID de teste (Interstitial)
