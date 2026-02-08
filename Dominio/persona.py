# Integrantes:
# - Crespo John
# - Danna Rodriguez
# - Genesis Garboa
# - Dayana Alvarado


class Persona:
    def __init__(self, cedula=None, nombre=None, apellido=None,
                 edad=None, facultad=None, carrera=None,
                 semestre=None, modalidad=None):
        # Al usar 'self.campo = valor', se activan los setters de abajo automáticamente
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.facultad = facultad
        self.carrera = carrera
        self.semestre = semestre
        self.modalidad = modalidad

    # --- CEDULA ---
    @property
    def cedula(self):
        return self._cedula

    @cedula.setter
    def cedula(self, valor):
        # Si es nulo, lo convertimos a texto vacío para que no falle el programa
        self._cedula = valor if valor else ""

    # --- NOMBRE ---
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor if valor else ""

    # --- APELLIDO ---
    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, valor):
        self._apellido = valor if valor else ""

    # --- EDAD ---
    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, valor):
        # La edad puede venir como int (del SpinBox) o string (de la BD)
        # Aquí nos aseguramos de guardarlo siempre bien o poner 0 si falla
        if valor is None:
            self._edad = 0
        else:
            try:
                self._edad = int(valor)
            except ValueError:
                self._edad = 0

    # --- FACULTAD ---
    @property
    def facultad(self):
        return self._facultad

    @facultad.setter
    def facultad(self, valor):
        self._facultad = valor if valor else "Seleccionar"

    # --- CARRERA ---
    @property
    def carrera(self):
        return self._carrera

    @carrera.setter
    def carrera(self, valor):
        self._carrera = valor.upper() if valor else "" # Truco: Lo guarda en MAYÚSCULAS automáticamente

    # --- SEMESTRE ---
    @property
    def semestre(self):
        return self._semestre

    @semestre.setter
    def semestre(self, valor):
        self._semestre = valor if valor else "Seleccionar"

    # --- MODALIDAD ---
    @property
    def modalidad(self):
        return self._modalidad

    @modalidad.setter
    def modalidad(self, valor):
        self._modalidad = valor if valor else ""

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.carrera}'