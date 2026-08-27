"""
Serviço responsável por converter uma lista de imagens em um único
arquivo PDF, inteiramente no dispositivo (sem internet e sem APIs
externas). Baseado em Pillow.
"""
import os
from PIL import Image


class PdfGenerationError(Exception):
    """Erro ao gerar o PDF a partir das imagens."""


def images_to_pdf(image_paths, output_path):
    """
    Converte `image_paths` (na ordem desejada) em um único PDF salvo
    em `output_path`.

    - Uma imagem por página.
    - Fundo branco (imagens com transparência, ex.: PNG, são
      compostas sobre um fundo branco antes de entrar no PDF).
    - Boa qualidade, sem recompressão agressiva.
    """
    if not image_paths:
        raise PdfGenerationError("Nenhuma imagem foi selecionada.")

    pages = []
    try:
        for path in image_paths:
            if not os.path.exists(path):
                raise PdfGenerationError(f"Arquivo não encontrado: {path}")
            img = Image.open(path)
            img.load()
            pages.append(_flatten_to_white_background(img))

        first, rest = pages[0], pages[1:]
        first.save(
            output_path,
            "PDF",
            resolution=150.0,
            save_all=True,
            append_images=rest,
        )
    except PdfGenerationError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise PdfGenerationError(f"Falha ao gerar o PDF: {exc}") from exc
    finally:
        for page in pages:
            try:
                page.close()
            except Exception:
                pass

    return output_path


def _flatten_to_white_background(img):
    """
    Garante fundo branco (necessário para PNG/WEBP com canal alpha) e
    modo RGB, adequado para exportação em PDF.
    """
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        img = img.convert("RGBA")
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])  # canal alpha como máscara
        return background

    if img.mode != "RGB":
        return img.convert("RGB")

    return img


def unique_output_path(directory, base_name="imagens_convertidas.pdf"):
    """
    Retorna um caminho de arquivo que não colide com um já existente,
    adicionando um sufixo numérico (ex.: "arquivo (1).pdf") quando
    necessário.
    """
    os.makedirs(directory, exist_ok=True)
    name, ext = os.path.splitext(base_name)
    candidate = os.path.join(directory, base_name)
    counter = 1
    while os.path.exists(candidate):
        candidate = os.path.join(directory, f"{name} ({counter}){ext}")
        counter += 1
    return candidate
