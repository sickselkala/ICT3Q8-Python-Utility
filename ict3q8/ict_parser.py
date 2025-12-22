'''
@author: selkala (19/12/2025)
versione 1.3
License: MIT (see LICENSE file)
'''

# coding=utf-8
import csv
import struct
import os
from collections import Counter
from ict3q8.ict_map import PERFORMANCE_MAP, ERROR_MAP

def parse_performance_log(raw_hex_string):
    '''Analizza la stringa Hex del Performance Log.'''
    clean_hex = raw_hex_string.replace(" ", "").replace("-", "").replace("\n", "").replace("\r", "")
    
    try:
        data_bytes = bytes.fromhex(clean_hex)
    except ValueError:
        return [{"Error": "Invalid Hex String"}]

    results = []
    
    for offset, length, desc in PERFORMANCE_MAP:
        if offset + length <= len(data_bytes):
            chunk = data_bytes[offset : offset + length]
            if length == 4:
                value = struct.unpack(">I", chunk)[0]
            elif length == 2:
                value = struct.unpack(">H", chunk)[0]
            else:
                value = chunk.hex()
                
            results.append({
                "Offset": offset,
                "Description": desc,
                "Value": value
            })
            
    return results

def parse_error_log(raw_hex_string):
    '''Analizza la stringa Hex dell'Error Log.'''
    clean_hex = raw_hex_string.replace(" ", "").replace("-", "").replace("\n", "").replace("\r", "")
    try:
        data_bytes = bytes.fromhex(clean_hex)
    except ValueError:
        return []

    errors = []
    RECORD_SIZE = 5 
    
    for i in range(0, len(data_bytes), RECORD_SIZE):
        chunk = data_bytes[i : i + RECORD_SIZE]
        if len(chunk) < RECORD_SIZE: break
        
        try:
            cmd_part = chunk[0:3].decode('ascii', errors='ignore')
            err_code = chunk[3:5].decode('ascii', errors='ignore')
            
            if cmd_part == '\x00\x00\x00': continue
            
            desc = ERROR_MAP.get(err_code, "Errore sconosciuto")
            
            errors.append({
                "Index": i // RECORD_SIZE,
                "Command": cmd_part,
                "Code": err_code,
                "Description": desc
            })
        except:
            continue
    return errors

# --- FUNZIONI DI EXPORT ---

def crea_report_unico(perf_data, error_data, filename="Sankyo_Full_Report.csv"):
    '''Export unico con separatore ; e SOMMARIO ERRORI'''
    try:
        full_path = os.path.abspath(filename)
        print(f"   [INFO] Tentativo di scrittura in: {full_path}")

        with open(filename, 'w', newline='') as f:
            
            # --- SEZIONE 1: PERFORMANCE ---
            f.write("--- REPORT PERFORMANCE LOG ---\n")
            if perf_data:
                keys = perf_data[0].keys() 
                writer = csv.DictWriter(f, fieldnames=keys, delimiter=';')
                writer.writeheader()
                writer.writerows(perf_data)
            else:
                f.write("Nessun dato.\n")
            
            f.write("\n\n") 
            
            # --- SEZIONE 2: SOMMARIO ERRORI  ---
            f.write("--- SOMMARIO ERRORI (Riepilogo) ---\n")
            if error_data:
                # lista di stringhe "Codice - Descrizione" per contarle
                descrizioni = [f"{row['Code']} - {row['Description']}" for row in error_data]
                conteggio = Counter(descrizioni)
                
                # intestazione
                f.write("Quantita;Tipo Errore\n")
                
                # risultati ordinati dal più frequente
                for errore_tipo, quantita in conteggio.most_common():
                    f.write(f"{quantita};{errore_tipo}\n")
            else:
                f.write("Nessun errore da riepilogare.\n")

            f.write("\n\n")

            # --- SEZIONE 3: LISTA ERRORI DETTAGLIATA ---
            f.write("--- REPORT ERROR LOG (Dettaglio Eventi) ---\n")
            if error_data:
                keys = error_data[0].keys()
                writer = csv.DictWriter(f, fieldnames=keys, delimiter=';')
                writer.writeheader()
                writer.writerows(error_data)
            else:
                f.write("Nessun errore.\n")
                
        print(f"\n   [EXPORT OK] File creato correttamente!")
        
    except Exception as e:
        print(f"\n   [ERRORE CRITICO] Impossibile scrivere il file.")
        print(f"   Dettaglio errore sistema: {e}")