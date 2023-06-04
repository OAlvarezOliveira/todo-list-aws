import warnings
import unittest
import boto3
from moto import mock_dynamodb
import sys
import os
import json
from unittest import mock

@mock_dynamodb
class TestDBFunctions(unittest.TestCase):
    def setUp(self):
        print ('---------------------')
        print ('Start: setUp')
        warnings.filterwarnings(
            "ignore",
            category=ResourceWarning,
            message="unclosed.*<socket.socket.*>")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="callable is None.*")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="Using or importing.*")
        """Create the mock database and table"""
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.is_local = 'true'
        self.uuid = "e8761243-9be8-3d12-456a-426614174000"
        self.text = "Aprender DevOps y Cloud en la UNIR"

        from src.todoList import create_todo_table
        self.table = create_todo_table(self.dynamodb)
        #self.table_local = create_todo_table()
        print ('End: setUp')

    def tearDown(self):
        print ('---------------------')
        print ('Start: tearDown')
        """Delete mock database and table after test is run"""
        self.table.delete()
        print ('Table deleted succesfully')
        #self.table_local.delete()
        self.dynamodb = None
        print ('End: tearDown')

    def test_table_exists(self):
        print ('---------------------')
        print ('Start: test_table_exists')
        #self.assertTrue(self.table)  # check if we got a result
        #self.assertTrue(self.table_local)  # check if we got a result

        print('Table name:' + self.table.name)
        tableName = os.environ['DYNAMODB_TABLE'];
        # check if the table name is 'ToDo'
        self.assertIn(tableName, self.table.name)
        #self.assertIn('todoTable', self.table_local.name)
        print ('End: test_table_exists')
        

    def test_put_todo(self):
        print ('---------------------')
        print ('Start: test_put_todo')
        # Testing file functions
        from src.todoList import put_item
        # Table local
        response = put_item(self.text, self.dynamodb)
        print ('Response put_item:' + str(response))
        self.assertEqual(200, response['statusCode'])
        # Table mock
        #self.assertEqual(200, put_item(self.text, self.dynamodb)[
        #                 'ResponseMetadata']['HTTPStatusCode'])
        print ('End: test_put_todo')

    def test_put_todo_error(self):
        print ('---------------------')
        print ('Start: test_put_todo_error')
        # Testing file functions
        from src.todoList import put_item
        # Table mock
        self.assertRaises(Exception, put_item("", self.dynamodb))
        self.assertRaises(Exception, put_item("", self.dynamodb))
        print ('End: test_put_todo_error')

    def test_get_todo(self):
        print ('---------------------')
        print ('Start: test_get_todo')
        from src.todoList import get_item
        from src.todoList import put_item

        # Testing file functions
        # Table mock
        responsePut = put_item(self.text, self.dynamodb)
        print ('Response put_item:' + str(responsePut))
        idItem = json.loads(responsePut['body'])['id']
        print ('Id item:' + idItem)
        self.assertEqual(200, responsePut['statusCode'])
        responseGet = get_item(
                idItem,
                self.dynamodb)
        print ('Response Get:' + str(responseGet))
        self.assertEqual(
            self.text,
            responseGet['text'])
        print ('End: test_get_todo')
    
    def test_list_todo(self):
        print ('---------------------')
        print ('Start: test_list_todo')
        from src.todoList import put_item
        from src.todoList import get_items

        # Testing file functions
        # Table mock
        put_item(self.text, self.dynamodb)
        result = get_items(self.dynamodb)
        print ('Response GetItems' + str(result))
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0]['text'] == self.text)
        print ('End: test_list_todo')


    def test_update_todo(self):
        print ('---------------------')
        print ('Start: test_update_todo')
        from src.todoList import put_item
        from src.todoList import update_item
        from src.todoList import get_item
        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
        # Testing file functions
        # Table mock
        responsePut = put_item(self.text, self.dynamodb)
        print ('Response PutItem' + str(responsePut))
        idItem = json.loads(responsePut['body'])['id']
        print ('Id item:' + idItem)
        result = update_item(idItem, updated_text,
                            "false",
                            self.dynamodb)
        print ('Result Update Item:' + str(result))
        self.assertEqual(result['text'], updated_text)
        print ('End: test_update_todo')


    def test_update_todo_error(self):
        print ('---------------------')
        print ('Start: atest_update_todo_error')
        from src.todoList import put_item
        from src.todoList import update_item
        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
        # Testing file functions
        # Table mock
        responsePut = put_item(self.text, self.dynamodb)
        print ('Response PutItem' + str(responsePut))
        self.assertRaises(
            Exception,
            update_item(
                updated_text,
                "",
                "false",
                self.dynamodb))
        self.assertRaises(
            TypeError,
            update_item(
                "",
                self.uuid,
                "false",
                self.dynamodb))
        self.assertRaises(
            Exception,
            update_item(
                updated_text,
                self.uuid,
                "",
                self.dynamodb))
        print ('End: atest_update_todo_error')

    def test_delete_todo(self):
        print ('---------------------')
        print ('Start: test_delete_todo')
        from src.todoList import delete_item
        from src.todoList import put_item
        from src.todoList import get_items
        # Testing file functions
        # Table mock
        responsePut = put_item(self.text, self.dynamodb)
        print ('Response PutItem' + str(responsePut))
        idItem = json.loads(responsePut['body'])['id']
        print ('Id item:' + idItem)
        delete_item(idItem, self.dynamodb)
        print ('Item deleted succesfully')
        self.assertTrue(len(get_items(self.dynamodb)) == 0)
        print ('End: test_delete_todo')

    def test_delete_todo_error(self):
        print ('---------------------')
        print ('Start: test_delete_todo_error')
        from src.todoList import delete_item
        # Testing file functions
        self.assertRaises(TypeError, delete_item("", self.dynamodb))
        print ('End: test_delete_todo_error') 
        
