from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from src.model.logica_hipoteca_inversa import (
    ParametrosHipoteca,
    HipotecaInversaError,
    desembolso_mensual,
    calcular_monto_prestamo,
)

Window.size = (480, 520)

TITULO_ERROR_VALIDACION = "Error de validación"
TITULO_ERROR_DATOS = "Datos inválidos"
TITULO_ERROR_INESPERADO = "Error inesperado"


class HipotecaInversaApp(App):
    title = "Hipoteca Inversa"

    def build(self) -> BoxLayout:
        raiz = BoxLayout(orientation="vertical", padding=20, spacing=15)

        encabezado = BoxLayout(orientation="horizontal", size_hint=(1, 0.13))

        titulo = Label(
            text="HIPOTECA INVERSA",
            font_size=20,
            bold=True,
            halign="left",
            valign="middle",
            size_hint=(0.6, 1),
        )
        self._ajustar_texto(titulo)

        instruccion = Label(
            text="Ingresa los datos a continuación:",
            font_size=14,
            halign="left",
            valign="middle",
            size_hint=(0.4, 1),
        )
        self._ajustar_texto(instruccion)

        encabezado.add_widget(titulo)
        encabezado.add_widget(instruccion)
        raiz.add_widget(encabezado)

        formulario = GridLayout(cols=2, spacing=10, size_hint=(1, 0.45))

        self.input_valor_inmueble = self._agregar_campo(formulario, "Valor del inmueble:")
        self.input_porcentaje = self._agregar_campo(formulario, "Porcentaje a prestar (0-1):")
        self.input_tasa_mensual = self._agregar_campo(formulario, "Tasa mensual (0-1):")
        self.input_plazo_meses = self._agregar_campo(formulario, "Plazo (meses):")

        raiz.add_widget(formulario)

        resultados = GridLayout(cols=2, spacing=10, size_hint=(1, 0.3))

        resultados.add_widget(Label(text="Monto del préstamo:", bold=True))
        self.label_monto_prestamo = Label(text="$ 0.00")
        resultados.add_widget(self.label_monto_prestamo)

        resultados.add_widget(Label(text="Cuota mensual:", bold=True))
        self.label_cuota = Label(text="$ 0.00")
        resultados.add_widget(self.label_cuota)

        resultados.add_widget(Label(text="Total abonos:", bold=True))
        self.label_total_abonos = Label(text="$ 0.00")
        resultados.add_widget(self.label_total_abonos)

        resultados.add_widget(Label(text="Total intereses:", bold=True))
        self.label_total_intereses = Label(text="$ 0.00")
        resultados.add_widget(self.label_total_intereses)

        raiz.add_widget(resultados)

        botones = BoxLayout(orientation="horizontal", size_hint=(1, 0.12), spacing=10)

        boton_calcular = Button(text="Calcular")
        boton_calcular.bind(on_press=self.calcular)
        botones.add_widget(boton_calcular)

        boton_limpiar = Button(text="Limpiar")
        boton_limpiar.bind(on_press=self.limpiar)
        botones.add_widget(boton_limpiar)

        raiz.add_widget(botones)

        return raiz

    @staticmethod
    def _ajustar_texto(label: Label) -> None:
        """
        Ajusta 'text_size' al tamaño real del widget cada vez que este
        cambia de tamaño, para que 'halign'/'valign' funcionen como
        se espera (Kivy centra el texto dentro de una caja del tamaño
        del texto por defecto, no del widget).
        """
        label.bind(size=lambda widget, tam: setattr(widget, "text_size", tam))

    @staticmethod
    def _agregar_campo(contenedor: GridLayout, texto: str) -> TextInput:
        contenedor.add_widget(Label(text=texto))
        campo = TextInput(multiline=False, font_size=18)
        contenedor.add_widget(campo)
        return campo

    def calcular(self, instance: Button) -> None:
        try:
            parametros = self._leer_datos()
            monto_prestamo = calcular_monto_prestamo(parametros)
            cuota, total_abonos, total_intereses = desembolso_mensual(parametros)
            self._mostrar_resultado(monto_prestamo, cuota, total_abonos, total_intereses)

        except HipotecaInversaError as error:
            self._mostrar_error(TITULO_ERROR_VALIDACION, str(error))

        except ValueError as error:
            mensaje = (
                f"Qué sucedió: no fue posible interpretar un valor ingresado ({error}).\n"
                "Por qué: uno o más campos están vacíos o contienen texto no numérico.\n"
                "Dónde: formulario de Hipoteca Inversa.\n"
                "Cómo se soluciona: ingrese solo números en todos los campos "
                "(use punto para los decimales y no deje campos vacíos)."
            )
            self._mostrar_error(TITULO_ERROR_DATOS, mensaje)

        except Exception as error:
            mensaje = (
                f"Qué sucedió: ocurrió un error inesperado ({error}).\n"
                "Por qué: no se identificó una causa específica dentro de la aplicación.\n"
                "Dónde: Hipoteca Inversa (interfaz gráfica).\n"
                "Cómo se soluciona: verifique los datos ingresados e intente "
                "nuevamente; si el error persiste, reporte el detalle al desarrollador."
            )
            self._mostrar_error(TITULO_ERROR_INESPERADO, mensaje)

    def limpiar(self, instance: Button) -> None:
        self.input_valor_inmueble.text = ""
        self.input_porcentaje.text = ""
        self.input_tasa_mensual.text = ""
        self.input_plazo_meses.text = ""
        self.label_monto_prestamo.text = "$ 0.00"
        self.label_cuota.text = "$ 0.00"
        self.label_total_abonos.text = "$ 0.00"
        self.label_total_intereses.text = "$ 0.00"

    def _leer_datos(self) -> ParametrosHipoteca:
        valor_inmueble = float(self.input_valor_inmueble.text)
        porcentaje = float(self.input_porcentaje.text)
        tasa_mensual = float(self.input_tasa_mensual.text)
        plazo_meses = int(float(self.input_plazo_meses.text))

        return ParametrosHipoteca(
            valor_inmueble=valor_inmueble,
            porcentaje=porcentaje,
            tasa_mensual=tasa_mensual,
            plazo_meses=plazo_meses,
        )

    def _mostrar_resultado(
        self, monto_prestamo: float, cuota: float, total_abonos: float, total_intereses: float
    ) -> None:
        self.label_monto_prestamo.text = f"$ {monto_prestamo:,.2f}"
        self.label_cuota.text = f"$ {cuota:,.2f}"
        self.label_total_abonos.text = f"$ {total_abonos:,.2f}"
        self.label_total_intereses.text = f"$ {total_intereses:,.2f}"

    def _mostrar_error(self, titulo: str, mensaje: str) -> None:
        contenido = BoxLayout(orientation="vertical", padding=10, spacing=10)

        etiqueta = Label(text=mensaje, halign="left", valign="top")
        self._ajustar_texto(etiqueta)
        contenido.add_widget(etiqueta)

        boton_cerrar = Button(text="Cerrar", size_hint=(1, 0.25))
        contenido.add_widget(boton_cerrar)

        popup = Popup(title=titulo, content=contenido, size_hint=(0.85, 0.6))
        boton_cerrar.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    HipotecaInversaApp().run()