#!/bin/bash

# Activar entorno virtual
source todo-list-aws/bin/activate

# Habilitar modo detallado
set -x

# Establecer PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH: $PYTHONPATH"

# Establecer variable de entorno para la tabla de DynamoDB
export DYNAMODB_TABLE=todoUnitTestsTable

# Ejecutar pruebas unitarias con Python
python test/unit/TestToDo.py

# Mostrar información de cobertura
pip show coverage
coverage run --include=src/todoList.py test/unit/TestToDo.py
coverage report -m
coverage xml

# Generar informe XML compatible con Cobertura
coverage xml -o coverage.xml

# Analizar el informe XML de Cobertura para mostrar las líneas no cubiertas
coverage report --show-missing
