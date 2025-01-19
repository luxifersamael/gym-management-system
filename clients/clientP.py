import socket
import json
import config

def verifica_abbonamento():
    """Verifica lo stato di un abbonamento tramite ID."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((config.HOST, config.PORT_SERVERG))

    id_abbonamento = int(input("Inserisci l'ID dell'abbonamento: "))

    richiesta = {
        'azione': 'verifica',
        'id': id_abbonamento
    }

    client_socket.send(json.dumps(richiesta).encode('utf-8'))
    risposta = json.loads(client_socket.recv(1024).decode('utf-8'))

    if risposta['status'] == 'successo':
        dati = risposta['dati']
        print(f"Abbonamento trovato: ID={dati['id']}, Cliente={dati['nome_cliente']}, Stato={dati['stato']}")
    else:
        print("Errore:", risposta['message'])

    client_socket.close()

if __name__ == '__main__':
    verifica_abbonamento()
