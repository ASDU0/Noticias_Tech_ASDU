import UI
import Scraping
import sys
from PyQt6.QtWidgets import QApplication



if __name__ == '__main__':

    app=QApplication(sys.argv)
    window=UI.MainWindow()
    sys.exit(app.exec())  
