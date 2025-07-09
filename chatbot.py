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
# 1️⃣ Iniciar Chrome
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

    exp_opt = ['enable-automation', 'ignore-certificate-errors', 'enable-logging']
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
# 2️⃣ Enviar mensaje con imagen
# -----------------------------------------------
def enviar_mensaje_whatsapp(nombre_chat, titulo, descripcion, autor, fecha, url, ruta_imagen):
    whatsapp_url = "https://web.whatsapp.com/"
    driver = iniciar_chrome()
    driver.get(whatsapp_url)

    try:
        wait = WebDriverWait(driver, 60)

        # ✅ Esperar escaneo del QR
        print("📷 Esperando que se escanee el QR de WhatsApp Web...")
        search_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        ))
        print("✅ QR escaneado. Esperando que cierres manualmente cualquier anuncio que aparezca...")
        print("⏳ Tienes 15 segundos para cerrar el popup si aparece.\n")
        time.sleep(15)  # Espera para cerrar anuncios manuales

        # 🔍 Buscar el chat
        search_box.click()
        search_box.send_keys(nombre_chat)
        search_box.send_keys(Keys.ENTER)
        print(f"💬 Chat '{nombre_chat}' abierto.")

        # ✍️ Esperar la caja de texto para mensajes
        input_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]')
        ))

        # 📝 Preparar y enviar mensaje
        mensaje = f"""*{titulo}*
{descripcion}

Autor: {autor}
Fecha: {fecha}
URL: {url}
"""

        input_box.click()
        input_box.clear()
        for linea in mensaje.split("\n"):
            input_box.send_keys(linea)
            input_box.send_keys(Keys.SHIFT + Keys.ENTER)
        input_box.send_keys(Keys.ENTER)
        print("✅ Mensaje de texto enviado.")

        # 📷 Enviar imagen si existe
        if ruta_imagen and os.path.exists(ruta_imagen):
            ruta_abs = os.path.abspath(ruta_imagen)
            comando = f'powershell -command "Add-Type -AssemblyName System.Windows.Forms; ' \
                      f'[Windows.Forms.Clipboard]::SetImage([Drawing.Image]::FromFile(\\\"{ruta_abs}\\\"))"'
            subprocess.run(comando, shell=True)
            time.sleep(1)

            input_box.click()
            time.sleep(1)
            pyautogui.hotkey("ctrl", "v")
            print("🖼 Imagen pegada en el chat.")
            time.sleep(3)
            pyautogui.press("enter")
            print("✅ Imagen enviada con éxito.")
        else:
            print("⚠️ No se encontró la imagen o no existe.")

    except Exception as e:
        print("❌ Ocurrió un error:")
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        print("🕐 Esperando 60 segundos antes de cerrar...")
        time.sleep(60)
        driver.quit()

# -----------------------------------------------
# 💡 Ejemplo de uso:
# -----------------------------------------------
# enviar_mensaje_whatsapp(
#     nombre_chat="Grupo de Noticias",
#     titulo="Novedades de la semana",
#     descripcion="Ya está disponible la nueva función de IA que resume documentos automáticamente.",
#     autor="ChatGPT News Bot",
#     fecha="2025-07-09",
#     url="https://ejemplo.com/novedades-ia",
#     ruta_imagen="noticia.jpg"
# )
