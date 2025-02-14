# Proyecto BATSEJ OPEN FINANCE S.A

## Documentación

Toda la documentación del código se encuentra en la carpeta `documentacion`. Dentro de esta carpeta encontrarás un archivo PDF que explica detalladamente el funcionamiento del aplicativo, sus características y su estructura.

## Notas importantes

Si realizas alguna modificación en el proyecto, puedes generar nuevamente el ejecutable utilizando el siguiente comando desde la carpeta raíz del proyecto:

```bash
pyinstaller --onefile --add-data "data/database.sqlite;data" src/main.py
