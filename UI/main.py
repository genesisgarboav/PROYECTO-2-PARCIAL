# Integrantes:
# - Crespo John
# - Danna Rodriguez
# - Genesis Garboa
# - Dayana Alvarado


import sys

from PySide6.QtWidgets import QApplication

from Servicio.persona import PersonaServicio

app = QApplication()
vtn_principal = PersonaServicio()
vtn_principal.show()
sys.exit(app.exec())