<<<<<<< HEAD
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(980, 680)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
=======
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(980, 680)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
>>>>>>> 99ee6cc1f27b24ec55020dfe9c9023f9d66fedb0
