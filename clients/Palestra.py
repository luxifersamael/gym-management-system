import socket
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import config

def registra_abbonamento():
    """Registra un nuovo abbonamento."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((config.HOST, config.PORT_SERVERA))

    nome_cliente = input("Inserisci nome cliente: ")
    durata = int(input("Inserisci durata (in mesi): "))

    richiesta = {
        'azione': 'registra',
        'nome_cliente': nome_cliente,
        'durata': durata
    }

    client_socket.send(json.dumps(richiesta).encode('utf-8'))
    risposta = json.loads(client_socket.recv(1024).decode('utf-8'))
    print("Risposta del server:", risposta['message'])
    print("ID assegnato:", risposta['id'])
    client_socket.close()

if __name__ == '__main__':
    registra_abbonamento()
