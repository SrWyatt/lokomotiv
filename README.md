
# LOKOMOTIV

Lokomotiv es una herramienta Bash diseñada para realizar búsquedas de perfiles de usuarios en redes sociales de manera rápida y organizada. Permite realizar tres tipos de búsquedas: básica, avanzada y personalizada, ofreciendo un enfoque flexible según las necesidades del usuario.

### Características principales
- Búsqueda básica: Escanea las redes sociales más populares (Facebook, Instagram, Twitter, TikTok, GitHub y LinkedIn).

- Búsqueda avanzada: Escanea más de 100 redes sociales y sitios populares, con resultados categorizados.

- Búsqueda personalizada: Permite al usuario definir su propio listado de redes sociales mediante custom.txt.

- Resultados:

         Verde [+] → Perfil encontrado
    
         Naranja [-] → No encontrado o posible falso negativo

    Cabe aclarar que esta herramienta sigue en desarrollo por lo que algunas funciones no darán la respuesta que se espera.
    
    ⚠️ Solo para usos recreativos 


## Requerimento(s)

Necesitas el paquete "curl" instalado en el sistema.

```bash
 # Arch Linux
sudo pacman -Syu curl

# Debian
sudo apt install curl

# Fedora
sudo dnf install curl
```
    
## Instalacion
```bash
 git clone https://github.com/SrWyatt/lokomotiv.git
 cd lokomotiv
 chmod +x lokomotiv
 bash lokomotiv
```
## Screenshot
![App Screenshot](https://github.com/SrWyatt/lokomotiv/blob/main/screenshot/2.png)

    Dentro de "social.txt" se encuentran 100 de los sitios
    más populares en donde se pueden buscar a los usuarios
    ingresados.

    Si el sitio que buscas no está en esta lista puedes
    agregarlo en "custom.txt" siguiendo el instructivo
    dentro de tal archivo.

