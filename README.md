# Hipoteca Inversa

Aplicación de consola en Python para simular el cálculo de una **hipoteca inversa**, siguiendo principios de código limpio y arquitectura por capas (Modelo - Vista - Controlador).

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
│       └── console.py               # Interfaz de consola (entrada/salida de datos)
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
- **`view`**: expone la interfaz de consola (`console.py`), encargada de solicitar datos al usuario y mostrar resultados. No contiene lógica de negocio.
- **`controller`**: actúa como intermediario entre `view` y `model`, coordinando el flujo de la aplicación sin mezclar responsabilidades de cálculo ni de presentación.
- **`tests`**: pruebas unitarias que validan el comportamiento de `model`, incluyendo casos válidos, casos límite y manejo de excepciones.
- **`doc`**: soporte documental del proyecto (entrevista de requisitos y casos de prueba).

## Funcionalidades

La lógica de negocio (`src/model/logica_hipoteca_inversa.py`) expone la función `desembolso_mensual(valor_inmueble, porcentaje, tasa_mensual, plazo_meses)`, que calcula, usando la fórmula de anualidad financiera:

- **Cuota mensual**: el valor que el banco pagaría mensualmente al propietario.
- **Abonos totales**: la suma de todas las cuotas pagadas durante el plazo.
- **Intereses totales**: la diferencia entre los abonos totales y el valor financiado del inmueble.

Si la tasa mensual es `0`, el cálculo usa una división simple del valor financiado entre el número de meses, evitando la indeterminación de la fórmula de anualidad.

### Reglas de negocio y validaciones

La función valida los datos de entrada y lanza una excepción específica por cada regla incumplida:

| Excepción | Condición que la dispara |
|---|---|
| `ValorPropiedad0` | El valor del inmueble es menor o igual a 0 |
| `HipotecaUsura` | La tasa mensual supera el 4% (límite de usura) |
| `PlazoMayor240` | El plazo excede los 240 meses (20 años) |
| `PlazoMenorIgual0` | El plazo es menor o igual a 0 meses |

### Pruebas unitarias

`tests/tests_hipoteca_inversa.py` valida el comportamiento de `desembolso_mensual` con:

- 3 casos normales con distintos valores de inmueble, porcentaje, tasa y plazo.
- 3 casos extraordinarios: tasa mensual en cero, desembolso único a 1 mes con 100% de financiación, y plazo máximo permitido (240 meses).
- 4 casos de error, uno por cada excepción de negocio (`ValorPropiedad0`, `HipotecaUsura`, `PlazoMenorIgual0`, `PlazoMayor240`).

## Requisitos

- Python 3.10 o superior
- No se requieren dependencias externas (usa únicamente la librería estándar de Python)

Puedes verificar tu versión de Python con:

```bash
python --version
```
## Integrantes

- Juan Sebastián Leal Suárez

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/Dokifobia/Hipoteca-inversa.git
cd Hipoteca-inversa
```

### 2. Instalar dependencias

```bash
pip install "kivy[base]"
pip install --user kivy
```

### 3. Ejecutar la interfaz de consola

```bash
python -m src.view.console
```

### 4. Ejecutar la interfaz gráfica (Kivy)

```bash
python -m src.view.gui
```

### 5. Ejecutar las pruebas unitarias

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