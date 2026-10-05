"""Helpers y constantes auxiliares para formularios."""

LIKERT_VALUES = range(1, 6)


def get_likert_labels():
    return {
        'estudiante': [
            ('sat_experiencia_general', 'La experiencia en general'),
            ('sat_relacion_teoria', 'Relación entre actividades realizadas y la formación académica'),
            ('sat_conocimiento_org', 'Conocimiento adquirido sobre la institución/empresa y su funcionamiento'),
            ('sat_trato_personal', 'El trato recibido por el personal de la institución/empresa'),
            ('sat_condiciones_amb', 'Condiciones ambientales (espacio, equipamiento, herramientas)'),
            ('sat_relacion_referente', 'Tu relación con el referente de la institución/empresa'),
            ('sat_orientaciones', 'Las orientaciones y explicaciones recibidas para tu tarea'),
            ('sat_relacion_profesor', 'Tu relación con el Profesor de Práctica Profesionalizante'),
            ('sat_apoyo_escuela', 'El apoyo de la escuela para resolver dudas o inconvenientes'),
        ],
        'docente': [
            ('sat_experiencia_general', 'La experiencia en general de realizar prácticas en esta empresa'),
            ('sat_adecuacion_teorica', 'La adecuación de las actividades a los conocimientos teóricos del alumno'),
            ('sat_trato_estudiantes', 'El trato y la acogida que los estudiantes recibieron en la empresa'),
            ('sat_relacion_referente', 'La relación y comunicación establecida con el Referente de la empresa'),
            ('sat_apoyo_empresa', 'El apoyo de la empresa para resolver inconvenientes durante la Práctica'),
        ],
        'referente': [
            ('sat_experiencia_general', 'La experiencia en general de recibir alumnos practicantes'),
            ('sat_adecuacion_teorica', 'Adecuación de los conocimientos teóricos del alumno a las tareas'),
            ('sat_adaptacion_estudiante', 'Capacidad de adaptación del practicante a la cultura de la empresa'),
            ('sat_relacion_profesor', 'Relación y fluidez de comunicación con el Profesor de la escuela'),
            ('sat_apoyo_escuela', 'Apoyo de la escuela para resolver inconvenientes o dudas'),
        ],
    }
