"""Vista Kivy para el cálculo de hipoteca inversa."""

from __future__ import annotations

import sys
from pathlib import Path

_RAIZ_PROYECTO = Path(__file__).resolve().parents[3]
if str(_RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(_RAIZ_PROYECTO))

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

KV = """
PantallaHipoteca:

<PantallaHipoteca>:
    orientation: "vertical"
    padding: "20dp"

    Label:
        text: "Calculadora de Hipoteca Inversa"
        font_size: "22sp"
"""


class PantallaHipoteca(BoxLayout):
    """Pantalla principal (en construcción)."""


class HipotecaInversaApp(App):
    def build(self):
        Builder.load_string(KV)
        return PantallaHipoteca()


if __name__ == "__main__":
    HipotecaInversaApp().run()