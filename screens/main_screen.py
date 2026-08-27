"""
Tela principal do aplicativo "Imagem → PDF".

Responsável por orquestrar: seleção de imagens, reordenação, geração
do PDF em background (sem travar a interface) e compartilhamento.
"""
import os
import threading

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import mainthread
from kivy.utils import platform
from kivy.app import App

from services.image_picker_service import pick_images
from services.pdf_service import images_to_pdf, unique_output_path, PdfGenerationError
from services.share_service import save_to_public_storage, share_pdf
from utils.constants import DEFAULT_PDF_NAME, COLOR_SUCCESS


class MainScreen(BoxLayout):
    def __init__(self, ads_service=None, **kwargs):
        super().__init__(**kwargs)
        self.ads_service = ads_service
        self.image_paths = []      # lista ordenada dos caminhos selecionados
        self.last_pdf_path = None
        self._processing_popup = None
        self._refresh_image_list()

    # ------------------------------------------------------------------
    # Seleção de imagens
    # ------------------------------------------------------------------
    def add_images(self):
        pick_images(self._on_images_picked)

    @mainthread
    def _on_images_picked(self, paths):
        if not paths:
            return
        self.image_paths.extend(paths)
        self._refresh_image_list()

    def clear_all(self):
        self.image_paths = []
        self._refresh_image_list()

    def remove_image(self, path):
        if path in self.image_paths:
            self.image_paths.remove(path)
            self._refresh_image_list()

    def move_image(self, path, direction):
        """Reordena a lista. direction: -1 (subir) ou +1 (descer)."""
        if path not in self.image_paths:
            return
        idx = self.image_paths.index(path)
        new_idx = idx + direction
        if 0 <= new_idx < len(self.image_paths):
            self.image_paths[idx], self.image_paths[new_idx] = (
                self.image_paths[new_idx],
                self.image_paths[idx],
            )
            self._refresh_image_list()

    def _refresh_image_list(self):
        container = self.ids.image_list
        container.clear_widgets()

        from widgets.image_card import ImageCard

        for path in self.image_paths:
            card = ImageCard(
                image_path=path,
                image_name=os.path.basename(path),
                on_remove=self.remove_image,
            )
            card.ids.up_btn.bind(on_release=lambda *_a, p=path: self.move_image(p, -1))
            card.ids.down_btn.bind(on_release=lambda *_a, p=path: self.move_image(p, 1))
            container.add_widget(card)

        total = len(self.image_paths)
        self.ids.count_label.text = f"{total} imagem(ns) selecionada(s)"
        self.ids.generate_btn.disabled = total == 0
        self.ids.clear_btn.disabled = total == 0

    # ------------------------------------------------------------------
    # Geração do PDF
    # ------------------------------------------------------------------
    def generate_pdf(self):
        if not self.image_paths:
            return
        self._show_processing_popup()
        threading.Thread(target=self._generate_pdf_worker, daemon=True).start()

    def _generate_pdf_worker(self):
        try:
            app_dir = App.get_running_app().user_data_dir
            output_path = unique_output_path(app_dir, DEFAULT_PDF_NAME)
            images_to_pdf(list(self.image_paths), output_path)
            public_path = save_to_public_storage(output_path)
            self._on_pdf_success(output_path, public_path)
        except PdfGenerationError as exc:
            self._on_pdf_error(str(exc))
        except Exception as exc:  # noqa: BLE001
            self._on_pdf_error(f"Erro inesperado: {exc}")

    @mainthread
    def _show_processing_popup(self):
        content = BoxLayout(orientation="vertical", spacing=12, padding=20)
        content.add_widget(Label(text="Gerando PDF, aguarde..."))
        content.add_widget(ProgressBar(max=100, value=50))
        self._processing_popup = Popup(
            title="Processando",
            content=content,
            size_hint=(0.8, 0.35),
            auto_dismiss=False,
        )
        self._processing_popup.open()

    @mainthread
    def _on_pdf_success(self, private_path, public_path):
        if self._processing_popup:
            self._processing_popup.dismiss()
        self.last_pdf_path = private_path

        location_text = public_path if platform == "android" else private_path

        content = BoxLayout(orientation="vertical", spacing=12, padding=20)
        content.add_widget(Label(text="PDF gerado com sucesso!", bold=True))
        content.add_widget(
            Label(text=f"Local:\n{location_text}", halign="center", valign="middle")
        )

        from widgets.rounded_button import RoundedButton

        share_btn = RoundedButton(
            text="Compartilhar PDF",
            bg_color=COLOR_SUCCESS,
            size_hint_y=None,
            height=48,
        )
        content.add_widget(share_btn)

        popup = Popup(title="Sucesso", content=content, size_hint=(0.85, 0.55))
        share_btn.bind(on_release=lambda *_a: (popup.dismiss(), share_pdf(private_path)))
        popup.open()

        if self.ads_service:
            self.ads_service.show_interstitial_after_pdf()

    @mainthread
    def _on_pdf_error(self, message):
        if self._processing_popup:
            self._processing_popup.dismiss()
        content = BoxLayout(orientation="vertical", spacing=12, padding=20)
        content.add_widget(Label(text=message, halign="center", valign="middle"))
        Popup(title="Erro ao gerar PDF", content=content, size_hint=(0.85, 0.35)).open()
