# BOT COTIZACIONES TELEGRAM

Bot de telegram en [python](https://www.python.org/) para hacer web scrapping y extraer las cotizaciones compra/venta del dólar blue.

## Instalación

Ejecuta el siguiente comando para instalar todas las dependencias necesarias: [pip](https://pip.pypa.io/en/stable/) para el bot.

```bash
pip install requests selenium webdriver_manager python-dotenv
```

## Configuración de Variables de Entorno:

Crea un archivo .env en la raíz del proyecto.
Agrega las siguientes variables al archivo .env:

```bash
TELEGRAM_BOT_TOKEN=
CHAT_IDS=
CHAT_ID_LOGS=
```

## Ejecutar el script con el siguiente comando

```bash
python nombre_de_tu_script.py
```

El bot iniciará y comenzará a enviar actualizaciones de cotización a los IDs de chat configurados

## Funciones principales

sendPhoto (): Envía una foto al chat especificado. Utilizado para enviar capturas de pantalla en caso de errores en el scraping.

sendMessage(): Envía un mensaje de texto al chat especificado.

get_dolar_blue_rate(): Realiza el scraping para obtener las cotizaciones de compra y venta del dólar blue.

cotizacion_es_valida(): Verifica si la cotización obtenida es válida.
