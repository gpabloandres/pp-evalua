from flask import Flask
from sqlalchemy import inspect, text

from config import Config
from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        migrate_evaluation_schema()

    from routes import register_routes
    register_routes(app)
    return app


def migrate_evaluation_schema():
    migrations = {
        'evaluaciones_estudiante': ['anio_evaluacion INTEGER', "periodo VARCHAR(20) DEFAULT 'no_especificado'"],
        'evaluaciones_profesor': ['anio_evaluacion INTEGER', "periodo VARCHAR(20) DEFAULT 'no_especificado'"],
        'evaluaciones_referente': [
            'anio_evaluacion INTEGER',
            "periodo VARCHAR(20) DEFAULT 'no_especificado'",
            'desempeno_adaptabilidad_tecnologica INTEGER',
        ],
    }

    with db.engine.begin() as connection:
        for table_name, definitions in migrations.items():
            existing_columns = {column['name'] for column in inspect(db.engine).get_columns(table_name)}
            for definition in definitions:
                column_name = definition.split()[0]
                if column_name not in existing_columns:
                    connection.execute(text(f'ALTER TABLE {table_name} ADD COLUMN {definition}'))

            connection.execute(text(
                f"UPDATE {table_name} "
                "SET anio_evaluacion = CAST(strftime('%Y', fecha_registro) AS INTEGER) "
                'WHERE anio_evaluacion IS NULL'
            ))


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
