## Bienvenidos a mi primer juego

# The Quest
Es un juego creado con el lenguaje: 
- **Python**

Y con la librería:
- **Pygame**

***
***

## Para poder instalarlo debes seguir los siguientes pasos:

### Mediante un archivo ZIP


1. Descarga el archivo ZIP desde el repositorio, con el botón verde **Code**. 

2. Descomprímelo y guárdalo en una carpeta en el escritorio.

3. Abre el proyecto con tu IDE preferido _(VSCode, VIM, etc.)_.
4. Instala lo necesario para ejecutar el juego desde el fichero **requirements.txt** con la funsion [pip](https://pip.pypa.io/en/stable/).
```powershell
pip install -r requirements.txt
```
5. Una vez instalada la librería **pygame**.

6. Ejecuta el fichero **Main.py**.

7. Puedes iniciar el juego con una base de datos limpia borrando el archivo **Records.db**, que se encuentra en la carpeta *data*.

***

### Mediante la función Git Clone


1. Copia el **URL** desde la sección **HTTPS**.

2. Ingresa a tu IDE preferido _(VSCode, VIM, etc.)_.

3. Abre la consola y ejecuta la función [git clone](https://support.atlassian.com/bitbucket-cloud/docs/clone-a-git-repository/).
```powershell
git clone "URL"
```
4. Instala lo necesario para ejecutar el juego desde el fichero **requirements.txt** con la función [pip](https://pip.pypa.io/en/stable/).
```powershell
pip install -r requirements.txt
```
5.  Una vez instalada la librería **pygame**.

6. Ejecuta el fichero **Main.py**.

7. Puedes iniciar el juego con una base de datos limpia borrando el archivo **Records.db**, que se encuentra en la carpeta *data*.

***
***
## Los controles son los siguientes:


Para mover la nave a través de los niveles:
- Flecha hacia arriba **UP**, para desplazarse hacia arriba.
- Flecha hacia abajo **DOWN**, para desplazarse hacia abajo.
- Para acelerar la velocidad de la nave debes presionar la tecla **Shift Izquierdo** en conjunto con la flecha de la dirección en la que deseas desplazarte.
- Para acelerar la velocidad de los meteoros debes presionar la tecla **Shift Derecho**.
- Para poner pausa o reanudar la musica presiona la tecla **1**.
- Para visualizar los controles al inicio del juego y durante el juego, presiona la tecla **2**.
***
***
## Las reglas del juego

- Al esquivar un meteoro, y que este llegue al límite izquierdo de la pantalla, se ganara 1 punto, por los pequeños, y 2 puntos por los grandes.
- Al llegar al mundo al final de cada nivel, recibes 5 puntos adicionales.
- Al chocar con un meteoro pequeño, perderás 1 vida y al chocar con uno grande perderás 2 vidas.
- Al quedarte sin vidas pierdes el juego.
- Si logras alcanzar un puntaje superior a los primeros 5, podrás grabar tus iniciales en la tabla de **Records**.

***
***

Sin más que agregar.

Disfruta el juego.

Cualquier observación o mejora es bienvenida.
***
***
Imagen del fuego de la nave: Image by rawpixel.com.

&copy; Juan Daniel Mejia Hoyos 2022