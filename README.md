# ICT3Q8-Python-Utility
Un driver Python completo e un analizzatore di log per il lettore di carte motorizzato **Sankyo ICT3Q8**. Questo progetto permette di controllare il dispositivo via seriale, gestire l'espulsione/ritiro carte e scaricare/decodificare i log di errore e performance senza l'ausilio di software proprietari.

## Funzionalità
- Connessione seriale RS232 (gestione parità e handshake).
- Comandi di base: Inizializzazione, Get Version, Espulsione (Fronte/Retro).
- **Log Parsing Avanzato**: Scarica i Performance Log ed Error Log.
- **Export CSV**: Genera report dettagliati decodificando i codici esadecimali in descrizioni leggibili.

##Architettura
graph TD
    Start((Avvio main.py)) --> Import{Import Librerie<br/>ict3q8};
    
    Import -- Errore --> ErrLib[Exit: Errore Librerie];
    Import -- OK --> InitClass[Istanza: SankyoDriver<br/>Porta: COM1];
    
    InitClass --> MenuLoop{Loop Menu<br/>Principale};
    
    MenuLoop --> |Mostra Opzioni| UserInput[/Input Utente/];
    
    UserInput -- "1" --> Conn[Connetti];
    Conn --> SerialCheck{Porta Aperta?};
    SerialCheck -- Si --> MenuLoop;
    SerialCheck -- No --> OpenSerial[Apertura pyserial<br/>con parametri Sankyo];
    OpenSerial --> HardwareReset[Reset Hardware];
    HardwareReset --> MenuLoop;
    
    UserInput -- "2" --> Init[Inizializza];
    Init --> CmdReset[Cmd: ict_reset];
    CmdReset --> CheckBanda{Analisi Risposta};
    CheckBanda -- "222...00" --> HiCo[Set: HICO];
    CheckBanda -- "222...01" --> LoCo[Set: LOCO];
    HiCo & LoCo --> MenuLoop;
    
    UserInput -- "3, 4, 5" --> Dumps[Comandi Rapidi<br/>Get FW / Dump Log a Video];
    Dumps --> MenuLoop;
    
    UserInput -- "6" --> Report[Genera Report Unico];
    
    subgraph "Logica Report (Scelta 6)"
        Report --> GetPerf[Get Performance Log<br/>Cmd: CfA];
        GetPerf --> ParsePerf[ict_parser: Analisi Hex];
        ParsePerf --> GetErr[Get Error Log<br/>Cmd: CfC Loop 0-4];
        GetErr --> ParseErr[ict_parser: Analisi Hex];
        ParseErr --> CreateCSV[ict_parser: Scrittura CSV<br/>su Desktop];
    end
    
    CreateCSV --> MenuLoop;
    
    UserInput -- "0" --> Disc[Disconnetti];
    Disc --> Close[Chiudi Porta Serial];
    Close --> End((Fine));
    
    style Start fill:#f9f,stroke:#333,stroke-width:2px
    style Report fill:#bbf,stroke:#333,stroke-width:2px
    style End fill:#f9f,stroke:#333,stroke-width:2px
    ```mermaid
graph TD
    A[Avvio] --> B{Menu};
    B -- 1 --> C[Connetti];
    B -- 2 --> D[Inizializza/Check HICO-LOCO];
    B -- 6 --> E[Genera Report CSV];
    E --> F[Performance Log Parsing];
    E --> G[Error Log Parsing x5];
    G --> H[Export Desktop];
    B -- 0 --> Z[Esci];

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