@mock_dynamodb
class TestDBFunctionsError(unittest.TestCase):
    def setUp(self):
        print ('---------------------')
        print ('Start: setUp')
        # Ignorar advertencias específicas durante las pruebas
        warnings.filterwarnings(
        "ignore",
        category=ResourceWarning,
        message="unclosed.*<socket.socket.*>")
        warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        message="callable is None.*")
        warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        message="Using or importing.*")
    
        # Crear la base de datos y la tabla simuladas
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.is_local = 'true'
        print('Fin: setUp')
        
        
    def test_get_todo_error(self):
        print('---------------------')
        print('Inicio: test_get_todo_error')
    
        # Importar la función get_item del archivo src/todoList.py
        from src.todoList import get_item
    
        # Simular la tabla
        self.table = table = mock.Mock()
    
        # Establecer el comportamiento de la función get_item para lanzar una excepción
        self.table.get_item.side_effect = Exception('Boto3 Exception')
    
        # Llamar a la función get_item con argumentos vacíos y el recurso dynamodb
        get_item("", self.dynamodb)
        print('Fin: test_get_todo_error')
        
    
    def test_put_todo_error(self):
        print('---------------------')
        print('Inicio: test_put_todo_error')
        
        # Importar la función put_item del archivo src/todoList.py
        from src.todoList import put_item
        
        # Simular la tabla
        self.assertRaises(Exception, put_item("", self.dynamodb))
        self.assertRaises(Exception, put_item("", self.dynamodb))
        
        print('Fin: test_put_todo_error')

    def test_update_todo_error(self):
        print('---------------------')
        print('Inicio: test_update_todo_error')
    
        # Importar las funciones put_item y update_item del archivo src/todoList.py
        from src.todoList import put_item, update_item
    
        self.text = "Aprender DevOps y Cloud en la UNIR"
        self.uuid = "e8761243-9be8-3d12-456a-426614174000"
        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
    
        # Llamar a la función put_item con el texto y el recurso dynamodb
        responsePut = put_item(self.text, self.dynamodb)
        print('Respuesta de put_item: ' + str(responsePut))
    
        # Lanzar excepciones específicas para probar la función update_item con diferentes argumentos
        self.assertRaises(Exception, update_item(updated_text, "", "false", self.dynamodb))
        self.assertRaises(TypeError, update_item("", self.uuid, "false", self.dynamodb))
        self.assertRaises(Exception, update_item(updated_text, self.uuid, "", self.dynamodb))
    
        print('Fin: test_update_todo_error')
     '''   
    def test_delete_todo_error(self):
        print('---------------------')
        print('Inicio: test_delete_todo_error')
    
        # Importar la función delete_item del archivo src/todoList.py
        from src.todoList import delete_item
    
        # Lanzar una excepción específica para pro
        # Probar la función delete_item con un argumento vacío y el recurso dynamodb
        self.assertRaises(TypeError, delete_item("", self.dynamodb))
    
        print('Fin: test_delete_todo_error')
    '''

if __name__ == '__main__':
    unittest.main()           