import sys
from PyQt6.QtWidgets import( QApplication, QWidget, QLabel,
                            QPushButton, QLineEdit, QVBoxLayout, 
                            QHBoxLayout, QTextEdit,QGraphicsDropShadowEffect,QMessageBox)

from PyQt6.QtGui import QFont,QColor,QPixmap
from PyQt6.QtCore import Qt

import Scraping
import chatbot


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.InicializarUI()
    
    def InicializarUI(self):
        self.setGeometry(230,100,1100,700) #(ubicacion, tamaño)
        self.setWindowTitle("NOTITECH") #Titulo noticia
        self.setStyleSheet("background-color: #91da47") #Color de la ventana
        self.generate_Window()#funcion que muestra los elementos de la ventana
        self.show()# funcion para mostrar la ventana
    


    #def presionar_boton_anterior():

    def generate_Window(self):


        def presionar_boton_start():
            driver = Scraping.iniciar_chrome()
            url="https://www.genbeta.com/"
            self.A=Scraping.obtener_datos(driver,url)
            QMessageBox.information(self, "Proceso finalizado", "Recolección de datos finalizado")

        self.contador=-1

        def presionar_boton_siguiente():
            if not self.A:
                return

            # Avanza el contador circularmente hacia adelante
            self.contador = (self.contador + 1) % len(self.A[0]) 
            
    
            OutputTituloNoticia.setText(str(self.A[0][self.contador]))
            OutputLinkNoticia.setText(str(self.A[1][self.contador]))
            OutputDescripcionNoticia.setText(str(self.A[2][self.contador]))
            OutputAutorNoticia.setText(str(self.A[3][self.contador]))
            OutputFechaNoticia.setText(str(self.A[4][self.contador]))
            imagen_texto="C:/Users/Jose/Desktop/NOTITECH/"+self.A[5][self.contador]
            pixmap = QPixmap(imagen_texto)
            LabelImagenNoticia.setPixmap(pixmap)

        def presionar_boton_anterior():
            if not self.A:
                return

            # Avanza el contador circularmente hacia adelante
            self.contador = (self.contador - 1) % len(self.A[0])

            OutputTituloNoticia.setText(str(self.A[0][self.contador]))
            OutputLinkNoticia.setText(str(self.A[1][self.contador]))
            OutputDescripcionNoticia.setText(str(self.A[2][self.contador]))
            OutputAutorNoticia.setText(str(self.A[3][self.contador]))
            OutputFechaNoticia.setText(str(self.A[4][self.contador]))
            imagen_texto="C:/Users/Jose/Desktop/NOTITECH/"+self.A[5][self.contador]
            pixmap = QPixmap(imagen_texto)
            LabelImagenNoticia.setPixmap(pixmap)
            LabelImagenNoticia.setScaledContents(True)
        
        def presionar_boton_subir():
            if not self.A:
                return

            nombre_chat = "Plageo"
            titulo = str(self.A[0][self.contador])
            descripcion = str(self.A[2][self.contador])
            autor = str(self.A[3][self.contador])
            fecha = str(self.A[4][self.contador])
            url = str(self.A[1][self.contador])
            ruta_imagen = "C:/Users/Jose/Desktop/NOTITECH/"+self.A[5][self.contador]

            chatbot.enviar_mensaje_whatsapp(nombre_chat, titulo, descripcion, autor, fecha, url, ruta_imagen)

        #-----Creamos todod los elementos de la UI------
        
        #===Elementos de Cabecera
        TituloApp=QLabel("Noticias Tech")
        TituloApp.setFont(QFont("Verdana", 28, QFont.Weight.Bold))
        # Crear sombra simulando efecto 3D
        sombra = QGraphicsDropShadowEffect()
        sombra.setOffset(3, 3)           # Desplazamiento de la sombra
        sombra.setBlurRadius(4)          # Suavizado de bordes
        sombra.setColor(QColor("black")) # Color de la sombra
        TituloApp.setGraphicsEffect(sombra)
        TituloApp.setStyleSheet("color: #2c3e50;")
        TituloApp.setStyleSheet("""
            border: 2px solid Blue;
            color: Brown;
            background-color: white;
        """)


        LogoASDU=QLabel("LOGO ASDU")
        LogoASDU.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        LogoASDU.setStyleSheet("color: #e74c3c;")  # Texto rojo

        #======Elementos del Cuerpo
        #=========Elemento de Titulo Noticia
        LabelTituloNoticia=QLabel("Titulo")
        LabelTituloNoticia.setFont(QFont("Verdana", 15, QFont.Weight.Bold))
        LabelTituloNoticia.setStyleSheet("color: #000000;border: none;")

        #=========Elementos de App Noticia
        #============Elemnto de Imagen
        OutputTituloNoticia=QTextEdit()
        OutputTituloNoticia.setFontPointSize(13)
        OutputTituloNoticia.setStyleSheet("background-color: #FFFFFF;color: #000000;")
        

        LabelImagenNoticia=QLabel()
        LabelImagenNoticia.setStyleSheet("background-color: #FFFFFF;")
        

        LabelImagenNoticia.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #============Elementos de Datos Noticia
        LabelLinkNoticia=QLabel("Link")
        LabelLinkNoticia.setFont(QFont("Verdana", 15, QFont.Weight.Bold))
        LabelLinkNoticia.setStyleSheet("color: #000000;border: none;")
        
        OutputLinkNoticia=QTextEdit()
        OutputLinkNoticia.setStyleSheet("background-color: #FFFFFF;color: #000000;")
        OutputLinkNoticia.setFontPointSize(13)

        LabelAutorNoticia=QLabel("Autor")
        LabelAutorNoticia.setFont(QFont("Verdana", 15, QFont.Weight.Bold))
        LabelAutorNoticia.setStyleSheet("color: #000000;border: none;")

        OutputAutorNoticia=QTextEdit()
        OutputAutorNoticia.setStyleSheet("background-color: #FFFFFF;color: #000000;")
        OutputAutorNoticia.setFontPointSize(13)

        LabelFechaNoticia=QLabel("Fecha")
        LabelFechaNoticia.setFont(QFont("Verdana", 15, QFont.Weight.Bold))
        LabelFechaNoticia.setStyleSheet("color: #000000;border: none;")

        OutputFechaNoticia=QTextEdit()
        OutputFechaNoticia.setStyleSheet("background-color: #FFFFFF;color: #000000;")
        OutputFechaNoticia.setFontPointSize(13)

        LabelDescripcionNoticia=QLabel("Descpricion")
        LabelDescripcionNoticia.setFont(QFont("Verdana", 15, QFont.Weight.Bold))
        LabelDescripcionNoticia.setStyleSheet("color: #000000;border: none;")

        OutputDescripcionNoticia=QTextEdit()
        OutputDescripcionNoticia.setStyleSheet("background-color: #FFFFFF;color: #000000;")
        OutputDescripcionNoticia.setFontPointSize(13)

        #============Elementos de Botones
        def crear_boton(texto, color_normal, color_hover):
            boton = QPushButton(texto)
            boton.setFixedSize(40, 40)
            boton.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color_normal};
                    color: white;
                    border: 10px;
                    padding: 10px 15px;
                    font-weight: bold;
                    border-radius: 0px;
                    min-width: 100px;
                }}
                QPushButton:hover {{
                    background-color: {color_hover};
                }}
            """)
            return boton

        
        boton_start=crear_boton("Start ->","purple","#FFFFFF")
        boton_start.clicked.connect(presionar_boton_start)

        boton_Subir = crear_boton("Subir", "red", "#27ae60")
        boton_Subir.clicked.connect(presionar_boton_subir)
        
        boton_Editar = crear_boton("Editar", "blue", "#2980b9")  

        boton_Siguiente = crear_boton("Siguiente", "yelow", "#8e44ad")  
        boton_Siguiente.clicked.connect(presionar_boton_siguiente)

        boton_Anterior= crear_boton("Anterior", "yelow", "#c0392b")   
        boton_Anterior.clicked.connect(presionar_boton_anterior)



        Layout_Control_Noticia=QVBoxLayout()
        Layout_Control_Noticia.addWidget(LabelLinkNoticia)
        Layout_Control_Noticia.addWidget(OutputLinkNoticia)
        Layout_Control_Noticia.addWidget(LabelAutorNoticia)
        Layout_Control_Noticia.addWidget(OutputAutorNoticia)
        Layout_Control_Noticia.addWidget(LabelFechaNoticia)
        Layout_Control_Noticia.addWidget(OutputFechaNoticia)
        Layout_Control_Noticia.addWidget(LabelDescripcionNoticia)
        Layout_Control_Noticia.addWidget(OutputDescripcionNoticia)


        Layout_Datos_Noticia=QHBoxLayout()
        Layout_Datos_Noticia.addWidget(LabelImagenNoticia,60)
        Layout_Datos_Noticia.addLayout(Layout_Control_Noticia,40)
        

        Layout_App_Noticia=QVBoxLayout()
        Layout_App_Noticia.addWidget(LabelTituloNoticia)
        Layout_App_Noticia.addWidget(OutputTituloNoticia)
        Layout_App_Noticia.addLayout(Layout_Datos_Noticia)

        Layout_Botones=QVBoxLayout()
        Layout_Botones.addWidget(boton_start)
        Layout_Botones.addWidget(boton_Anterior)
        Layout_Botones.addWidget(boton_Siguiente)
        Layout_Botones.addWidget(boton_Editar)
        Layout_Botones.addWidget(boton_Subir)
        Layout_Botones.setContentsMargins(30, 20, 10, 20)

        Layout_Cuerpo=QHBoxLayout()
        Layout_Cuerpo.addLayout(Layout_App_Noticia,70)
        Layout_Cuerpo.addLayout(Layout_Botones,30)

        widget_Cuerpo = QWidget()
        widget_Cuerpo.setStyleSheet("""

            border: 2px solid #000000;
            background-color: #d9d9d9;
            border-radius: 0px;
        """)
        widget_Cuerpo.setLayout(Layout_Cuerpo)

        Layout_Cabecera=QHBoxLayout()
        Layout_Cabecera.addWidget(TituloApp)
        Layout_Cabecera.addStretch()
        Layout_Cabecera.addWidget(LogoASDU)
        Layout_Cabecera.setContentsMargins(5,5,5,5)
        

        Layout_Main=QVBoxLayout()
        Layout_Main.addLayout(Layout_Cabecera,15)
        Layout_Main.addWidget  (widget_Cuerpo,85)


        self.setLayout(Layout_Main)

