import socket
import json
import sqlite3
import threading
import signal
import config

is_running = True  # Variabile globale per il ciclo del server
lock = threading.Lock()  # Mutex per accesso sicuro al database


def inizializza_database():
    """Crea il database e la tabella abbonamenti se non esistono."""
    conn = sqlite3.connect('../database/abbonamenti.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS abbonamenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT NOT NULL,
            durata INTEGER NOT NULL,
            stato TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def gestisci_richiesta(richiesta):
    """Gestisce le richieste ricevute dai client."""
    print(f"Richiesta ricevuta: {richiesta}")
    conn = sqlite3.connect('../database/abbonamenti.db')
    cursor = conn.cursor()

    if richiesta['azione'] == 'registra':
        cursor.execute('''
            INSERT INTO abbonamenti (nome_cliente, durata, stato) 
            VALUES (?, ?, ?)
        ''', (richiesta['nome_cliente'], richiesta['durata'], 'attivo'))
        conn.commit()
        abbonamento_id = cursor.lastrowid
        conn.close()
        print(f"Abbonamento registrato con ID: {abbonamento_id}")
        return {'status': 'successo', 'message': 'Abbonamento registrato', 'id': abbonamento_id}

    elif richiesta['azione'] == 'verifica':
        cursor.execute('SELECT * FROM abbonamenti WHERE id = ?', (richiesta['id'],))
        abbonamento = cursor.fetchone()
        conn.close()
        if abbonamento:
            return {
                'status': 'successo',
                'dati': {
                    'id': abbonamento[0],
                    'nome_cliente': abbonamento[1],
                    'durata': abbonamento[2],
                    'stato': abbonamento[3]
                }
            }
        else:
            return {'status': 'errore', 'message': 'ID abbonamento non trovato'}

    elif richiesta['azione'] == 'modifica':
        cursor.execute('UPDATE abbonamenti SET stato = ? WHERE id = ?', (richiesta['stato'], richiesta['id']))
        conn.commit()
        conn.close()
        return {'status': 'successo', 'message': 'Stato aggiornato'}

    else:
        conn.close()
        return {'status': 'errore', 'message': 'Azione non riconosciuta'}


def gestisci_connessione(client_socket):
    """Elabora una connessione client."""
    try:
        data = client_socket.recv(1024).decode('utf-8')
        richiesta = json.loads(data)
        risposta = gestisci_richiesta(richiesta)
        client_socket.send(json.dumps(risposta).encode('utf-8'))
    except Exception as e:
        print(f"Errore nella connessione: {e}")
    finally:
        client_socket.close()


def avvia_server():
    """Avvia il server con gestione dei thread."""
    global is_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config.HOST, config.PORT_SERVERA))
    server_socket.listen(10)
    print(f"ServerA in ascolto su {config.HOST}:{config.PORT_SERVERA}")

    while is_running:
        try:
            client_socket, addr = server_socket.accept()
            print(f"Connessione accettata da {addr}")
            thread = threading.Thread(target=gestisci_connessione, args=(client_socket,))
            thread.start()
        except Exception as e:
            print(f"Errore nel server: {e}")

    server_socket.close()
    print("ServerA terminato.")


def gestisci_sigint(sig, frame):
    """Gestisce l'interruzione SIGINT per spegnere il server."""
    global is_running
    print("\nInterruzione ricevuta. Spegnimento del server...")
    is_running = False


if __name__ == '__main__':
    signal.signal(signal.SIGINT, gestisci_sigint)  # Imposta l'handler SIGINT
    inizializza_database()
    avvia_server()
