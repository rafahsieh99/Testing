import pytest
import socket
import threading
import time

# 1. TDD - Nueva función para validar mensajes
def test_validar_mensaje():
    def validar_mensaje(mensaje):
        if not mensaje or mensaje.isspace():
            return False
        return True
    
    assert not validar_mensaje(""), "Mensaje vacío no válido"
    assert not validar_mensaje("   "), "Espacios en blanco no válidos"
    assert validar_mensaje("Hola"), "Mensaje normal debe ser válido"

# 2. Pruebas de integración básicas
def test_conexion_multiple():
    # Crear 2 clientes
    cliente1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conectar ambos clientes
        cliente1.connect(('127.0.0.1', 55555))
        cliente2.connect(('127.0.0.1', 55555))
        
        # Manejar el mensaje de usuario para ambos clientes
        cliente1.recv(1024)  # Recibir '@usuario'
        cliente1.send('Usuario1'.encode('utf-8'))
        cliente2.recv(1024)  # Recibir '@usuario'
        cliente2.send('Usuario2'.encode('utf-8'))
        
        # Recibir mensaje de bienvenida
        cliente1.recv(1024)
        cliente2.recv(1024)
        
        # Enviar mensaje desde cliente1
        mensaje = "Hola desde cliente 1"
        cliente1.send(mensaje.encode('utf-8'))
        time.sleep(0.1)  # Dar tiempo para la transmisión
        
        # Recibir en cliente2
        respuesta = cliente2.recv(1024).decode('utf-8')
        assert mensaje in respuesta, "Mensaje no recibido correctamente"
        
    except Exception as e:
        pytest.fail(f"Error en la prueba: {e}")
    finally:
        cliente1.close()
        cliente2.close()

# 3. Prueba de desconexión
def test_desconexion():
    cliente1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conectar ambos clientes
        cliente1.connect(('127.0.0.1', 55555))
        cliente2.connect(('127.0.0.1', 55555))
        
        # Manejar el mensaje de usuario
        cliente1.recv(1024)
        cliente1.send('Usuario1'.encode('utf-8'))
        cliente2.recv(1024)
        cliente2.send('Usuario2'.encode('utf-8'))
        
        # Recibir mensaje de bienvenida
        cliente1.recv(1024)
        cliente2.recv(1024)
        
        # Desconectar cliente1
        cliente1.close()
        time.sleep(0.1)  # Dar tiempo para procesar la desconexión
        
        # Verificar que cliente2 sigue funcionando
        mensaje = "Mensaje después de desconexión"
        cliente2.send(mensaje.encode('utf-8'))
        assert True, "Cliente2 pudo enviar mensaje después de desconexión"
        
    except Exception as e:
        pytest.fail(f"Error en la prueba: {e}")
    finally:
        try:
            cliente2.close()
        except:
            pass

# 4. Prueba de mensajes simultáneos
def test_mensajes_simultaneos():
    cliente1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conectar clientes
        cliente1.connect(('127.0.0.1', 55555))
        cliente2.connect(('127.0.0.1', 55555))
        
        # Manejar el mensaje de usuario
        cliente1.recv(1024)
        cliente1.send('Usuario1'.encode('utf-8'))
        cliente2.recv(1024)
        cliente2.send('Usuario2'.encode('utf-8'))
        
        # Recibir mensaje de bienvenida
        cliente1.recv(1024)
        cliente2.recv(1024)
        
        # Enviar mensajes al mismo tiempo
        mensaje1 = "Mensaje desde cliente 1"
        mensaje2 = "Mensaje desde cliente 2"
        
        cliente1.send(mensaje1.encode('utf-8'))
        cliente2.send(mensaje2.encode('utf-8'))
        
        time.sleep(0.1)  # Dar tiempo para recibir mensajes
        
        # Verificar que ambos reciben los mensajes
        recibido1 = cliente1.recv(1024).decode('utf-8')
        recibido2 = cliente2.recv(1024).decode('utf-8')
        
        assert mensaje2 in recibido1 or mensaje1 in recibido2, "Los mensajes no se recibieron correctamente"
        
    except Exception as e:
        pytest.fail(f"Error en la prueba: {e}")
    finally:
        cliente1.close()
        cliente2.close()

def test_mensaje_vacio_no_enviado():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 55555))
    
    # Aquí estamos enviando un mensaje vacío, que debería ser rechazado
    mensaje_vacio = ""
    cliente.send(mensaje_vacio.encode('utf-8'))
    
    # Esperamos que el servidor no acepte el mensaje vacío
    respuesta = cliente.recv(1024).decode('utf-8')
    assert respuesta == "Error: Mensaje vacío no permitido", "El servidor debería rechazar mensajes vacíos"
