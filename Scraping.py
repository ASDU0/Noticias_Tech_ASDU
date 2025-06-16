# Para instalar automáticamente chromedriver
from webdriver_manager.chrome import ChromeDriverManager
# Driver de Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# Para modificar las opciones de webdriver en Chrome
from selenium.webdriver.chrome.options import Options
#para definir el tipo de busqueda del elemento
from selenium.webdriver.common.by import By
import urllib.request
import os


def iniciar_chrome():
    """Inicia Chrome con los parámetros indicados y devuelve el driver."""

    # Instalamos la versión de chromedriver correspondiente
    ruta = ChromeDriverManager().install()

    # OPCIONES de CHROME
    options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}") 

    # Configuraciones de la ventana
    options.add_argument("--window-size=1000,1000")
    options.add_argument("--start-maximized")

    # Seguridad y rendimiento
    options.add_argument("--headless")
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
    #PARAMETROS A OMITIR EN EL INICIO DE CHROMEDRIVER
    exp_opt=[
        'enable-automation', #para que no muestre la notificacion "Un software esta automatizando de prubas esat controlado por Chrome"
        'ignore-certificate-errors', #para ignorar errores de certificados (a veces estan caducados)
        'enable-logging' #para que no se muestre en la terminal "Devtools listening on..."
    ]

    #PARAMETROS QUE DEFINENEN PREFERENCIAS EN CHROMEDRIVER
    prefs={
        "profile.default_content_setting_values.notifications" : 2,#notificaciones: 0=preguntar | 1=permitir | 2=no permitir
        "intl.accpet_languages": ["es-ES","es"],
        "credentials_enable_service": False #para evitar que Chrome nos pregunte su queremos guardar la contraseña al loguearnos
    }
    options.add_experimental_option("prefs",prefs)
    options.add_experimental_option("excludeSwitches",exp_opt)


    # Instanciamos el servicio de chromedriver
    s = Service(ruta)

    # Instanciamos webdriver de selenium con Chrome
    driver = webdriver.Chrome(service=s, options=options)

    # Devolvemos el driver
    return driver

def obtener_datos(driver,url):
    driver.get(url)
    titulos=driver.find_elements(By.CSS_SELECTOR,"h2.abstract-title")
    urls=driver.find_elements(By.CSS_SELECTOR,"a.abstract-link-more")
    descripciones=driver.find_elements(By.CSS_SELECTOR,"div.abstract-excerpt")
    autores=driver.find_elements(By.CSS_SELECTOR,"footer.abstract-byline")
    fechas=driver.find_elements(By.CSS_SELECTOR,"time.abstract-date")
    url_imagen=driver.find_elements(By.CSS_SELECTOR,"div.base-asset-image")

    A=[]
    Titulos=[]
    for t in titulos:
        Titulos.append(t.text)
    
    Urls=[]
    for u in urls:
        Urls.append(u.get_attribute("href"))

    Descripciones=[]
    for d in descripciones:
        Descripciones.append(d.text)
    

    Autores=[]
    for a in autores:
        try:
            Autores.append(a.find_element(By.CSS_SELECTOR, "a.abstract-author").text)
            
        except:
            Autores.append("No encontrado")


    Fechas=[]
    for f in fechas:
        Fechas.append(f.get_attribute("datetime"))

    Url_Imagenes=[]
    for ui in url_imagen:
        img_tag = ui.find_element(By.TAG_NAME, "img")
        Url_Imagenes.append(img_tag.get_attribute("src"))

    import os.path

#Devuelve el contenido de una URL en formato bytesa
    def get_file(url):
        req=urllib.request.urlopen(url)
        html=req.read()
        return html

    AuxI=[]
    for idx, i in enumerate(Url_Imagenes):
        # Generamos un nombre de archivo único usando el índice
        nombre_archivo = f"{idx}_{os.path.basename(i)}"
        AuxI.append(nombre_archivo)
        with open(nombre_archivo, "wb") as f:
            f.write(get_file(i))

    A.append(Titulos)
    A.append(Urls)
    A.append(Descripciones)
    A.append(Autores)
    A.append(Fechas)
    A.append(AuxI)
    
    return A


# MAIN #####################################
if __name__ == '__main__':
    
    driver = iniciar_chrome()
    url="https://www.genbeta.com/"
    B=obtener_datos(driver,url)

    for i in B:
        print("============================")
        for j in i:
            print("--------------")
            print(j)
            print("--------------")
        print("============================")


    


    #Eliminar archivos
    '''archivos = [
    "0_200_200.png", "1_200_200.png", "2_200_200.jpeg", "3_200_200.jpeg",
    "4_200_200.jpeg", "5_200_200.jpeg", "6_original.jpeg", "7_200_200.png",
    "8_200_200.jpeg", "9_200_200.jpeg", "10_200_200.jpeg", "11_200_200.jpeg",
    "12_200_200.jpeg", "13_200_200.png", "14_200_200.jpeg", "15_200_200.jpeg"
    ]

    for archivo in archivos:
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f"Archivo eliminado: {archivo}")
        else:
            print(f"No existe: {archivo}")

    print("Todos los archivos eliminados.")'''
    
        
    driver.quit()