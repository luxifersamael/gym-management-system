import socket
import json
import config

def modifica_stato():
    """Modifica lo stato di un abbonamento."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((config.HOST, config.PORT_SERVERA))

    id_abbonamento = int(input("Inserisci l'ID dell'abbonamento: "))
    nuovo_stato = input("Inserisci il nuovo stato (attivo/sospeso): ").strip().lower()

    if nuovo_stato not in ['attivo', 'sospeso']:
        print("Stato non valido. Usa 'attivo' o 'sospeso'.")
        client_socket.close()
        return

    richiesta = {
        'azione': 'modifica',
        'id': id_abbonamento,
        'stato': nuovo_stato
    }

    client_socket.send(json.dumps(richiesta).encode('utf-8'))
    risposta = json.loads(client_socket.recv(1024).decode('utf-8'))
    print("Risposta del server:", risposta['message'])
    client_socket.close()

if __name__ == '__main__':
    modifica_stato()
