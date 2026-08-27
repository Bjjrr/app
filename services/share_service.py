"""
Salvamento em área pública e compartilhamento do PDF gerado.

Usa a biblioteca `androidstorage4kivy`, que trata corretamente o
Scoped Storage do Android 10+ e cuida do FileProvider necessário para
compartilhar arquivos com outros aplicativos (WhatsApp, Gmail,
Telegram, etc.), sem precisar editar manualmente o AndroidManifest.xml.
"""
from kivy.utils import platform


def save_to_public_storage(private_path):
    """
    Copia o PDF (gerado na pasta privada do app) para uma área pública
    de "Documentos", acessível pelo usuário fora do app (ex.: por um
    gerenciador de arquivos). Retorna o caminho/URI público resultante.
    """
    if platform != "android":
        # Em desktop, apenas devolve o caminho local para fins de teste.
        return private_path

    from androidstorage4kivy import SharedStorage

    shared = SharedStorage()
    public_uri = shared.copy_to_shared(private_path, collection="documents")
    return public_uri


def share_pdf(private_path):
    """
    Abre a caixa de diálogo nativa de compartilhamento do Android para
    o PDF informado (WhatsApp, Gmail, Telegram, etc., quando
    instalados no aparelho).
    """
    if platform != "android":
        print(f"[DEV] Compartilhamento simulado (não é Android): {private_path}")
        return

    from androidstorage4kivy import SharedStorage

    shared = SharedStorage()
    shared.share_file(private_path)
