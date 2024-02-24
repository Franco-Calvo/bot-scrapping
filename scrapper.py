import requests
import time
import re
import os 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN') #COLOCAS EL TOKEN DE TU BOT OBTENIDO POR BOT_FATHER (Colóca tu TOKEN dentro de la variable de entorno)
chat_ids = os.getenv("CHAT_IDS").strip("[]").replace("'", "").split(",") # (Colóca tus ID's dentro de la variable de entorno, en un Array)
chat_id_logs = os.getenv('CHAT_ID_LOGS') #Puedes crear un grupo personalizado para recibir los logs e imágenes del error aquí (Colóca tu ID dentro de la variable de entorno)

ultimo_valor_compra = 'inicial'
ultimo_valor_venta = 'inicial'

def sendPhoto(chat_id, photo_path):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendPhoto'
    files = {'photo': open(photo_path, 'rb')}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    print(f"Foto enviada: {response.text}")

def sendMessage(chat_id, message):
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
    print(f"Mensaje enviado: {response.text}")

def get_dolar_blue_rate():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)
    driver.get('') #Colocas la URL del sitio web del que quieras extraer la cotización

    try:
        compra = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-14qlmbp"))).text #Reemplazan ".css" por el selector que contiene el texto que quieran extraer
        venta = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1i2k8fd"))).text  #Reemplazan ".css" por el selector que contiene el texto que quieran extraer
    except Exception as e:
        screenshot_path = 'screenshot_error.png'
        driver.save_screenshot(screenshot_path)
        sendPhoto(chat_id_logs, screenshot_path)
        print("Error cotización:", e)
        compra = "Error"
        venta = "Error"
    finally:
        driver.quit()

    return compra.strip(), venta.strip()

def cotizacion_es_valida(cotizacion):
    return bool(re.search(r'\d', cotizacion)) 

def run_bot():
    global ultimo_valor_compra, ultimo_valor_venta
    while True:
        valor_compra_actual, valor_venta_actual = get_dolar_blue_rate()
        if cotizacion_es_valida(valor_compra_actual) and cotizacion_es_valida(valor_venta_actual):
            simbolo_compra = "🟢" if valor_compra_actual > ultimo_valor_compra else "🔴"
            simbolo_venta = "🟢" if valor_venta_actual > ultimo_valor_venta else "🔴"
            if valor_compra_actual != ultimo_valor_compra or valor_venta_actual != ultimo_valor_venta: 
                mensaje_coti = f"Buenos Aires - Compra: {simbolo_compra} {valor_compra_actual}, Venta: {simbolo_venta} {valor_venta_actual}" #Colocas el mensaje que quieres que se envíe
                for chat_id in chat_ids:
                    sendMessage(chat_id, mensaje_coti)
                ultimo_valor_compra = valor_compra_actual
                ultimo_valor_venta = valor_venta_actual

        time.sleep(20) #Colocas el tiempo que quieres que espere para volver a buscar la cotización

if __name__ == "__main__":
    run_bot()