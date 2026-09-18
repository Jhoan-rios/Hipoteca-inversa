# Hipoteca Inversa

Aplicación en Python para simular el cálculo de una **hipoteca inversa**, con interfaz de **consola** y de **escritorio (Kivy)**, siguiendo principios de código limpio y arquitectura por capas (Modelo - Vista - Controlador).

## Integrantes del equipo

| Nombre | GitHub |
|---|---|
| Jhoan Ríos | [@jhoan-rios](https://github.com/jhoan-rios) |
| Jose Berrio | [@JoseBerrioC](https://github.com/JoseBerrioC) |

## Estructura del proyecto

```
Hipoteca-inversa/
├── doc/
│   ├── EntrevistaJuanDavid.mp3      # Entrevista de levantamiento de requisitos
│   └── casos_de_prueba.xlsx         # Casos de prueba documentados
├── src/
│   ├── controller/
│   │   └── __init__.py              # Orquesta la comunicación entre view y model
│   ├── model/
│   │   ├── __init__.py
│   │   └── logica_hipoteca_inversa.py  # Lógica de negocio y cálculos financieros
│   └── view/
│       ├── __init__.py
│       ├── console.py                # Interfaz de consola (entrada/salida de datos)
│       └── gui/
│           ├── __init__.py
│           └── hipoteca_inversa_gui.py  # Interfaz gráfica de escritorio (Kivy)
├── tests/
│   ├── __init__.py
│   └── tests_hipoteca_inversa.py    # Pruebas unitarias de la lógica de negocio
├── .gitignore
├── LICENSE
└── README.md
```

### Descripción de la arquitectura

El proyecto sigue una separación de responsabilidades tipo **MVC**:

- **`model`**: contiene toda la lógica de cálculo de la hipoteca inversa (validaciones, fórmulas financieras, reglas de negocio y excepciones propias del dominio). No depende de cómo se muestren los datos.
- **`view`**: expone las interfaces de usuario — de consola (`console.py`) y gráfica (`gui/hipoteca_inversa_gui.py`) —, encargadas de solicitar datos al usuario y mostrar resultados. Ninguna de las dos contiene lógica de negocio.
- **`controller`**: actúa como intermediario entre `view` y `model`, coordinando el flujo de la aplicación sin mezclar responsabilidades de cálculo ni de presentación.
- **`tests`**: pruebas unitarias que validan el comportamiento de `model`, incluyendo casos válidos, casos límite y manejo de excepciones.
- **`doc`**: soporte documental del proyecto (entrevista de requisitos y casos de prueba).

## Funcionalidades

La lógica de negocio (`src/model/logica_hipoteca_inversa.py`) expone la función `desembolso_mensual(parametros)`, que calcula, usando la fórmula de anualidad financiera:

- **Cuota mensual**: el valor que el banco pagaría mensualmente al propietario.
- **Abonos totales**: la suma de todas las cuotas pagadas durante el plazo.
- **Intereses totales**: la diferencia entre los abonos totales y el valor financiado del inmueble.

Si la tasa mensual es `0`, el cálculo usa una división simple del valor financiado entre el número de meses, evitando la indeterminación de la fórmula de anualidad.

### Reglas de negocio y validaciones

La función valida los datos de entrada y lanza una excepción específica por cada regla incumplida:

| Excepción | Condición que la dispara |
|---|---|
| `ValorPropiedadCero` | El valor del inmueble es menor o igual a 0 |
| `HipotecaUsura` | La tasa mensual supera el 4% (límite de usura) |
| `PlazoMayorPermitido` | El plazo excede los 240 meses (20 años) |
| `PlazoMenorIgualCero` | El plazo es menor o igual a 0 meses |

### Interfaz gráfica (GUI)

La GUI (`src/view/gui/hipoteca_inversa_gui.py`), construida con **Kivy**, ofrece:

- Formulario con los 4 campos de entrada (valor del inmueble, porcentaje de desembolso, tasa mensual, plazo).
- Validación de formato con resaltado visual del campo con error y mensajes descriptivos.
- Manejo de las excepciones de negocio del modelo, mostrando el motivo exacto del rechazo.
- Botón **Calcular** (también disponible con la tecla Enter) y botón **Limpiar** para reiniciar el formulario.
- Resultado detallado: monto del préstamo, cuota mensual, total de abonos y total de intereses.

### Pruebas unitarias

`tests/tests_hipoteca_inversa.py` valida el comportamiento de `desembolso_mensual` con:

- 3 casos normales con distintos valores de inmueble, porcentaje, tasa y plazo.
- 3 casos extraordinarios: tasa mensual en cero, desembolso único a 1 mes con 100% de financiación, y plazo máximo permitido (240 meses).
- 4 casos de error, uno por cada excepción de negocio (`ValorPropiedadCero`, `HipotecaUsura`, `PlazoMenorIgualCero`, `PlazoMayorPermitido`).

## Requisitos

- Python 3.10 o superior
- Para la interfaz de consola: no se requieren dependencias externas (solo librería estándar)
- Para la interfaz gráfica: el paquete **Kivy**

Puedes verificar tu versión de Python con:

```bash
python --version
```

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/Jose-Dv/Hipoteca-inversa.git
```

### 2. Ubicarse en la carpeta del proyecto

```bash
cd Hipoteca-inversa
```

### 3. (Recomendado) Crear y activar un entorno virtual

```bash
python -m venv venv
```

En Windows:
```powershell
venv\Scripts\activate
```

En macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Ejecutar la interfaz de consola

```bash
python src/view/console.py
```

Esto iniciará la aplicación en modo consola, donde podrás ingresar los datos solicitados (valor del inmueble, porcentaje de financiación, tasa de interés mensual y plazo en meses) para obtener la cuota mensual, los abonos totales y los intereses totales de la hipoteca inversa.

### 5. Ejecutar la interfaz gráfica (GUI)

Primero instala Kivy dentro de tu entorno virtual:

```bash
pip install kivy
```

Luego, **desde la raíz del proyecto**, ejecuta la GUI como módulo:

```bash
python -m src.view.gui.hipoteca_inversa_gui
```

> **Nota:** ejecutar el archivo directamente (por ejemplo, dando clic en "Run" dentro de la carpeta `gui`) puede producir el error `ModuleNotFoundError: No module named 'src'`, ya que Python necesita ubicarse en la raíz del proyecto para resolver los imports internos (`from src.model import ...`). El comando anterior evita ese problema.

### 6. Ejecutar las pruebas unitarias

Desde la raíz del proyecto:

```bash
python -m unittest tests/tests_hipoteca_inversa.py
```

O bien, si prefieres ejecutar todas las pruebas del proyecto automáticamente:

```bash
python -m unittest discover -s tests
```

Un resultado exitoso mostrará algo similar a:

```
----------------------------------------------------------------------
Ran 10 tests in 0.00Xs

OK
```

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
