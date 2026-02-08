from Datos.conexion import Conexion
from Dominio.persona import Persona
import pyodbc as bd


class PersonaDAO:
    # 1. SQL ADAPTADO A LA TABLA 'Estudiantes'
    _INSERT = ("INSERT INTO Estudiantes (cedula, nombre, apellido, edad, facultad, carrera, semestre, modalidad) "
               "VALUES (?, ?, ?, ?, ?, ?, ?, ?)")

    _SELECT = ("SELECT * FROM Estudiantes WHERE cedula = ?")

    _UPDATE = ("UPDATE Estudiantes SET nombre=?, apellido=?, edad=?, facultad=?, carrera=?, semestre=?, modalidad=? "
               "WHERE cedula=?")

    _DELETE = ("DELETE FROM Estudiantes WHERE cedula=?")

    @classmethod
    def insertar_persona(cls, persona):
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            # Orden de los 8 datos
            datos = (persona.cedula, persona.nombre, persona.apellido,
                     persona.edad, persona.facultad, persona.carrera,
                     persona.semestre, persona.modalidad)

            cursor.execute(cls._INSERT, datos)
            cursor.commit()
            if cursor.rowcount > 0:
                return {'ejecuto': True, 'mensaje': 'Estudiante registrado con éxito.'}
            else:
                return {'ejecuto': False, 'mensaje': 'No se pudo guardar.'}
        except bd.IntegrityError:
            return {'ejecuto': False, 'mensaje': 'La cédula ya existe.'}
        except Exception as e:
            return {'ejecuto': False, 'mensaje': f'Error al guardar: {e}'}

    @classmethod
    def seleccionar_persona(cls, cedula):
        obj = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls._SELECT, (cedula,))
            registro = cursor.fetchone()

            if registro:
                # Mapeo de columnas (Indices basados en la tabla creada)
                obj = Persona(
                    cedula=registro[0],
                    nombre=registro[1],
                    apellido=registro[2],
                    edad=registro[3],
                    facultad=registro[4],
                    carrera=registro[5],
                    semestre=registro[6],
                    modalidad=registro[7]
                )
            return obj
        except Exception as e:
            print(f"Error al buscar: {e}")
            return None

    @classmethod
    def actualizar_persona(cls, persona):
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            datos = (persona.nombre, persona.apellido, persona.edad,
                     persona.facultad, persona.carrera, persona.semestre,
                     persona.modalidad, persona.cedula)

            cursor.execute(cls._UPDATE, datos)
            cursor.commit()
            if cursor.rowcount > 0:
                return {'ejecuto': True, 'mensaje': 'Actualizado con éxito.'}
            else:
                return {'ejecuto': False, 'mensaje': 'No se encontró la cédula.'}
        except Exception as e:
            return {'ejecuto': False, 'mensaje': f'Error al actualizar: {e}'}

    @classmethod
    def eliminar_persona(cls, cedula):
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls._DELETE, (cedula,))
            cursor.commit()
            if cursor.rowcount > 0:
                return {'ejecuto': True, 'mensaje': 'Eliminado con éxito.'}
            else:
                return {'ejecuto': False, 'mensaje': 'No se encontró el registro.'}
        except Exception as e:
            return {'ejecuto': False, 'mensaje': f'Error al eliminar: {e}'}