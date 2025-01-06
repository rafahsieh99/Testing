import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f'El servidor esta en linea {host}: {port}')

clientes = []
usuarios = []

def transmision(mensaje, _cliente=None):
    for cliente in clientes:
        if _cliente is None or cliente != _cliente:
            try:
                cliente.send(mensaje)
            except:
                # Si falla el envío, ignoramos ese cliente
                pass

def manejo_mensajes(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)
            if not mensaje:  # Si el mensaje está vacío, el cliente se desconectó
                raise Exception("Cliente desconectado")
            transmision(mensaje, cliente)
        except:
            try:
                index = clientes.index(cliente)
                usuario = usuarios[index]
                transmision(f'Chat: {usuario} se desconecto'.encode('utf-8'))
                clientes.remove(cliente)
                usuarios.remove(usuario)
            except:
                pass  # Si el cliente ya fue removido, ignoramos el error
            finally:
                try:
                    cliente.close()
                except:
                    pass
            break

def recibir_conecciones():
    while True:
        try:
            cliente, addres = server.accept()
            cliente.send('@usuario'.encode('utf-8'))
            usuario = cliente.recv(1024).decode('utf-8')

            clientes.append(cliente)
            usuarios.append(usuario)

            print(f'{usuario} estas conectado con {str(addres)}')

            mensaje = f'Chat: {usuario} se unio al chat'.encode('utf-8')
            transmision(mensaje, cliente)
            cliente.send('Conectado al servidor'.encode('utf-8'))

            thread = threading.Thread(target=manejo_mensajes, args=(cliente,))
            thread.start()
        except Exception as e:
            print(f"Error al aceptar conexión: {e}")

if __name__ == '__main__':
    recibir_conecciones()
