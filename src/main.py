import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from backend import SensorBackend  # Adjusted for the new structure

def main():
    """
    Initializes and runs the Qt application with a QML-based UI.
    """
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    backend = SensorBackend()
    engine.rootContext().setContextProperty("backend", backend)

    engine.load("qml/main.qml")
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()