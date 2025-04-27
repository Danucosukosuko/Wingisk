# Wingisk

![WingiskRooted](https://github.com/user-attachments/assets/c76b25f5-bec9-4236-a24a-24c5b285e6b3)

![Made With Python](https://img.shields.io/badge/Made_with-Love-red)
![GitHub Downloads (all assets, latest release)](https://img.shields.io/github/downloads/danucosukosuko/Wingisk/latest/total)

# Wingisk Manager - Paquete ZIP

🚀 Instala **Wingisk Manager** rápidamente usando [ZipInstaller](https://github.com/danucosukosuko/ZipInstaller).

---

## ¿Qué es esto?

Este es el **paquete ZIP** de Wingisk Manager, diseñado para instalarse de forma rápida usando **ZipInstaller**, un instalador de archivos comprimidos para Windows.

> 📦 Piensa en esto como el **TWRP** del mundo Windows: instalación rápida, ligera y lista para usar. (ZipInstaller)
> 
> ⚠ Este paquete "rooteará" (te dará privilegios máximos de SYSTEM) a tu dispositivo con Windows, lo que lo puede hacer más inseguro. No lo uses en tu dispositivo 

---

## Contenido del paquete

| Archivo              | Descripción                                                        |
|----------------------|---------------------------------------------------------------------|
| `wingiskmanager.exe`  | Ejecutable principal de Wingisk Manager.                           |
| `psexec64.exe`        | Herramienta para elevación a SYSTEM (descarga automática, ya que PsExec es propiedad de Microsoft). |

---

## Requisitos

| Requisito        | Detalles                                  |
|------------------|-------------------------------------------|
| Sistema operativo | Windows 10/11                            |
| Permisos          | No necesarios (ideal en entornos PE)     |
| Herramientas      | [ZipInstaller](https://github.com/danucosukosuko/ZipInstaller) descargado |

---

## Instalación

| Paso | Instrucciones                                                              |
|-----:|---------------------------------------------------------------------------|
|  1.  | Arranca el equipo usando **Hiren's BootCD PE**.                           |
|  2.  | Descarga **Wingisk Manager** y **ZipInstaller**.                          |
|  3.  | Extrae y ejecuta `ZipInstaller.exe`.                                       |
|  4.  | Selecciona el paquete ZIP de Wingisk Manager.                             |
|  5.  | Deja que la instalación automática finalice.                              |
|  6.  | ¡Listo! Usa Sticky Keys o CMD (`wingiskmanager`) para abrirlo.             |

> Para omitir la contraseña de usuario, inicia Wingisk desde las herramientas de accesibilidad en la pantalla de login.

---

# Wingisk Manager

## Funcionalidades

| Funcionalidad                      | Descripción                                                               |
|-------------------------------------|---------------------------------------------------------------------------|
| 🚀 Elevación SYSTEM                 | Usa PsExec para elevar privilegios a SYSTEM.                              |
| 👤 Creación de usuario oculto       | Crea el usuario `wingisk` con privilegios de administrador.               |
| 🛠️ Activación de "Administrador"    | Activa la cuenta de Administrador oculta de Windows.                     |
| 🔥 Desactivación de Defender        | Desactiva Windows Defender fácilmente.                                   |
| 🖥️ Shells SYSTEM                    | CMD y PowerShell elevadas a SYSTEM.                                       |
| 📂 Gestión avanzada de archivos    | Tomar propiedad y eliminar archivos protegidos.                          |
| 🌐 Servidor API WebSocket           | Permite ejecución remota de comandos vía TCP (localhost:15090).          |

---

## Uso básico

| Comando                             | Acción                              |
|-------------------------------------|------------------------------------|
| `wingiskmanager.exe`                | Ejecución normal, solicita permisos si es necesario. |
| `wingiskmanager.exe --api`          | Lanza el servidor WebSocket en `127.0.0.1:15090`.    |

---

## Comunicación con la API WebSocket

### Ejemplo en Python

```python
import socket

def lanzar_programa(ruta):
    try:
        with socket.create_connection(("127.0.0.1", 15090)) as s:
            s.sendall(ruta.encode())
            respuesta = s.recv(4096)
            print("Respuesta:", respuesta.decode())
    except Exception as e:
        print("Error:", e)

lanzar_programa(r"C:\Windows\System32\cmd.exe /c cmd.exe")
```

| Detalle                 | Valor                |
|--------------------------|----------------------|
| Puerto                   | 15090                |
| Dirección                | 127.0.0.1 (localhost) |
| Autenticación            | ❌ No disponible      |
| Seguridad recomendada    | Cortafuegos o modificación del código |

---

## Notas de seguridad

⚠️ **Advertencia de uso**:

- La API WebSocket **no tiene autenticación** y es accesible en la red local.
- Se recomienda **no usar en producción** sin modificaciones de seguridad.
- Wingisk puede alterar configuraciones críticas de Windows.

---

## Resumen

| Característica             | Estado                         |
|-----------------------------|--------------------------------|
| Elevación de privilegios    | ✅ Automática |
| Instalación rápida          | ✅ Mediante ZipInstaller |
| Seguridad API               | ⚠️ No segura por defecto |
| Uso recomendado             | 🧪 Entornos de laboratorio, o en dispositivos aislados. |

---

**Made with ❤️ by Pablo.**

---  
