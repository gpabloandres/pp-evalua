from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class EvaluacionEstudiante(db.Model):
    __tablename__ = 'evaluaciones_estudiante'

    id = db.Column(db.Integer, primary_key=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    anio_evaluacion = db.Column(db.Integer, nullable=False, default=lambda: datetime.now().year)
    periodo = db.Column(db.String(20), nullable=False, default='mitad')

    nombre_estudiante = db.Column(db.String(120), nullable=False)
    anio_division = db.Column(db.String(50), nullable=False)
    escuela = db.Column(db.String(150), nullable=False)
    empresa = db.Column(db.String(150), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    referente_empresa = db.Column(db.String(120), nullable=False)
    profesor_practica = db.Column(db.String(120), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)

    sat_experiencia_general = db.Column(db.Integer, nullable=False)
    sat_relacion_teoria = db.Column(db.Integer, nullable=False)
    sat_conocimiento_org = db.Column(db.Integer, nullable=False)
    sat_trato_personal = db.Column(db.Integer, nullable=False)
    sat_condiciones_amb = db.Column(db.Integer, nullable=False)
    sat_relacion_referente = db.Column(db.Integer, nullable=False)
    sat_orientaciones = db.Column(db.Integer, nullable=False)
    sat_relacion_profesor = db.Column(db.Integer, nullable=False)
    sat_apoyo_escuela = db.Column(db.Integer, nullable=False)

    resumen_itinerario = db.Column(db.Text, nullable=True)
    resumen_actividades = db.Column(db.Text, nullable=True)
    ventaja_empresa = db.Column(db.Text, nullable=True)
    aspecto_positivo = db.Column(db.Text, nullable=True)
    actividades_no_desarrolladas = db.Column(db.Text, nullable=True)
    propuesta_mejora = db.Column(db.Text, nullable=True)


class EvaluacionProfesor(db.Model):
    __tablename__ = 'evaluaciones_profesor'

    id = db.Column(db.Integer, primary_key=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    anio_evaluacion = db.Column(db.Integer, nullable=False, default=lambda: datetime.now().year)
    periodo = db.Column(db.String(20), nullable=False, default='mitad')

    nombre_profesor = db.Column(db.String(120), nullable=False)
    escuela = db.Column(db.String(150), nullable=False)
    empresa = db.Column(db.String(150), nullable=False)
    cantidad_estudiantes = db.Column(db.Integer, nullable=False, default=1)

    sat_experiencia_general = db.Column(db.Integer, nullable=False)
    sat_adecuacion_teorica = db.Column(db.Integer, nullable=False)
    sat_trato_estudiantes = db.Column(db.Integer, nullable=False)
    sat_relacion_referente = db.Column(db.Integer, nullable=False)
    sat_apoyo_empresa = db.Column(db.Integer, nullable=False)

    beneficios_estudiantes = db.Column(db.Text, nullable=True)
    aspectos_no_desarrollados = db.Column(db.Text, nullable=True)
    propuesta_mejora = db.Column(db.Text, nullable=True)


class EvaluacionReferente(db.Model):
    __tablename__ = 'evaluaciones_referente'

    id = db.Column(db.Integer, primary_key=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    anio_evaluacion = db.Column(db.Integer, nullable=False, default=lambda: datetime.now().year)
    periodo = db.Column(db.String(20), nullable=False, default='mitad')

    nombre_referente = db.Column(db.String(120), nullable=False)
    empresa = db.Column(db.String(150), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    cantidad_practicantes = db.Column(db.Integer, nullable=False, default=1)
    nombre_estudiante_evaluado = db.Column(db.String(120), nullable=True)

    sat_experiencia_general = db.Column(db.Integer, nullable=False)
    sat_adecuacion_teorica = db.Column(db.Integer, nullable=False)
    sat_adaptacion_estudiante = db.Column(db.Integer, nullable=False)
    sat_relacion_profesor = db.Column(db.Integer, nullable=False)
    sat_apoyo_escuela = db.Column(db.Integer, nullable=False)

    desempeno_teoria = db.Column(db.Integer, nullable=False)
    desempeno_instrucciones = db.Column(db.Integer, nullable=False)
    desempeno_metodo_orden = db.Column(db.Integer, nullable=False)
    desempeno_calidad_herramientas = db.Column(db.Integer, nullable=False)
    desempeno_autonomia_iniciativa = db.Column(db.Integer, nullable=False)
    desempeno_trabajo_equipo = db.Column(db.Integer, nullable=False)
    desempeno_responsabilidad = db.Column(db.Integer, nullable=False)
    desempeno_adaptabilidad_tecnologica = db.Column(db.Integer, nullable=True)

    inconvenientes = db.Column(db.Text, nullable=True)
    beneficios = db.Column(db.Text, nullable=True)
    aspectos_no_desarrollados = db.Column(db.Text, nullable=True)
    propuesta_mejora = db.Column(db.Text, nullable=True)


__all__ = [
    'db',
    'EvaluacionEstudiante',
    'EvaluacionProfesor',
    'EvaluacionReferente',
]
