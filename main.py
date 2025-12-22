'''
Sankyo Utility Tool
Version: 1.0.0
Author: Selkala 2025
License: MIT (see LICENSE file)
'''
import os
import sys
import serial
from datetime import datetime

try:
    from ict3q8 import ict_ser as ict
    from ict3q8 import ict_cmds
    from ict3q8 import ict_parser 
except ImportError as e:
    print(f"ERRORE LIBRERIE: {e}")
    sys.exit(1)

class SankyoDriver:
    def __init__(self, port='COM1', baud=38400):
        self.port = port
        self.baud = baud
        self.ser = None
        self.tipo_banda = "N/D"

    def connetti(self):
        if self.ser and self.ser.is_open:
            print("Già connesso.")
            return True
        try:
            print(f"Connessione a {self.port}...")
            self.ser = serial.Serial(self.port, self.baud, serial.EIGHTBITS, serial.PARITY_EVEN, serial.STOPBITS_ONE, timeout=3, rtscts=True)
            self.ser.dtr = True; self.ser.rts = True
            print("Hardware pronto.")
            return True
        except Exception as e:
            print(f"Errore: {e}")
            return False

    def disconnetti(self):
        if self.ser: self.ser.close()
        self.ser = None

    def _check(self):
        if not self.ser or not self.ser.is_open:
            print("Non connesso."); return False
        return True

    def inizializza(self):
        if not self._check(): return
        print(">> Inizializzazione...")
        res = ict_cmds.ict_reset(self.ser)
        if res and res[0] == 0:
            print("   [OK] ACK Ricevuto.")
            if len(res) > 3:
                if res[3].startswith(b'2220110000100000'): self.tipo_banda = "HICO"
                elif res[3].startswith(b'2220010000100001'): self.tipo_banda = "LOCO"
        else:
            print(f"   [FAIL] Errore: {res}")

    def get_versione_fw(self):
        if not self._check(): return
        print(">> Versione FW...")
        print(f"   {ict.sendrecvICT(self.ser, b'CA1')}")

    # --- METODI VISUALIZZAZIONE RAPIDA (Dump a schermo) ---

    def get_performance(self):
        if not self._check(): return
        print(">> Performance Log (Dump)...")
        res = ict_cmds.performancelog(self.ser)
        if res and res[0] == 0 and len(res) > 3:
            ict_cmds.stampa_hex_dump(res[3], titolo="PERFORMANCE LOG")
        else:
            print(f"   [FAIL] Errore: {res}")

    def get_error(self):
        if not self._check(): return
        print(">> Error Log (Dump)...")
        for i in range(5):
            res = ict_cmds.errorlog(self.ser, page=i)
            if res and res[0] == 0 and len(res) > 3:
                ict_cmds.stampa_hex_dump(res[3], titolo=f"PAGINA {i}")

    # --- METODO REPORT UNICO ---

    def genera_report_unico(self):
        if not self._check(): return
        print("\n" + "="*50)
        print(" GENERAZIONE REPORT UNICO (Performance + Errori)")
        print("="*50)

        # 1. ACQUISIZIONE PERFORMANCE
        print(">> Acquisizione Performance Log...")
        res_perf = ict_cmds.performancelog(self.ser)
        
        perf_data = []
        if res_perf and res_perf[0] == 0 and len(res_perf) > 3:
            hex_perf = res_perf[3].hex().upper()
            perf_data = ict_parser.parse_performance_log(hex_perf)
            print(f"   [OK] Acquisiti {len(perf_data)} contatori.")
        else:
            print("   [FAIL] Impossibile leggere Performance Log.")

        # 2. ACQUISIZIONE ERRORI (Ciclo 5 pagine)
        print(">> Acquisizione Error Log (5 Pagine)...")
        full_err_hex = ""
        for i in range(5):
            print(f"   ...Pagina {i}...", end="\r")
            res_err = ict_cmds.errorlog(self.ser, page=i)
            if res_err and res_err[0] == 0 and len(res_err) > 3:
                full_err_hex += res_err[3].hex()
        
        error_data = []
        if full_err_hex:
            error_data = ict_parser.parse_error_log(full_err_hex)
            print(f"\n   [OK] Acquisiti {len(error_data)} eventi di errore.")
        else:
            print("\n   [WARN] Nessun dato errori trovato.")

        # 3. CREAZIONE FILE UNICO (SOLO UNA CHIAMATA)
        print(">> Scrittura file...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_file = f"Sankyo_Report_{timestamp}.csv"
        
        # Percorso Desktop
        import os
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        full_path = os.path.join(desktop_path, nome_file)
        
        # Unica chiamata corretta
        ict_parser.crea_report_unico(perf_data, error_data, full_path)

def main():
    driver = SankyoDriver()
    while True:
        print(f"\n--- SANKYO TOOL ({driver.tipo_banda}) ---")
        print("1. Connetti")
        print("2. Inizializza")
        print("3. Visualizza Performance (Dump)")
        print("4. Visualizza Errori (Dump)")
        print("5. Versione FW")
        print("6. GENERA REPORT UNICO (.csv)")
        print("0. Esci")
        
        sel = input("Scelta: ")
        if sel == '1': driver.connetti()
        elif sel == '2': driver.inizializza()
        elif sel == '3': driver.get_performance()
        elif sel == '4': driver.get_error()
        elif sel == '5': driver.get_versione_fw()
        elif sel == '6': driver.genera_report_unico()
        elif sel == '0': driver.disconnetti(); break

if __name__ == "__main__": main()