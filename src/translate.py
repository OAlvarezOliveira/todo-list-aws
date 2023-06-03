import json
import decimalencoder
import todoList


def translate(event, context):
    # Obtener el elemento de la lista de tareas mediante el ID proporcionado en los parámetros de la ruta
    item = todoList.get_item(event['pathParameters']['id'])
    print(json.dumps(event['pathParameters'], indent=4))  # Imprimir los parámetros de la ruta en formato JSON
    
    # Traducir el texto del elemento al idioma especificado en los parámetros de la ruta
    idioma = event['pathParameters']['idioma']
    traduccion = str(todoList.get_translate(item["text"], idioma))
    
    # Actualizar el texto del elemento con la traducción obtenida
    item["text"] = traduccion
    print("Traducción del texto:\n\r")
    print(json.dumps(item["text"], cls=decimalencoder.DecimalEncoder, indent=4))  # Imprimir la traducción en formato JSON
    
    # Crear la respuesta según si se encontró o no el elemento
    if item:
        response = {
            "statusCode": 200,
            "body": json.dumps(item, cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response
