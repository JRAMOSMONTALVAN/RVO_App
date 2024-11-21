import subprocess
import time

# Espera un poco antes de abrir el navegador
time.sleep(2)

# Intenta abrir el navegador utilizando subprocess
subprocess.run(['start', 'http://127.0.0.1:5000'], shell=True)
