import os
import ctypes
import subprocess
import sys
import getpass
import winreg as reg
import signal
import atexit

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_to_system():
    print("[*] Elevando a SYSTEM con PsExec...")
    args = [
        "psexec64", "-i", "-s", sys.executable, " ".join(sys.argv)
    ]
    subprocess.run(args, shell=True)

def is_system():
    return getpass.getuser().lower() == "system"

def create_wingisk_user():
    print("[*] Creando el usuario wingisk con privilegios NT AUTHORITY...")
    username = "wingisk"
    password = "Wingisk@2025"  # Puedes hacer esto aleatorio o pedir al usuario

    os.system(f"net user {username} {password} /add")
    os.system(f"net localgroup SYSTEM {username} /add")
    print(f"[+] Usuario '{username}' creado y añadido a Administrators.")
    print(f"[+] Puedes iniciar sesión con el usuario '{username}' y contraseña '{password}'.")

def check_registry():
    # Intentamos acceder al registro, si no existe lo creamos
    try:
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"SOFTWARE\Wingisk", 0, reg.KEY_READ)
        value, _ = reg.QueryValueEx(registry_key, "Open")
        reg.CloseKey(registry_key)
        return value
    except FileNotFoundError:
        return None  # Si la clave no existe, devolvemos None

def set_registry(value):
    # Establecemos el valor del registro Open
    registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"SOFTWARE\Wingisk", 0, reg.KEY_WRITE)
    reg.SetValueEx(registry_key, "Open", 0, reg.REG_SZ, str(value))
    reg.CloseKey(registry_key)

def root_menu():
    while True:
        print("\n🚀 WINGISK - Root Menu (SYSTEM)")
        print("1. Listar procesos")
        print("2. Mostrar usuarios")
        print("3. Shell interactiva (cmd)")
        print("4. Activar cuenta Administrador oculta")
        print("5. Desactivar Windows Defender")
        print("6. Tomar control de archivo o carpeta")
        print("7. Eliminar archivo/carpeta protegida")
        print("8. Shell PowerShell como SYSTEM")
        print("9. Crear usuario Wingisk (NT AUTHORITY)")
        print("10. Salir")

        opt = input(">> ")

        if opt == "1":
            os.system("tasklist")
        elif opt == "2":
            os.system("net user")
        elif opt == "3":
            os.system("cmd")
        elif opt == "4":
            os.system("net user Administrator /active:yes")
            print("[+] Cuenta Administrador activada.")
        elif opt == "5":
            os.system("powershell Set-MpPreference -DisableRealtimeMonitoring $true")
            print("[+] Defender desactivado.")
        elif opt == "6":
            path = input("Ruta del archivo o carpeta: ")
            os.system(f"takeown /f \"{path}\" /a /r /d y")
            os.system(f"icacls \"{path}\" /grant Administrators:F /t")
        elif opt == "7":
            path = input("Archivo o carpeta a eliminar: ")
            os.system(f"takeown /f \"{path}\" /a /r /d y")
            os.system(f"icacls \"{path}\" /grant Administrators:F /t")
            os.system(f"rmdir /s /q \"{path}\"" if os.path.isdir(path) else f"del /f /q \"{path}\"")
        elif opt == "8":
            os.system("powershell")
        elif opt == "9":
            create_wingisk_user()
        elif opt == "10":
            print("👋 Saliendo de Wingisk...")
            break
        else:
            print("Opción inválida.")

def cleanup():
    print("[*] Cerrando el programa. Restableciendo el valor del registro a 0.")
    set_registry(0)

if __name__ == "__main__":
    # Registra la función cleanup para ser llamada cuando el programa se cierre
    atexit.register(cleanup)

    # Maneja la señal SIGINT (Ctrl+C) para llamar a cleanup
    signal.signal(signal.SIGINT, lambda signal, frame: cleanup() or sys.exit(0))

    print("\n🌟 WINGISK - Windows Root Manager\n")

    # Comprobar si el registro existe y es 1
    reg_value = check_registry()

    if reg_value is None or reg_value == 0:
        # Si el registro no existe o tiene el valor 0, se ejecuta PsExec para elevar
        print("[*] No se ha encontrado la clave de registro o está en 0. Elevando con PsExec...")
        elevate_to_system()
        sys.exit()  # Terminamos la ejecución aquí, ya que el proceso ha sido elevado

    else:
        # Si el valor del registro es 1, entramos directamente al menú
        print("[*] Saltando la verificación de elevación y entrando al menú.")
        root_menu()
        set_registry(0)  # Cambiar el valor de Open a 0 después de entrar al menú
