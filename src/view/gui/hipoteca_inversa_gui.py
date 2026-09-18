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
from kivy.uix.textinput import TextInput
from src.model.logica_hipoteca_inversa import ParametrosHipoteca

class CampoInvalido(Exception):
    """Error de FORMATO en un campo del formulario (no es un error de negocio)."""

    def __init__(self, nombre_campo: str, widget: TextInput) -> None:
        self.widget = widget
        super().__init__(
            f"El campo '{nombre_campo}' es obligatorio y debe ser numérico.")
        

KV = """
<CampoEntrada@BoxLayout>:
    orientation: "vertical"
    size_hint_y: None
    height: "64dp"
    etiqueta: ""
    texto_ayuda: ""

    Label:
        text: root.etiqueta
        size_hint_y: None
        height: "20dp"
        halign: "left"
        text_size: self.size
        color: 0.2, 0.2, 0.2, 1

    TextInput:
        id: entrada
        multiline: False
        input_filter: "float"
        hint_text: root.texto_ayuda


PantallaHipoteca:

<PantallaHipoteca>:
    valor_inmueble: campo_valor.ids.entrada
    porcentaje: campo_porcentaje.ids.entrada
    tasa: campo_tasa.ids.entrada
    plazo: campo_plazo.ids.entrada

    orientation: "vertical"
    padding: "20dp"
    spacing: "10dp"

    Label:
        text: "Calculadora de Hipoteca Inversa"
        font_size: "22sp"
        size_hint_y: None
        height: "44dp"
        bold: True

    CampoEntrada:
        id: campo_valor
        etiqueta: "Valor del inmueble ($)"
        texto_ayuda: "Ej: 300000000"

    CampoEntrada:
        id: campo_porcentaje
        etiqueta: "Porcentaje de desembolso (%)"
        texto_ayuda: "Ej: 60"

    CampoEntrada:
        id: campo_tasa
        etiqueta: "Tasa de interés mensual (%)"
        texto_ayuda: "Ej: 1.2 (máx. 4%)"

    CampoEntrada:
        id: campo_plazo
        etiqueta: "Plazo en meses"
        texto_ayuda: "Ej: 180 (máx. 240)"

    Button:
        text: "Calcular"
        size_hint_y: None
        height: "48dp"
        on_release: root.calcular()
"""


class PantallaHipoteca(BoxLayout):

    def calcular(self) -> None:
        try:
            parametros = self._leer_parametros()
        except CampoInvalido as error:
            print(error)  # se reemplazará por un mensaje en pantalla (commit 5)
            return
        print(parametros)  # verificación temporal, se reemplaza en el siguiente commit

    def _leer_parametros(self) -> ParametrosHipoteca:
        """Convierte el texto de los campos a `ParametrosHipoteca`.

        Raises:
            CampoInvalido: si algún campo está vacío o no es numérico.
        """
        valor_inmueble = self._leer_campo_numerico(
            self.valor_inmueble, "Valor del inmueble"
        )
        porcentaje = self._leer_campo_numerico(
            self.porcentaje, "Porcentaje de desembolso"
        ) / 100
        tasa_mensual = self._leer_campo_numerico(
            self.tasa, "Tasa de interés mensual"
        ) / 100
        plazo_meses = int(self._leer_campo_numerico(self.plazo, "Plazo en meses"))

        return ParametrosHipoteca(
            valor_inmueble=valor_inmueble,
            porcentaje=porcentaje,
            tasa_mensual=tasa_mensual,
            plazo_meses=plazo_meses,
        )

    @staticmethod
    def _leer_campo_numerico(campo: TextInput, nombre_visible: str) -> float:
        """Lee y convierte el texto de un campo a `float`.

        Raises:
            CampoInvalido: si el texto está vacío o no es un número.
        """
        try:
            return float(campo.text)
        except ValueError as error:
            raise CampoInvalido(nombre_visible, campo) from error
    def _leer_campo_numerico(campo: TextInput, nombre_visible: str) -> float:
        """Lee y convierte el texto de un campo a `float`.

        Raises:
            CampoInvalido: si el texto está vacío o no es un número.
        """
        try:
            return float(campo.text)
        except ValueError as error:
            raise CampoInvalido(nombre_visible, campo) from error


class HipotecaInversaApp(App):
    def build(self):
        Builder.load_string(KV)
        return PantallaHipoteca()


if __name__ == "__main__":
    HipotecaInversaApp().run()