# ICT3Q8-Python-Utility
Un driver Python completo e un analizzatore di log per il lettore di carte motorizzato **Sankyo ICT3Q8**. Questo progetto permette di controllare il dispositivo via seriale, gestire l'espulsione/ritiro carte e scaricare/decodificare i log di errore e performance senza l'ausilio di software proprietari.

## Funzionalità
- Connessione seriale RS232 (gestione parità e handshake).
- Comandi di base: Inizializzazione, Get Version, Espulsione (Fronte/Retro).
- **Log Parsing Avanzato**: Scarica i Performance Log ed Error Log.
- **Export CSV**: Genera report dettagliati decodificando i codici esadecimali in descrizioni leggibili.


## Requisiti
- Python 3.x
- Libreria `pyserial`

## Crediti e Attribuzione
Questo progetto si basa sulla libreria originale `ict3q8` creata da **Bert** (2018).
Il codice originale è stato:
1.  **Aggiornato** per Python 3 moderni.
2.  **Corretto** nella gestione dei protocolli di Log (CfA/CfC).
3.  **Esteso** con i moduli `ict_map` e `ict_parser` per la decodifica dei dati.

## Installazione
1. Clona la repo.
2. Esegui `pip install pyserial` (o usa la cartella locale inclusa).
3. Esegui `python main.py`.

## Disclaimer
Software fornito "così com'è" per scopi di test e diagnostica. Non affiliato con Sankyo.
