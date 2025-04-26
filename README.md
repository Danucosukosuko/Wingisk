# Wingisk

![WingiskRooted](https://github.com/user-attachments/assets/c76b25f5-bec9-4236-a24a-24c5b285e6b3)

# Wingisk Manager - Paquete ZIP

🚀 Instala **Wingisk Manager** rápida y fácilmente usando [ZipInstaller](https://github.com/ZipInstaller).

## ¿Qué es esto?

Este es el **paquete ZIP** de Wingisk Manager.  
Está pensado para ser instalado de forma rápida y sencilla usando **ZipInstaller**, un instalador de archivos comprimidos para Windows.

> Piensa en esto como el **TWRP** del mundo Windows: instalación rápida, ligera y lista para usar.

## ¿Qué incluye el paquete?

- `wingiskmanager.exe` → El ejecutable principal.
- `psexec64.exe` → Necesario para la elevación de privilegios SYSTEM. ⚠️ No provisto en el paquete, pero se descarga automáticamente

## Requisitos

- Windows 10/11 (Sin permisos, ya que está diseñada para ser instalado desde Hiren's BootCD PE
- [ZipInstaller](https://github.com/ZipInstaller) descargado y listo para usar.

## Instalación
1. Usa un entorno como Hiren's BootCD PE
2. Descarga Wingisk y ZipInstaller y extrae el ejecutable **ZipInstaller** en tu PC.
3. Ejecuta `ZipInstaller.exe`.
4. Selecciona el **paquete ZIP** de Wingisk Manager.
5. Espera a que termine la instalación, ya que es automática.
6. ¡Listo! El acceso root quedará instalado. Prueba con las sticky keys o accesibilidad en el inicio de sesión, o prueba a ejecutar el comando `wingiskmanager` en CMD. Te pedirá elevación por contraseña del usuario actual. Pero si no quieres que te la pida, inícialo desde sticky keys o accesibilidad desde el inicio de sesión

## Modo de uso

Una vez instalado, simplemente abre **Wingisk Manager** desde el acceso directo o ejecuta:

# 🚀 Herramienta para la gestión avanzada de Windows como SYSTEM.

## Funcionalidades

- Elevación automática a SYSTEM usando PsExec.
- Creación de un usuario oculto con privilegios altos (`wingisk`).
- Activación de la cuenta "Administrador" oculta de Windows.
- Desactivación rápida de Windows Defender.
- Shells interactivas como SYSTEM (CMD y PowerShell).
- Toma de propiedad y eliminación de archivos/carpeta protegidos.
- API WebSocket que se inicia por TCP

## Uso

### Ejecución normal

```cmd
wingiskmanager.exe
```

Te pedirá elevar permisos automáticamente si no eres SYSTEM.

### Ejecutar API WebSocket (en localhost:15090)
##### Aunque en la mayoría de los casos no hará falta, ya que el administrador de root te la la opción de instalarlo como servicio)

```cmd
wingiskmanager.exe --api
```

- El servidor escucha comandos de ejecución en el puerto **15090**.
- Por defecto, **solo local** (127.0.0.1).

## Comunicación con la API WebSocket

Para lanzar un programa a través de la API:

```python
import socket

def lanzar_programa(ruta):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 15090))
    s.sendall(ruta.encode())
    respuesta = s.recv(4096)
    print("Respuesta:", respuesta.decode())
    s.close()

lanzar_programa("C:\Windows\System32\cmd.exe /c cmd.exe")
```

### Notas de seguridad

- El acceso de la API es libre para toda la red local. Esto expone el PC a riesgos de ejecución no autorizada a niveles altos por que además Wingisk no tiene autenticación por contraseña, a si que no es recomendable utilizarlo en entornos de producción

## Importante

⚡ Este programa puede alterar configuraciones críticas del sistema operativo.

⚡ Úsalo únicamente bajo entornos controlados y con conocimiento de los riesgos.

---

Made with ❤️ by Pablo.
