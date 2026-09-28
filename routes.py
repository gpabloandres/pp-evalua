from flask import flash, jsonify, redirect, render_template_string, request, url_for
from sqlalchemy import func

from models import db, EvaluacionEstudiante, EvaluacionProfesor, EvaluacionReferente


BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Gestión de Prácticas Profesionalizantes{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bs-primary-rgb: 37, 99, 235;
            --brand-gradient: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        }
        body {
            background-color: #f8fafc;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #334155;
        }
        .navbar-brand-custom {
            font-weight: 700;
            background: var(--brand-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-banner {
            background: var(--brand-gradient);
            color: white;
            border-radius: 1rem;
            padding: 2.5rem 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
        }
        .card-custom {
            border: none;
            border-radius: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card-custom:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        .btn-gradient {
            background: var(--brand-gradient);
            color: white;
            border: none;
            font-weight: 600;
        }
        .btn-gradient:hover {
            color: white;
            opacity: 0.95;
        }
        .likert-group label {
            font-size: 0.85rem;
            text-align: center;
            cursor: pointer;
        }
        .likert-radio {
            width: 1.25rem;
            height: 1.25rem;
        }
        .form-section-title {
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
            color: #1e293b;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom sticky-top shadow-sm">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center gap-2" href="{{ url_for('index') }}">
                <i class="fa-solid fa-graduation-cap text-primary fs-3"></i>
                <span class="fs-4 navbar-brand-custom">Prácticas Profesionalizantes</span>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto gap-1">
                    <li class="nav-item">
                        <a class="nav-link px-3" href="{{ url_for('index') }}"><i class="fa-solid fa-house me-1"></i> Inicio</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link px-3" href="{{ url_for('evaluacion_estudiante') }}"><i class="fa-solid fa-user-graduate me-1"></i> Estudiante</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link px-3" href="{{ url_for('evaluacion_profesor') }}"><i class="fa-solid fa-chalkboard-user me-1"></i> Docente</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link px-3" href="{{ url_for('evaluacion_referente') }}"><i class="fa-solid fa-building-user me-1"></i> Tutor Empresa</a>
                    </li>
                    <li class="nav-item">
                        <a class="btn btn-outline-primary ms-lg-2 rounded-pill px-3" href="{{ url_for('informes') }}">
                            <i class="fa-solid fa-chart-pie me-1"></i> Informes y Gráficos
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container my-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show rounded-3 shadow-sm mb-4" role="alert">
                        <i class="fa-solid fa-circle-check me-2"></i> {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <footer class="bg-white border-top py-4 mt-5">
        <div class="container text-center text-muted fs-7">
            <p class="mb-0">&copy; 2026 Sistema Integrado de Prácticas Profesionalizantes. Desarrollado con Flask & SQLite.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
"""

INDEX_TEMPLATE = BASE_TEMPLATE + """
{% block content %}
<div class="hero-banner text-center text-md-start">
    <div class="row align-items-center">
        <div class="col-md-8">
            <h1 class="fw-bold display-5 mb-2"><i class="fa-solid fa-clipboard-check me-2"></i> Evaluaciones de Prácticas</h1>
            <p class="lead mb-3">Plataforma centralizada para la recolección, almacenamiento y análisis de opiniones de los diferentes actores institucionales y empresariales.</p>
            <div class="d-flex flex-wrap gap-2">
                <a href="{{ url_for('informes') }}" class="btn btn-light btn-lg fw-semibold shadow-sm text-primary">
                    <i class="fa-solid fa-chart-line me-1"></i> Ver Panel de Informes
                </a>
                <a href="{{ url_for('generar_datos_demo') }}" class="btn btn-outline-light btn-lg fw-semibold" onclick="return confirm('¿Cargar datos de prueba ficticios en la base de datos?');">
                    <i class="fa-solid fa-database me-1"></i> Cargar Datos Demo
                </a>
            </div>
        </div>
        <div class="col-md-4 text-center d-none d-md-block">
            <i class="fa-solid fa-chart-column fa-8x opacity-75"></i>
        </div>
    </div>
</div>

<h3 class="fw-bold mb-4"><i class="fa-solid fa-pen-to-square me-2 text-primary"></i> Seleccione su Rol para completar el Formulario</h3>

<div class="row g-4">
    <div class="col-md-4">
        <div class="card card-custom h-100 p-4 border-top border-primary border-4">
            <div class="text-primary mb-3">
                <i class="fa-solid fa-user-graduate fa-3x"></i>
            </div>
            <h4 class="fw-bold">Estudiantes</h4>
            <p class="text-muted">Evalúe su experiencia en la empresa, condiciones del entorno, conocimientos aplicados y sugerencias de mejora.</p>
            <div class="mt-auto">
                <a href="{{ url_for('evaluacion_estudiante') }}" class="btn btn-primary w-100 fw-semibold rounded-pill">
                    Comenzar Evaluación <i class="fa-solid fa-arrow-right ms-1"></i>
                </a>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card card-custom h-100 p-4 border-top border-success border-4">
            <div class="text-success mb-3">
                <i class="fa-solid fa-chalkboard-user fa-3x"></i>
            </div>
            <h4 class="fw-bold">Profesor de Prácticas</h4>
            <p class="text-muted">Registre su valoración sobre el vínculo escuela-empresa, la adecuación teórica y el seguimiento brindado.</p>
            <div class="mt-auto">
                <a href="{{ url_for('evaluacion_profesor') }}" class="btn btn-success w-100 fw-semibold rounded-pill">
                    Comenzar Evaluación <i class="fa-solid fa-arrow-right ms-1"></i>
                </a>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card card-custom h-100 p-4 border-top border-warning border-4">
            <div class="text-warning mb-3">
                <i class="fa-solid fa-building-user fa-3x"></i>
            </div>
            <h4 class="fw-bold">Referente / Tutor Empresa</h4>
            <p class="text-muted">Evalúe el desempeño del practicante (autonomía, iniciativa, hábitos) y la relación con la institución educativa.</p>
            <div class="mt-auto">
                <a href="{{ url_for('evaluacion_referente') }}" class="btn btn-warning text-dark w-100 fw-semibold rounded-pill">
                    Comenzar Evaluación <i class="fa-solid fa-arrow-right ms-1"></i>
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

FORM_ESTUDIANTE_TEMPLATE = BASE_TEMPLATE + """
{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-10">
        <div class="card card-custom p-4 p-md-5">
            <div class="d-flex align-items-center gap-3 mb-4">
                <div class="bg-primary text-white p-3 rounded-circle fs-3">
                    <i class="fa-solid fa-user-graduate"></i>
                </div>
                <div>
                    <h2 class="fw-bold mb-0">Evaluación de la Experiencia por el Estudiante</h2>
                    <p class="text-muted mb-0">Anexo II - Evaluación del practicante sobre su centro de prácticas</p>
                </div>
            </div>

            <form method="POST" action="{{ url_for('evaluacion_estudiante') }}">
                <h5 class="form-section-title"><i class="fa-solid fa-id-card me-2"></i>1. Datos Generales</h5>
                <div class="row g-3 mb-4">
                    <div class="col-md-6"><label class="form-label fw-semibold">Nombre y Apellido del Estudiante *</label><input type="text" name="nombre_estudiante" class="form-control" required placeholder="Ej: Juan Pérez"></div>
                    <div class="col-md-3"><label class="form-label fw-semibold">Año / División *</label><input type="text" name="anio_division" class="form-control" required placeholder="Ej: 6to 2da"></div>
                    <div class="col-md-3"><label class="form-label fw-semibold">Especialidad *</label><input type="text" name="especialidad" class="form-control" required placeholder="Ej: Electromecánica / Informática"></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Escuela Técnica *</label><input type="text" name="escuela" class="form-control" required placeholder="Ej: EETP N° 461"></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Empresa / Organización *</label><input type="text" name="empresa" class="form-control" required placeholder="Ej: Techint / Mantenimiento SRL"></div>
                    <div class="col-md-4"><label class="form-label fw-semibold">Área / Sector asignado *</label><input type="text" name="area" class="form-control" required placeholder="Ej: Control de Calidad"></div>
                    <div class="col-md-4"><label class="form-label fw-semibold">Referente en la Empresa *</label><input type="text" name="referente_empresa" class="form-control" required placeholder="Ej: Ing. Carlos Gómez"></div>
                    <div class="col-md-4"><label class="form-label fw-semibold">Profesor de Práctica *</label><input type="text" name="profesor_practica" class="form-control" required placeholder="Ej: Prof. Roberto Martínez"></div>
                </div>

                <h5 class="form-section-title"><i class="fa-solid fa-star me-2"></i>2. Nivel de Satisfacción por Aspecto</h5>
                <p class="text-muted small mb-3">Indica tu grado de satisfacción (1: Nada Conforme | 2: Poco Conforme | 3: Conforme | 4: Muy Conforme | 5: Sumamente Conforme)</p>
                <div class="table-responsive mb-4">
                    <table class="table table-bordered table-hover align-middle">
                        <thead class="table-light text-center">
                            <tr>
                                <th style="width: 45%;">Aspecto Evaluado</th>
                                <th>1<br><small class="text-muted fw-normal">Nada</small></th>
                                <th>2<br><small class="text-muted fw-normal">Poco</small></th>
                                <th>3<br><small class="text-muted fw-normal">Conforme</small></th>
                                <th>4<br><small class="text-muted fw-normal">Muy</small></th>
                                <th>5<br><small class="text-muted fw-normal">Sumamente</small></th>
                            </tr>
                        </thead>
                        <tbody>
                            {% set items = [
                                ('sat_experiencia_general', 'La experiencia en general'),
                                ('sat_relacion_teoria', 'Relación entre actividades realizadas y conocimientos teóricos'),
                                ('sat_conocimiento_org', 'Conocimiento adquirido sobre una organización empresarial'),
                                ('sat_trato_personal', 'El trato recibido por el personal de la empresa'),
                                ('sat_condiciones_amb', 'Condiciones ambientales (espacio, equipamiento, herramientas)'),
                                ('sat_relacion_referente', 'Tu relación con el Referente de la empresa'),
                                ('sat_orientaciones', 'Las orientaciones y explicaciones recibidas para tu tarea'),
                                ('sat_relacion_profesor', 'Tu relación con el Profesor de Práctica Profesionalizante'),
                                ('sat_apoyo_escuela', 'El apoyo de la escuela para resolver dudas o inconvenientes')
                            ] %}
                            {% for field_name, label in items %}
                            <tr>
                                <td><strong>{{ label }}</strong></td>
                                {% for val in range(1, 6) %}
                                <td class="text-center"><input class="form-check-input likert-radio" type="radio" name="{{ field_name }}" value="{{ val }}" {% if val == 4 %}checked{% endif %} required></td>
                                {% endfor %}
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

                <h5 class="form-section-title"><i class="fa-solid fa-comment-dots me-2"></i>3. Comentarios y Diagnóstico Cualitativo</h5>
                <div class="row g-3 mb-4">
                    <div class="col-md-6"><label class="form-label fw-semibold">Itinerario seguido (áreas/sectores)</label><textarea name="resumen_itinerario" class="form-control" rows="2" placeholder="Resuma brevemente el itinerario..."></textarea></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Principales actividades desarrolladas</label><textarea name="resumen_actividades" class="form-control" rows="2" placeholder="Describa sus tareas principales..."></textarea></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Ventaja de realizar la Práctica en esta empresa</label><textarea name="ventaja_empresa" class="form-control" rows="2" placeholder="Señale alguna ventaja observada..."></textarea></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Aspecto más positivo para su formación</label><textarea name="aspecto_positivo" class="form-control" rows="2" placeholder="¿Cuál cree que fue el aspecto más positivo?"></textarea></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Actividades no desarrolladas que considera importantes</label><textarea name="actividades_no_desarrolladas" class="form-control" rows="2" placeholder="Temas o tareas que le hubiera gustado realizar..."></textarea></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Sugerencias de mejora / Cambios planteados</label><textarea name="propuesta_mejora" class="form-control" rows="2" placeholder="Si repitiera la experiencia, ¿qué cambiaría?"></textarea></div>
                </div>

                <div class="text-end">
                    <button type="submit" class="btn btn-gradient btn-lg px-5 rounded-pill shadow"><i class="fa-solid fa-paper-plane me-2"></i> Registrar Evaluación</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
"""

FORM_PROFESOR_TEMPLATE = BASE_TEMPLATE + """
{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-10">
        <div class="card card-custom p-4 p-md-5 border-top border-success border-4">
            <div class="d-flex align-items-center gap-3 mb-4">
                <div class="bg-success text-white p-3 rounded-circle fs-3"><i class="fa-solid fa-chalkboard-user"></i></div>
                <div>
                    <h2 class="fw-bold mb-0">Evaluación de la Experiencia - Docente de Prácticas</h2>
                    <p class="text-muted mb-0">Anexo III - Informe de seguimiento y vinculación del Profesor</p>
                </div>
            </div>

            <form method="POST" action="{{ url_for('evaluacion_profesor') }}">
                <h5 class="form-section-title"><i class="fa-solid fa-id-card me-2"></i>1. Datos de la Escuela y Empresa</h5>
                <div class="row g-3 mb-4">
                    <div class="col-md-6"><label class="form-label fw-semibold">Nombre del Profesor *</label><input type="text" name="nombre_profesor" class="form-control" required placeholder="Ej: Ing. Mario Silva"></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Escuela Técnica *</label><input type="text" name="escuela" class="form-control" required placeholder="Ej: EETP N° 461"></div>
                    <div class="col-md-8"><label class="form-label fw-semibold">Empresa donde realizaron la Práctica *</label><input type="text" name="empresa" class="form-control" required placeholder="Ej: Acindar / Mahle"></div>
                    <div class="col-md-4"><label class="form-label fw-semibold">Cantidad de estudiantes a su cargo *</label><input type="number" name="cantidad_estudiantes" min="1" class="form-control" value="1" required></div>
                </div>

                <h5 class="form-section-title"><i class="fa-solid fa-star me-2"></i>2. Grado de Satisfacción con la Empresa</h5>
                <div class="table-responsive mb-4">
                    <table class="table table-bordered table-hover align-middle">
                        <thead class="table-light text-center"><tr><th style="width: 45%;">Aspecto Evaluado</th><th>1<br><small class="text-muted fw-normal">Nada</small></th><th>2<br><small class="text-muted fw-normal">Poco</small></th><th>3<br><small class="text-muted fw-normal">Conforme</small></th><th>4<br><small class="text-muted fw-normal">Muy</small></th><th>5<br><small class="text-muted fw-normal">Sumamente</small></th></tr></thead>
                        <tbody>
                            {% set items = [
                                ('sat_experiencia_general', 'La experiencia en general de realizar prácticas en esta empresa'),
                                ('sat_adecuacion_teorica', 'La adecuación de las actividades a los conocimientos teóricos del alumno'),
                                ('sat_trato_estudiantes', 'El trato y la acogida que los estudiantes recibieron en la empresa'),
                                ('sat_relacion_referente', 'La relación y comunicación establecida con el Referente de la empresa'),
                                ('sat_apoyo_empresa', 'El apoyo de la empresa para resolver inconvenientes durante la Práctica')
                            ] %}
                            {% for field_name, label in items %}
                            <tr>
                                <td><strong>{{ label }}</strong></td>
                                {% for val in range(1, 6) %}
                                <td class="text-center"><input class="form-check-input likert-radio" type="radio" name="{{ field_name }}" value="{{ val }}" {% if val == 4 %}checked{% endif %} required></td>
                                {% endfor %}
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

                <h5 class="form-section-title"><i class="fa-solid fa-comment-dots me-2"></i>3. Retroalimentación Pedagógica</h5>
                <div class="row g-3 mb-4">
                    <div class="col-md-12"><label class="form-label fw-semibold">Principales beneficios obtenidos por los estudiantes</label><textarea name="beneficios_estudiantes" class="form-control" rows="2" placeholder="Comente los principales logros de aprendizaje..."></textarea></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Aspectos no desarrollados en el Plan de Prácticas</label><textarea name="aspectos_no_desarrollados" class="form-control" rows="2" placeholder="Aspectos a incluir en el plan futuro..."></textarea></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Propuestas de mejora o cambios sugeridos</label><textarea name="propuesta_mejora" class="form-control" rows="2" placeholder="Indique al menos un aspecto a mejorar..."></textarea></div>
                </div>

                <div class="text-end">
                    <button type="submit" class="btn btn-success btn-lg px-5 rounded-pill shadow"><i class="fa-solid fa-paper-plane me-2"></i> Registrar Informe Docente</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
"""

FORM_REFERENTE_TEMPLATE = BASE_TEMPLATE + """
{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-10">
        <div class="card card-custom p-4 p-md-5 border-top border-warning border-4">
            <div class="d-flex align-items-center gap-3 mb-4">
                <div class="bg-warning text-dark p-3 rounded-circle fs-3"><i class="fa-solid fa-building-user"></i></div>
                <div>
                    <h2 class="fw-bold mb-0">Evaluación del Practicante y la Experiencia por el Referente Empresa</h2>
                    <p class="text-muted mb-0">Anexo I y IV - Informe del Tutor / Instructor Organizacional</p>
                </div>
            </div>

            <form method="POST" action="{{ url_for('evaluacion_referente') }}">
                <h5 class="form-section-title"><i class="fa-solid fa-building me-2"></i>1. Datos del Referente y Empresa</h5>
                <div class="row g-3 mb-4">
                    <div class="col-md-6"><label class="form-label fw-semibold">Nombre del Referente / Instructor *</label><input type="text" name="nombre_referente" class="form-control" required placeholder="Ej: Ing. Laura Fernández"></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Empresa / Organización *</label><input type="text" name="empresa" class="form-control" required placeholder="Ej: Bunge / General Motors"></div>
                    <div class="col-md-4"><label class="form-label fw-semibold">Cargo en la Empresa *</label><input type="text" name="cargo" class="form-control" required placeholder="Ej: Jefa de Mantenimiento"></div>
                    <div class="col-md-4"><label class="form-label fw-semibold">Área / Sector *</label><input type="text" name="area" class="form-control" required placeholder="Ej: Automatización"></div>
                    <div class="col-md-4"><label class="form-label fw-semibold">Cantidad de Practicantes a Cargo *</label><input type="number" name="cantidad_practicantes" min="1" value="1" class="form-control" required></div>
                    <div class="col-md-12"><label class="form-label fw-semibold">Nombre del Estudiante Evaluado (Opcional si evalúa un caso individual)</label><input type="text" name="nombre_estudiante_evaluado" class="form-control" placeholder="Ej: Lucas González"></div>
                </div>

                <h5 class="form-section-title"><i class="fa-solid fa-list-check me-2"></i>2. Evaluación de Competencias y Desempeño del Practicante</h5>
                <p class="text-muted small mb-3">Nivel de Logro (1: Muy Bajo/Nulo | 2: Bajo | 3: Aceptable | 4: Alto | 5: Muy Alto / Superó expectativas)</p>
                <div class="table-responsive mb-4">
                    <table class="table table-bordered table-hover align-middle">
                        <thead class="table-light text-center"><tr><th style="width: 45%;">Indicadores de Logro / Aspectos</th><th>1<br><small class="text-muted fw-normal">Muy bajo</small></th><th>2<br><small class="text-muted fw-normal">Bajo</small></th><th>3<br><small class="text-muted fw-normal">Aceptable</small></th><th>4<br><small class="text-muted fw-normal">Alto</small></th><th>5<br><small class="text-muted fw-normal">Muy Alto</small></th></tr></thead>
                        <tbody>
                            {% set desempeno_items = [
                                ('desempeno_teoria', 'Conocimientos teóricos específicos aplicados'),
                                ('desempeno_instrucciones', 'Asimilación de instrucciones verbales y escritas'),
                                ('desempeno_metodo_orden', 'Método de trabajo, orden, limpieza y seguridad'),
                                ('desempeno_calidad_herramientas', 'Calidad del trabajo y uso adecuado de herramientas/equipos'),
                                ('desempeno_autonomia_iniciativa', 'Autonomía en tareas e iniciativa/resolución de problemas'),
                                ('desempeno_trabajo_equipo', 'Espíritu de colaboración y trabajo en equipo'),
                                ('desempeno_responsabilidad', 'Asistencia, puntualidad, responsabilidad e interés')
                            ] %}
                            {% for field_name, label in desempeno_items %}
                            <tr>
                                <td><strong>{{ label }}</strong></td>
                                {% for val in range(1, 6) %}
                                <td class="text-center"><input class="form-check-input likert-radio" type="radio" name="{{ field_name }}" value="{{ val }}" {% if val == 4 %}checked{% endif %} required></td>
                                {% endfor %}
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

                <h5 class="form-section-title"><i class="fa-solid fa-handshake me-2"></i>3. Satisfacción Global con la Experiencia y la Escuela</h5>
                <div class="table-responsive mb-4">
                    <table class="table table-bordered table-hover align-middle">
                        <thead class="table-light text-center"><tr><th style="width: 45%;">Aspecto</th><th>1<br><small class="text-muted fw-normal">Nada</small></th><th>2<br><small class="text-muted fw-normal">Poco</small></th><th>3<br><small class="text-muted fw-normal">Conforme</small></th><th>4<br><small class="text-muted fw-normal">Muy</small></th><th>5<br><small class="text-muted fw-normal">Sumamente</small></th></tr></thead>
                        <tbody>
                            {% set sat_items = [
                                ('sat_experiencia_general', 'La experiencia en general de recibir alumnos practicantes'),
                                ('sat_adecuacion_teorica', 'Adecuación de los conocimientos teóricos del alumno a las tareas'),
                                ('sat_adaptacion_estudiante', 'Capacidad de adaptación del practicante a la cultura de la empresa'),
                                ('sat_relacion_profesor', 'Relación y fluidez de comunicación con el Profesor de la escuela'),
                                ('sat_apoyo_escuela', 'Apoyo de la escuela para resolver inconvenientes o dudas')
                            ] %}
                            {% for field_name, label in sat_items %}
                            <tr>
                                <td><strong>{{ label }}</strong></td>
                                {% for val in range(1, 6) %}
                                <td class="text-center"><input class="form-check-input likert-radio" type="radio" name="{{ field_name }}" value="{{ val }}" {% if val == 4 %}checked{% endif %} required></td>
                                {% endfor %}
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

                <h5 class="form-section-title"><i class="fa-solid fa-comment-dots me-2"></i>4. Comentarios y Observaciones</h5>
                <div class="row g-3 mb-4">
                    <div class="col-md-6"><label class="form-label fw-semibold">Principales beneficios para la empresa</label><textarea name="beneficios" class="form-control" rows="2" placeholder="Aporte de los practicantes a la organización..."></textarea></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Principales dificultades o inconvenientes</label><textarea name="inconvenientes" class="form-control" rows="2" placeholder="Dificultades observadas..."></textarea></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Aspectos a reforzar en la formación del estudiante</label><textarea name="aspectos_no_desarrollados" class="form-control" rows="2" placeholder="Conocimientos o competencias a mejorar..."></textarea></div>
                    <div class="col-md-6"><label class="form-label fw-semibold">Sugerencias para futuras Prácticas Profesionalizantes</label><textarea name="propuesta_mejora" class="form-control" rows="2" placeholder="Recomendaciones para la escuela..."></textarea></div>
                </div>

                <div class="text-end">
                    <button type="submit" class="btn btn-warning text-dark btn-lg px-5 rounded-pill shadow"><i class="fa-solid fa-paper-plane me-2"></i> Registrar Informe de Empresa</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
"""

DASHBOARD_TEMPLATE = BASE_TEMPLATE + """
{% block content %}
<div class="d-flex flex-column flex-md-row align-items-md-center justify-content-between mb-4 gap-3">
    <div>
        <h2 class="fw-bold mb-1"><i class="fa-solid fa-chart-column text-primary me-2"></i> Panel Analítico e Informes</h2>
        <p class="text-muted mb-0">Consolidado cuantitativo y cualitativo de las opiniones de los tres actores.</p>
    </div>
    <div class="d-flex gap-2">
        <a href="{{ url_for('informes') }}" class="btn btn-outline-secondary rounded-pill"><i class="fa-solid fa-arrows-rotate me-1"></i> Actualizar</a>
    </div>
</div>

<div class="row g-3 mb-4">
    <div class="col-md-4"><div class="card card-custom p-3 border-start border-primary border-4 bg-white"><div class="d-flex align-items-center justify-content-between"><div><span class="text-muted small fw-bold">EVALUACIONES ESTUDIANTES</span><h2 class="fw-bold text-primary mb-0" id="kpi-estudiantes">0</h2></div><div class="bg-primary bg-opacity-10 text-primary p-3 rounded-circle fs-3"><i class="fa-solid fa-user-graduate"></i></div></div></div></div>
    <div class="col-md-4"><div class="card card-custom p-3 border-start border-success border-4 bg-white"><div class="d-flex align-items-center justify-content-between"><div><span class="text-muted small fw-bold">EVALUACIONES DOCENTES</span><h2 class="fw-bold text-success mb-0" id="kpi-docentes">0</h2></div><div class="bg-success bg-opacity-10 text-success p-3 rounded-circle fs-3"><i class="fa-solid fa-chalkboard-user"></i></div></div></div></div>
    <div class="col-md-4"><div class="card card-custom p-3 border-start border-warning border-4 bg-white"><div class="d-flex align-items-center justify-content-between"><div><span class="text-muted small fw-bold">EVALUACIONES TUTORES</span><h2 class="fw-bold text-warning mb-0" id="kpi-tutores">0</h2></div><div class="bg-warning bg-opacity-10 text-warning p-3 rounded-circle fs-3"><i class="fa-solid fa-building-user"></i></div></div></div></div>
</div>

<div class="row g-4 mb-4">
    <div class="col-lg-7"><div class="card card-custom p-4 h-100"><h5 class="fw-bold mb-3"><i class="fa-solid fa-chart-bar text-primary me-2"></i> Grado de Satisfacción Promedio por Actor (Escala 1 a 5)</h5><div class="chart-container" style="position: relative; height:300px;"><canvas id="satisfaccionChart"></canvas></div></div></div>
    <div class="col-lg-5"><div class="card card-custom p-4 h-100"><h5 class="fw-bold mb-3"><i class="fa-solid fa-chart-pie text-success me-2"></i> Competencias de Estudiantes según Tutores</h5><div class="chart-container" style="position: relative; height:300px;"><canvas id="competenciasChart"></canvas></div></div></div>
</div>

<div class="card card-custom p-4">
    <div class="d-flex align-items-center justify-content-between mb-3">
        <h5 class="fw-bold mb-0"><i class="fa-solid fa-comments text-info me-2"></i> Reporte Cualitativo y Sugerencias de Mejora</h5>
        <select id="filtro-rol" class="form-select form-select-sm w-auto" onchange="cargarObservaciones()">
            <option value="todos">Todos los Actores</option>
            <option value="estudiantes">Solo Estudiantes</option>
            <option value="docentes">Solo Docentes</option>
            <option value="tutores">Solo Tutores Empresa</option>
        </select>
    </div>
    <div class="table-responsive">
        <table class="table table-striped table-hover align-middle">
            <thead class="table-dark">
                <tr><th>Actor</th><th>Nombre / Entidad</th><th>Empresa / Escuela</th><th>Sugerencias de Mejora / Aspectos Positivos</th></tr>
            </thead>
            <tbody id="tabla-observaciones"><tr><td colspan="4" class="text-center py-3 text-muted">Cargando comentarios...</td></tr></tbody>
        </table>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
let chartSat = null;
let chartComp = null;

document.addEventListener('DOMContentLoaded', function() {
    cargarEstadisticas();
    cargarObservaciones();
});

function cargarEstadisticas() {
    fetch('{{ url_for("api_estadisticas") }}')
        .then(res => res.json())
        .then(data => {
            document.getElementById('kpi-estudiantes').innerText = data.totales.estudiantes;
            document.getElementById('kpi-docentes').innerText = data.totales.docentes;
            document.getElementById('kpi-tutores').innerText = data.totales.tutores;

            const ctxSat = document.getElementById('satisfaccionChart').getContext('2d');
            if (chartSat) chartSat.destroy();
            chartSat = new Chart(ctxSat, {
                type: 'bar',
                data: {
                    labels: ['Exp. General', 'Rel. Teoría/Práctica', 'Relación / Vínculo', 'Apoyo Institución'],
                    datasets: [
                        { label: 'Estudiantes', data: [data.promedios.estudiante.general, data.promedios.estudiante.teoria, data.promedios.estudiante.relacion, data.promedios.estudiante.apoyo], backgroundColor: 'rgba(37, 99, 235, 0.75)' },
                        { label: 'Docentes', data: [data.promedios.docente.general, data.promedios.docente.teoria, data.promedios.docente.relacion, data.promedios.docente.apoyo], backgroundColor: 'rgba(22, 163, 74, 0.75)' },
                        { label: 'Tutores Empresa', data: [data.promedios.tutor.general, data.promedios.tutor.teoria, data.promedios.tutor.relacion, data.promedios.tutor.apoyo], backgroundColor: 'rgba(217, 119, 6, 0.75)' }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { min: 0, max: 5, ticks: { stepSize: 1 } } }
                }
            });

            const ctxComp = document.getElementById('competenciasChart').getContext('2d');
            if (chartComp) chartComp.destroy();
            chartComp = new Chart(ctxComp, {
                type: 'radar',
                data: {
                    labels: ['Conoc. Teóricos', 'Instrucciones', 'Método/Orden', 'Uso Herramientas', 'Autonomía/Iniciativa', 'Trabajo Equipo', 'Responsabilidad'],
                    datasets: [{
                        label: 'Nivel Promedio Observado',
                        data: [data.competencias.teoria, data.competencias.instrucciones, data.competencias.metodo, data.competencias.herramientas, data.competencias.autonomia, data.competencias.equipo, data.competencias.responsabilidad],
                        fill: true,
                        backgroundColor: 'rgba(217, 119, 6, 0.2)',
                        borderColor: 'rgb(217, 119, 6)',
                        pointBackgroundColor: 'rgb(217, 119, 6)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { r: { min: 0, max: 5 } }
                }
            });
        })
        .catch(err => console.error("Error al cargar estadísticas:", err));
}

function cargarObservaciones() {
    const rol = document.getElementById('filtro-rol').value;
    fetch(`{{ url_for("api_observaciones") }}?rol=${rol}`)
        .then(res => res.json())
        .then(items => {
            const tbody = document.getElementById('tabla-observaciones');
            if (items.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" class="text-center py-3 text-muted">No se encontraron comentarios registrados.</td></tr>';
                return;
            }
            tbody.innerHTML = items.map(item => `
                <tr>
                    <td><span class="badge bg-${item.badge}">${item.actor}</span></td>
                    <td class="fw-semibold">${item.nombre}</td>
                    <td>${item.entidad}</td>
                    <td>${item.comentario || '<em>Sin observaciones particulares</em>'}</td>
                </tr>
            `).join('');
        });
}
</script>
{% endblock %}
"""

def avg_metric(value):
    return round(float(value), 2) if value else 0.0


def create_demo_records():
    estudiante_1 = EvaluacionEstudiante(
        nombre_estudiante='Matías Rossi', anio_division='6to 1ra', escuela='EETP N° 461',
        empresa='Techint', area='Mantenimiento Industrial', referente_empresa='Ing. Carlos Gómez',
        profesor_practica='Prof. Roberto Martínez', especialidad='Electromecánica',
        sat_experiencia_general=5, sat_relacion_teoria=4, sat_conocimiento_org=5,
        sat_trato_personal=4, sat_condiciones_amb=5, sat_relacion_referente=5,
        sat_orientaciones=4, sat_relacion_profesor=5, sat_apoyo_escuela=4,
        aspecto_positivo='Uso de instrumental de última tecnología y trabajo en equipos reales.',
        propuesta_mejora='Extender las semanas de prácticas en el sector de automatización.'
    )
    estudiante_2 = EvaluacionEstudiante(
        nombre_estudiante='Sofia Fernández', anio_division='6to 2da', escuela='EETP N° 462',
        empresa='Mantenimiento SRL', area='Calidad y Desarrollo', referente_empresa='Laura Paez',
        profesor_practica='Prof. Ana Torres', especialidad='Informática',
        sat_experiencia_general=4, sat_relacion_teoria=3, sat_conocimiento_org=4,
        sat_trato_personal=5, sat_condiciones_amb=4, sat_relacion_referente=4,
        sat_orientaciones=4, sat_relacion_profesor=4, sat_apoyo_escuela=3,
        aspecto_positivo='Excelente ambiente de trabajo y colaboración del equipo.',
        propuesta_mejora='Adelantar contenidos de bases de datos SQL en 5to año.'
    )

    docente_1 = EvaluacionProfesor(
        nombre_profesor='Prof. Roberto Martínez', escuela='EETP N° 461', empresa='Techint',
        cantidad_estudiantes=3, sat_experiencia_general=5, sat_adecuacion_teorica=4,
        sat_trato_estudiantes=5, sat_relacion_referente=5, sat_apoyo_empresa=4,
        beneficios_estudiantes='Comprensión integral de normas de seguridad e higiene laboral.',
        propuesta_mejora='Programar reuniones mensuales presenciales escuela-empresa.'
    )

    referente_1 = EvaluacionReferente(
        nombre_referente='Ing. Carlos Gómez', empresa='Techint', cargo='Jefe de Planta',
        area='Mantenimiento', cantidad_practicantes=2, nombre_estudiante_evaluado='Matías Rossi',
        sat_experiencia_general=5, sat_adecuacion_teorica=4, sat_adaptacion_estudiante=5,
        sat_relacion_profesor=4, sat_apoyo_escuela=4, desempeno_teoria=4,
        desempeno_instrucciones=5, desempeno_metodo_orden=5, desempeno_calidad_herramientas=4,
        desempeno_autonomia_iniciativa=4, desempeno_trabajo_equipo=5, desempeno_responsabilidad=5,
        beneficios='Aporte fresco de ideas y colaboración en proyectos secundarios.',
        propuesta_mejora='Profundizar en lectura de planos neumáticos.'
    )

    return [estudiante_1, estudiante_2, docente_1, referente_1]


def render_page(template):
    content_block = '{% block content %}'
    block_end = '{% endblock %}'
    content_start = template.find(content_block, len(BASE_TEMPLATE))
    content_end = template.find(block_end, content_start)
    content = template[content_start + len(content_block):content_end]

    page_template = BASE_TEMPLATE.replace(
        content_block + block_end,
        content,
        1
    )

    scripts_block = '{% block scripts %}'
    scripts_start = template.find(scripts_block, content_end)
    if scripts_start != -1:
        scripts_end = template.find(block_end, scripts_start)
        scripts = template[scripts_start + len(scripts_block):scripts_end]
        page_template = page_template.replace(
            scripts_block + block_end,
            scripts,
            1
        )

    return render_template_string(page_template)


def register_routes(app):
    @app.route('/')
    def index():
        return render_page(INDEX_TEMPLATE)

    @app.route('/evaluacion/estudiante', methods=['GET', 'POST'])
    def evaluacion_estudiante():
        if request.method == 'POST':
            evaluacion = EvaluacionEstudiante(
                nombre_estudiante=request.form.get('nombre_estudiante'),
                anio_division=request.form.get('anio_division'),
                escuela=request.form.get('escuela'),
                empresa=request.form.get('empresa'),
                area=request.form.get('area'),
                referente_empresa=request.form.get('referente_empresa'),
                profesor_practica=request.form.get('profesor_practica'),
                especialidad=request.form.get('especialidad'),
                sat_experiencia_general=int(request.form.get('sat_experiencia_general', 4)),
                sat_relacion_teoria=int(request.form.get('sat_relacion_teoria', 4)),
                sat_conocimiento_org=int(request.form.get('sat_conocimiento_org', 4)),
                sat_trato_personal=int(request.form.get('sat_trato_personal', 4)),
                sat_condiciones_amb=int(request.form.get('sat_condiciones_amb', 4)),
                sat_relacion_referente=int(request.form.get('sat_relacion_referente', 4)),
                sat_orientaciones=int(request.form.get('sat_orientaciones', 4)),
                sat_relacion_profesor=int(request.form.get('sat_relacion_profesor', 4)),
                sat_apoyo_escuela=int(request.form.get('sat_apoyo_escuela', 4)),
                resumen_itinerario=request.form.get('resumen_itinerario'),
                resumen_actividades=request.form.get('resumen_actividades'),
                ventaja_empresa=request.form.get('ventaja_empresa'),
                aspecto_positivo=request.form.get('aspecto_positivo'),
                actividades_no_desarrolladas=request.form.get('actividades_no_desarrolladas'),
                propuesta_mejora=request.form.get('propuesta_mejora')
            )
            db.session.add(evaluacion)
            db.session.commit()
            flash('¡Evaluación de Estudiante registrada con éxito!', 'success')
            return redirect(url_for('index'))
        return render_page(FORM_ESTUDIANTE_TEMPLATE)

    @app.route('/evaluacion/profesor', methods=['GET', 'POST'])
    def evaluacion_profesor():
        if request.method == 'POST':
            evaluacion = EvaluacionProfesor(
                nombre_profesor=request.form.get('nombre_profesor'),
                escuela=request.form.get('escuela'),
                empresa=request.form.get('empresa'),
                cantidad_estudiantes=int(request.form.get('cantidad_estudiantes', 1)),
                sat_experiencia_general=int(request.form.get('sat_experiencia_general', 4)),
                sat_adecuacion_teorica=int(request.form.get('sat_adecuacion_teorica', 4)),
                sat_trato_estudiantes=int(request.form.get('sat_trato_estudiantes', 4)),
                sat_relacion_referente=int(request.form.get('sat_relacion_referente', 4)),
                sat_apoyo_empresa=int(request.form.get('sat_apoyo_empresa', 4)),
                beneficios_estudiantes=request.form.get('beneficios_estudiantes'),
                aspectos_no_desarrollados=request.form.get('aspectos_no_desarrollados'),
                propuesta_mejora=request.form.get('propuesta_mejora')
            )
            db.session.add(evaluacion)
            db.session.commit()
            flash('¡Informe del Profesor registrado con éxito!', 'success')
            return redirect(url_for('index'))
        return render_page(FORM_PROFESOR_TEMPLATE)

    @app.route('/evaluacion/referente', methods=['GET', 'POST'])
    def evaluacion_referente():
        if request.method == 'POST':
            evaluacion = EvaluacionReferente(
                nombre_referente=request.form.get('nombre_referente'),
                empresa=request.form.get('empresa'),
                cargo=request.form.get('cargo'),
                area=request.form.get('area'),
                cantidad_practicantes=int(request.form.get('cantidad_practicantes', 1)),
                nombre_estudiante_evaluado=request.form.get('nombre_estudiante_evaluado'),
                sat_experiencia_general=int(request.form.get('sat_experiencia_general', 4)),
                sat_adecuacion_teorica=int(request.form.get('sat_adecuacion_teorica', 4)),
                sat_adaptacion_estudiante=int(request.form.get('sat_adaptacion_estudiante', 4)),
                sat_relacion_profesor=int(request.form.get('sat_relacion_profesor', 4)),
                sat_apoyo_escuela=int(request.form.get('sat_apoyo_escuela', 4)),
                desempeno_teoria=int(request.form.get('desempeno_teoria', 4)),
                desempeno_instrucciones=int(request.form.get('desempeno_instrucciones', 4)),
                desempeno_metodo_orden=int(request.form.get('desempeno_metodo_orden', 4)),
                desempeno_calidad_herramientas=int(request.form.get('desempeno_calidad_herramientas', 4)),
                desempeno_autonomia_iniciativa=int(request.form.get('desempeno_autonomia_iniciativa', 4)),
                desempeno_trabajo_equipo=int(request.form.get('desempeno_trabajo_equipo', 4)),
                desempeno_responsabilidad=int(request.form.get('desempeno_responsabilidad', 4)),
                inconvenientes=request.form.get('inconvenientes'),
                beneficios=request.form.get('beneficios'),
                aspectos_no_desarrollados=request.form.get('aspectos_no_desarrollados'),
                propuesta_mejora=request.form.get('propuesta_mejora')
            )
            db.session.add(evaluacion)
            db.session.commit()
            flash('¡Evaluación del Referente registrada con éxito!', 'success')
            return redirect(url_for('index'))
        return render_page(FORM_REFERENTE_TEMPLATE)

    @app.route('/informes')
    def informes():
        return render_page(DASHBOARD_TEMPLATE)

    @app.route('/api/estadisticas')
    def api_estadisticas():
        tot_est = EvaluacionEstudiante.query.count()
        tot_doc = EvaluacionProfesor.query.count()
        tot_tut = EvaluacionReferente.query.count()

        est_gen = avg_metric(db.session.query(func.avg(EvaluacionEstudiante.sat_experiencia_general)).scalar())
        est_teo = avg_metric(db.session.query(func.avg(EvaluacionEstudiante.sat_relacion_teoria)).scalar())
        est_rel = avg_metric(db.session.query(func.avg(EvaluacionEstudiante.sat_relacion_referente)).scalar())
        est_apo = avg_metric(db.session.query(func.avg(EvaluacionEstudiante.sat_apoyo_escuela)).scalar())

        doc_gen = avg_metric(db.session.query(func.avg(EvaluacionProfesor.sat_experiencia_general)).scalar())
        doc_teo = avg_metric(db.session.query(func.avg(EvaluacionProfesor.sat_adecuacion_teorica)).scalar())
        doc_rel = avg_metric(db.session.query(func.avg(EvaluacionProfesor.sat_relacion_referente)).scalar())
        doc_apo = avg_metric(db.session.query(func.avg(EvaluacionProfesor.sat_apoyo_empresa)).scalar())

        tut_gen = avg_metric(db.session.query(func.avg(EvaluacionReferente.sat_experiencia_general)).scalar())
        tut_teo = avg_metric(db.session.query(func.avg(EvaluacionReferente.sat_adecuacion_teorica)).scalar())
        tut_rel = avg_metric(db.session.query(func.avg(EvaluacionReferente.sat_relacion_profesor)).scalar())
        tut_apo = avg_metric(db.session.query(func.avg(EvaluacionReferente.sat_apoyo_escuela)).scalar())

        comp_teo = avg_metric(db.session.query(func.avg(EvaluacionReferente.desempeno_teoria)).scalar())
        comp_ins = avg_metric(db.session.query(func.avg(EvaluacionReferente.desempeno_instrucciones)).scalar())
        comp_met = avg_metric(db.session.query(func.avg(EvaluacionReferente.desempeno_metodo_orden)).scalar())
        comp_her = avg_metric(db.session.query(func.avg(EvaluacionReferente.desempeno_calidad_herramientas)).scalar())
        comp_aut = avg_metric(db.session.query(func.avg(EvaluacionReferente.desempeno_autonomia_iniciativa)).scalar())
        comp_equ = avg_metric(db.session.query(func.avg(EvaluacionReferente.desempeno_trabajo_equipo)).scalar())
        comp_res = avg_metric(db.session.query(func.avg(EvaluacionReferente.desempeno_responsabilidad)).scalar())

        return jsonify({
            'totales': {'estudiantes': tot_est, 'docentes': tot_doc, 'tutores': tot_tut},
            'promedios': {
                'estudiante': {'general': est_gen, 'teoria': est_teo, 'relacion': est_rel, 'apoyo': est_apo},
                'docente': {'general': doc_gen, 'teoria': doc_teo, 'relacion': doc_rel, 'apoyo': doc_apo},
                'tutor': {'general': tut_gen, 'teoria': tut_teo, 'relacion': tut_rel, 'apoyo': tut_apo}
            },
            'competencias': {
                'teoria': comp_teo,
                'instrucciones': comp_ins,
                'metodo': comp_met,
                'herramientas': comp_her,
                'autonomia': comp_aut,
                'equipo': comp_equ,
                'responsabilidad': comp_res,
            }
        })

    @app.route('/api/observaciones')
    def api_observaciones():
        rol = request.args.get('rol', 'todos')
        resultados = []

        if rol in ['todos', 'estudiantes']:
            for e in EvaluacionEstudiante.query.order_by(EvaluacionEstudiante.id.desc()).limit(10).all():
                resultados.append({
                    'actor': 'Estudiante',
                    'badge': 'primary',
                    'nombre': e.nombre_estudiante,
                    'entidad': f"{e.escuela} / {e.empresa}",
                    'comentario': e.propuesta_mejora or e.aspecto_positivo
                })

        if rol in ['todos', 'docentes']:
            for d in EvaluacionProfesor.query.order_by(EvaluacionProfesor.id.desc()).limit(10).all():
                resultados.append({
                    'actor': 'Docente',
                    'badge': 'success',
                    'nombre': d.nombre_profesor,
                    'entidad': f"{d.escuela} -> {d.empresa}",
                    'comentario': d.propuesta_mejora or d.beneficios_estudiantes
                })

        if rol in ['todos', 'tutores']:
            for t in EvaluacionReferente.query.order_by(EvaluacionReferente.id.desc()).limit(10).all():
                resultados.append({
                    'actor': 'Tutor',
                    'badge': 'warning',
                    'nombre': t.nombre_referente,
                    'entidad': f"{t.empresa} / {t.area}",
                    'comentario': t.propuesta_mejora or t.beneficios or t.inconvenientes
                })

        return jsonify(resultados)

    @app.route('/generar_datos_demo')
    def generar_datos_demo():
        db.session.add_all(create_demo_records())
        db.session.commit()
        flash('¡Datos de prueba cargados correctamente!', 'info')
        return redirect(url_for('informes'))
