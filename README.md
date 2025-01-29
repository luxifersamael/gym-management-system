
# Progetto reti



## Configurazione

Per far funzionare il progetto esegui i seguenti comandi:

```bash
  git clone https://github.com/luxifersamael/gym-management-system.git
```
Entra nella cartella
```bash
  cd gym-management-system.git
```
Crea ambiente virtuale
```bash
  python -m venv .venv
```
Attiva l'ambiente (windows)
```bash
  .venv\Scripts\activate
```
Inizializza DB se già inizializzato avvia solo il server con lo stesso comando
```bash
  python server/serverA.py
```
Avvia serverG
```bash
  python server/serverG.py
```
Registra un nuovo abbonamento
```bash
  python clients/Palestra.py
```
Per verificare un abbonamento
```bash
  python clients/clientP.py
```
Per modificare lo stato di un abbonamento
```bash
  python clients/clientM.py
```


# Struttura del Progetto

Questa sezione descrive l'organizzazione del progetto, con un'overview della struttura dei file e delle directory.


```plaintext
gym-management-system/
├── server/
│   ├── serverA.py           # Server principale per la gestione degli abbonamenti
│   ├── serverG.py           # Server intermedio per verifiche
├── clients/
│   ├── Palestra.py          # Client per registrare abbonamenti
│   ├── clientP.py           # Client per verificare abbonamenti
│   ├── clientM.py           # Client per modificare lo stato degli abbonamenti
├── database/
│   ├── abbonamenti.db       # Database SQLite per gli abbonamenti
├── README.md                # Documentazione del progetto
└── config.py                # File di configurazione (porte, host)
```

## Authors

- [@luxifersamael](https://www.github.com/luxifersamael)
- [@sungvzer](https://www.github.com/sungvzer)
- [@OFamos](https://www.github.com/OFamos)
- [@munery](https://www.github.com/munery)
