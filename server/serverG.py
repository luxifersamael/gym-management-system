import socket
import json
import threading
import signal
import config

is_running = True


def inoltra_a_serverA(richiesta):
    """Inoltra una richiesta a ServerA e restituisce la risposta."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_a_socket:
            server_a_socket.connect((config.HOST, config.PORT_SERVERA))
            server_a_socket.send(json.dumps(richiesta).encode('utf-8'))
            risposta = server_a_socket.recv(1024).decode('utf-8')
            return json.loads(risposta)
    except Exception as e:
        print(f"Errore durante l'inoltro a ServerA: {e}")
        return {'status': 'errore', 'message': 'Errore nella comunicazione con ServerA'}


def gestisci_connessione(client_socket):
    """Elabora una connessione client."""
    try:
        data = client_socket.recv(1024).decode('utf-8')
        richiesta = json.loads(data)
        risposta = inoltra_a_serverA(richiesta)
        client_socket.send(json.dumps(risposta).encode('utf-8'))
    except Exception as e:
        print(f"Errore nella connessione: {e}")
    finally:
        client_socket.close()


def avvia_server():
    """Avvia il server."""
    global is_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Riutilizzo della porta
    server_socket.bind((config.HOST, config.PORT_SERVERG))
    server_socket.settimeout(1)  # Timeout di 1 secondo per evitare blocchi su accept()
    server_socket.listen(10)
    print(f"ServerG in ascolto su {config.HOST}:{config.PORT_SERVERG}")

    try:
        while is_running:
            try:
                # Accetta connessioni in arrivo
                client_socket, addr = server_socket.accept()
                print(f"Connessione accettata da {addr}")
                thread = threading.Thread(target=gestisci_connessione, args=(client_socket,))
                thread.start()
            except socket.timeout:
                # Timeout scaduto, verifica lo stato di is_running
                continue
            except Exception as e:
                print(f"Errore nel server: {e}")
    except KeyboardInterrupt:
        print("\nInterruzione ricevuta, spegnimento del server...")
        is_running = False
    finally:
        server_socket.close()
        print("ServerG terminato.")


def gestisci_sigint(sig, frame):
    """Gestisce l'interruzione SIGINT per spegnere il server."""
    global is_running
    print("\nInterruzione ricevuta. Spegnimento del server...")
    is_running = False


if __name__ == '__main__':
    signal.signal(signal.SIGINT, gestisci_sigint)
    avvia_server()
