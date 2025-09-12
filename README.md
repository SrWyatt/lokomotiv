# LOKOMOTIV 
#### 1.4.1 (LÉTOV) - SNAPSHOT

Lokomotiv es una herramienta Python diseñada para estimar la **probabilidad de existencia**
de perfiles de usuarios en redes sociales de manera rápida y organizada.  
Permite realizar tres tipos de búsquedas: **básica**, **avanzada** y **personalizada**.

## Características principales

- **Búsqueda básica:** Escanea redes sociales populares (Facebook, Instagram, Twitter, YouTube, GitHub)
- **Búsqueda avanzada:** Escanea más de 100 sitios, con resultados categorizados por categoría
- **Búsqueda personalizada:** Permite usar un listado propio en `custom.json`
- **Guardado de resultados:** Posibilidad de exportar resultados en CSV con:
  - Sitio
  - Probabilidad de existencia
  - Tiempo de verificación
  - URL revisada

## Indicadores de resultados

- `[+]` Verde → Alta probabilidad de existencia 
- `[-]` Rojo  → Baja probabilidad de existencia 
- `E` → Porcentaje de existencia estimado
- `T` → Tiempo que tardó en verificar
- `P` → Progreso de la búsqueda
## Dependencias
```bash
   # Debian
    sudo apt update
    sudo apt install python3 python3-pip -y

    # Arch Linux
    sudo pacman -Syu python python-pip --noconfirm

    # Fedora
    sudo dnf install python3 python3-pip -y

    # Instalar requests
    pip install requests
```

## Instalación
```bash
    git clone https://github.com/SrWyatt/lokomotiv.git
    cd snapshot
    python3 snapshot.py
```

## Entorno virtual (opcional)
```bash
    cd lokomotiv
    python3 -m venv venv
    source venv/bin/activate
    pip install requests
    python3 lokomotiv.py
    deactivate
```




    
## Screenshots

![App Screenshot](https://raw.githubusercontent.com/SrWyatt/lokomotiv/refs/heads/main/screenshots/1.png)

![App Screenshot](https://raw.githubusercontent.com/SrWyatt/lokomotiv/refs/heads/main/screenshots/2.png)

