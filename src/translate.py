import json
import decimalencoder
import todoList

def translate(event, context):
    # Obtener elemento todoList mediante el ID proporcionado pathParameters
    item = todoList.get_item(event['pathParameters']['id'])
    # Imprimir los parámetros de la ruta en formato JSON
    print(json.dumps(event['pathParameters'], indent=4))  
    
    # Traducir el texto del elemento al idioma especificado pathParameters
    idioma = event['pathParameters']['idioma']
    traduccion = str(todoList.get_translate(item["text"], idioma))
    
    # Actualizar el texto del elemento con la traducción 
    item["text"] = traduccion
    print("Traducción del texto:\n\r")
    # Imprimir la traducción en formato JSON
    print(json.dumps(item["text"], cls=decimalencoder.DecimalEncoder, indent=4))
    
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
