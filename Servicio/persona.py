# Integrantes:
# - Crespo John
# - Danna Rodriguez
# - Genesis Garboa
# - Dayana Alvarado


from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QMainWindow, QMessageBox

from Datos.personaDAO import PersonaDAO
from Dominio.persona import Persona
from UI.vtnPrincipal import Ui_vtnPrincipal


class PersonaServicio(QMainWindow):
    def __init__(self):
        super(PersonaServicio, self).__init__()
        self.ui = Ui_vtnPrincipal()
        self.ui.setupUi(self)

        # --- CONEXIONES BOTONES ---
        self.ui.btninsertar.clicked.connect(self.guardar)
        self.ui.btnbuscar.clicked.connect(self.buscar)
        self.ui.btnactualizar.clicked.connect(self.actualizar)
        self.ui.btneliminar.clicked.connect(self.eliminar)
        self.ui.btnGuardar.clicked.connect(self.guardar)
        self.ui.btnlimpiar.clicked.connect(self.limpiar)

        # Validador: Cédula solo números
        self.ui.txtcedula.setValidator(QIntValidator())

    def obtener_datos_ui(self):
        # Capturamos todos los datos de la nueva interfaz
        return Persona(
            cedula=self.ui.txtcedula.text(),
            nombre=self.ui.txtNombre.text(),
            apellido=self.ui.txtApellido.text(),
            edad=self.ui.spEdad.text(),  # QSpinBox
            facultad=self.ui.cbfacultad.currentText(),  # ComboBox
            carrera=self.ui.txtCarrera.text(),  # LineEdit
            semestre=self.ui.cbsemestre.currentText(),  # ComboBox
            modalidad=self.ui.txtModaEstud.text()  # LineEdit
        )

    def guardar(self):
        persona = self.obtener_datos_ui()

        # --- VALIDACIONES ---

        # 1. Cédula
        if not persona.cedula or len(persona.cedula) < 3:
            QMessageBox.warning(self, 'Alerta', 'Ingrese una cédula válida.')
            return

        # 2. Nombre
        elif not persona.nombre:
            QMessageBox.warning(self, 'Alerta', 'El nombre es obligatorio.')
            return

        # 3. Apellido
        elif not persona.apellido:
            QMessageBox.warning(self, 'Alerta', 'El apellido es obligatorio.')
            return

        # 4. VALIDACIÓN DE EDAD (Nueva)
        # Si la edad es 0, asumimos que no se ingresó nada.
        elif int(persona.edad) == 0:
            QMessageBox.warning(self, 'Alerta', 'Debe ingresar la edad del estudiante.')
            return

        # 5. Facultad
        elif persona.facultad == "Seleccionar":
            QMessageBox.warning(self, 'Alerta', 'Debe seleccionar una Facultad.')
            return

        # 6. Carrera
        elif not persona.carrera:
            QMessageBox.warning(self, 'Alerta', 'El campo Carrera es obligatorio.')
            return

        # 7. Semestre
        elif persona.semestre == "Seleccionar":
            QMessageBox.warning(self, 'Alerta', 'Debe seleccionar un Semestre.')
            return

        # 8. Modalidad (Opcional: Si quieres que sea obligatoria, descomenta esto)
        elif not persona.modalidad:
              QMessageBox.warning(self, 'Alerta', 'Ingrese la modalidad.')
              return

        # --- GUARDAR EN BASE DE DATOS ---
        else:
            resp = PersonaDAO.insertar_persona(persona)

            if resp['ejecuto']:
                self.ui.statusbar.showMessage('Guardado correctamente', 3000)
                self.limpiar()
            else:
                QMessageBox.critical(self, 'Error', resp['mensaje'])

    def buscar(self):
        cedula = self.ui.txtcedula.text()
        if not cedula:
            QMessageBox.warning(self, 'Alerta', 'Ingrese cédula para buscar.')
            return

        p = PersonaDAO.seleccionar_persona(cedula)

        if p:
            self.ui.txtNombre.setText(p.nombre)
            self.ui.txtApellido.setText(p.apellido)
            self.ui.spEdad.setValue(int(p.edad))  # SetValue para SpinBox
            self.ui.cbfacultad.setCurrentText(p.facultad)
            self.ui.txtCarrera.setText(p.carrera)
            self.ui.cbsemestre.setCurrentText(p.semestre)
            self.ui.txtModaEstud.setText(p.modalidad)
            self.ui.statusbar.showMessage('Estudiante encontrado', 2000)
        else:
            QMessageBox.warning(self, 'Aviso', 'No encontrado.')

    def actualizar(self):
        persona = self.obtener_datos_ui()

        # --- CORRECCIÓN AQUÍ ---
        # Antes solo decía 'if not persona.cedula: return' (Silencioso)
        # Ahora le agregamos el mensaje:
        if not persona.cedula:
            QMessageBox.warning(self, 'Advertencia', 'Debe haber una cédula escrita para poder actualizar.')
            return

        # Llamada a la base de datos
        resp = PersonaDAO.actualizar_persona(persona)

        if resp['ejecuto']:
            self.ui.statusbar.showMessage(resp['mensaje'], 3000)
            self.limpiar()
        else:
            # Esto saldrá si la cédula no existe en la BD
            QMessageBox.critical(self, 'Error', resp['mensaje'])

    def eliminar(self):
        cedula = self.ui.txtcedula.text()
        if not cedula:
            QMessageBox.warning(self, 'Alerta', 'Ingrese cédula para eliminar.')
            return

        if QMessageBox.question(self, 'Confirmar', '¿Borrar estudiante?') == QMessageBox.Yes:
            resp = PersonaDAO.eliminar_persona(cedula)
            if resp['ejecuto']:
                self.limpiar()
                self.ui.statusbar.showMessage(resp['mensaje'], 3000)
            else:
                QMessageBox.critical(self, 'Error', resp['mensaje'])

    def limpiar(self):
        self.ui.txtcedula.clear()
        self.ui.txtNombre.clear()
        self.ui.txtApellido.clear()
        self.ui.spEdad.setValue(0)  # Reiniciar SpinBox a 0
        self.ui.cbfacultad.setCurrentIndex(0)
        self.ui.txtCarrera.clear()
        self.ui.cbsemestre.setCurrentIndex(0)
        self.ui.txtModaEstud.clear()