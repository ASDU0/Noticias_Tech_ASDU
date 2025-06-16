from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback
import os
import subprocess
import pyautogui

# -------------------------------
# 1️⃣ Función para iniciar Chrome
# -------------------------------
def iniciar_chrome():
    ruta = ChromeDriverManager().install()

    options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--window-size=1000,1000")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    options.add_argument("--disable-blink-features=AutomationControlled")
    exp_opt = [
        'enable-automation',
        'ignore-certificate-errors',
        'enable-logging'
    ]
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "intl.accept_languages": ["es-ES", "es"],
        "credentials_enable_service": False
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", exp_opt)

    s = Service(ruta)
    driver = webdriver.Chrome(service=s, options=options)
    return driver

# -----------------------------------------------
# 2️⃣ Función para enviar mensaje con imagen
# -----------------------------------------------
def enviar_mensaje_whatsapp(nombre_chat, titulo, descripcion, autor, fecha, url, ruta_imagen):
    whatsapp_url = "https://web.whatsapp.com/"
    driver = iniciar_chrome()
    driver.get(whatsapp_url)

    try:
        wait = WebDriverWait(driver, 60)

        # Esperar la caja de búsqueda
        search_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        ))
        print(" QR escaneado. Buscando chat...")

        # Buscar el chat
        search_box.click()
        search_box.send_keys(nombre_chat)
        search_box.send_keys(Keys.ENTER)
        print(f" Chat '{nombre_chat}' abierto.")

        # Esperar la caja de texto para mensajes
        input_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]')
        ))

        # Preparar el mensaje estructurado
        mensaje = f"""*{titulo}*
{descripcion}

Autor: {autor}
Fecha: {fecha}
URL: {url}
"""

        #  Enviar el mensaje de texto
        input_box.click()
        input_box.clear()
        for linea in mensaje.split("\n"):
            input_box.send_keys(linea)
            input_box.send_keys(Keys.SHIFT + Keys.ENTER)
        input_box.send_keys(Keys.ENTER)
        print(" Mensaje de texto enviado.")

        #  Enviar la imagen en un mensaje nuevo
        if ruta_imagen and os.path.exists(ruta_imagen):
            # Copiar imagen al portapapeles
            ruta_abs = os.path.abspath(ruta_imagen)
            comando = f'powershell -command "Add-Type -AssemblyName System.Windows.Forms; ' \
                       f'[Windows.Forms.Clipboard]::SetImage([Drawing.Image]::FromFile(\\\"{ruta_abs}\\\"))"'
            subprocess.run(comando, shell=True)
            time.sleep(1)

            # Hacer clic en la caja de texto (para un nuevo mensaje)
            input_box = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]')
            ))
            input_box.click()
            time.sleep(1)

            # Pegar la imagen
            pyautogui.hotkey("ctrl", "v")
            print(" Imagen pegada en el chat.")
            time.sleep(3)  # espera a que se cargue la vista previa

            # Enviar la imagen (Enter)
            pyautogui.press("enter")
            print(" Imagen enviada con éxito.")
        else:
            print("⚠️ No se encontró la ruta de la imagen o no existe.")

    except Exception as e:
        print(" Ocurrió un error:")
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        time.sleep(60)
        driver.quit()






