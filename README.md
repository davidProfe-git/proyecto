# Juego de Tetris

Este es un juego de Tetris implementado en Python utilizando PyQt5. El juego incluye:
- Una interfaz gráfica con tetrominós coloridos.
- Mecánicas de eliminación de líneas y seguimiento de puntajes.
- Persistencia de los puntajes más altos entre sesiones.

## Características
- **Formas de Tetrominós**: Todas las formas estándar de Tetris (I, O, T, S, Z, J, L).
- **Eliminación de Líneas**: Las líneas horizontales completas se eliminan y el puntaje se actualiza.
- **Puntajes Altos**: Los puntajes más altos se guardan en un archivo `highscores.json`.
- **Controles del Teclado**:
  - Flecha Izquierda: Mover el tetrominó a la izquierda.
  - Flecha Derecha: Mover el tetrominó a la derecha.
  - Flecha Abajo: Hacer que el tetrominó caiga más rápido.
  - Barra Espaciadora: Rotar el tetrominó.

## Requisitos
- Python 3.14 o superior.
- Librería PyQt5.

## Instalación
1. Clona este repositorio o descarga los archivos del proyecto.
2. Asegúrate de tener Python 3.14 instalado en tu sistema.
3. Instala la librería requerida:
   ```bash
   pip install PyQt5
   ```

## Cómo Ejecutar
1. Navega al directorio del proyecto en tu terminal:
   ```bash
   cd C:/Users/David/Documents/2026-T1/inteligencia artificial/proyecto
   ```
2. Ejecuta el juego:
   ```bash
   python tetris.py
   ```
3. Usa los controles del teclado para jugar.

## Puntajes Altos
Los puntajes más altos se guardan en un archivo llamado `highscores.json` en el directorio del proyecto. Los puntajes más altos se muestran después de que termina el juego.

## Solución de Problemas
- Si el juego no inicia, asegúrate de que PyQt5 esté instalado correctamente ejecutando:
  ```bash
  pip show PyQt5
  ```
- Si encuentras algún problema, verifica que estás utilizando Python 3.14 o superior.

## Licencia
Este proyecto es de código abierto y está disponible bajo la Licencia MIT.