# Sistema de Gestión para Licorería 🍾  

Este proyecto es una **aplicación de gestión** para una licorería, desarrollada en **Python** con interacción a una base de datos desde **SQL** o si la migramos podemos trabajar con **PostgreSQL**. 

---
El programa permite realizar operaciones básicas sobre distintas tablas y facilitar la administración del negocio. Nos hemos enfocado a la administracion de una licoreria DRINKERS para facilitar el trabajo o ahorrar tiempo para la gestion de la misma
Usando herramientas como SQL Server, Postgre y Python. Presentamos una interfaz para el flujo de ventas, manejo de las mismas, control de empleados y clientes, de la misma forma llevar el control de los detalles de las ventas, el control de los stock de bebidas todo ya implementado para usarlo de manera optima
Presentamos una interfaz mas dinamica para el uso de cualquier tipo de publico, asi mismo llevando el control de todo con ID's para un mejor flujo, una interfaz sencilla y eficaz.
---

## Introducción  
El sistema permite gestionar de manera eficiente la información de productos, ventas y clientes en una licorería. Proporciona funcionalidades para:  
- Registrar y modificar datos en la base de datos.  
- Visualizar detalles importantes de productos y empleados.  
- Facilitar la gestión de categorías, subcategorías y ventas.  

---

## Características Principales  
- **Gestión de Productos:** Agregar, editar y eliminar productos de la base de datos.  
- **Control de Clientes y Empleados:** Visualización y manipulación de registros.  
- **Tablas Organizativas:** Relación de categorías, subcategorías y detalles de ventas.  
- **Funciones CRUD:** Implementadas en módulos separados para mejor organización.  

---

## Requisitos del Proyecto  
Asegúrate de tener instalados los siguientes requisitos:  
- **Python 3.x**  
- **PostgreSQL 12+**  
- **Librerías de Python:**  
   pip install psycopg2-binary  
   pip install tkinter  

---

## Estructura del Proyecto  
La estructura del proyecto está organizada en carpetas y archivos de la siguiente manera:

Proyecto_Licoreria/
│
├── cerrar/                  # Funcionalidades de cierre
│   ├── cerrarpo             # Archivo relacionado con procesos de cierre
│
├── clase/                   # Clases del programa
│   ├── conexion             # Conectar a la base de datos
│
├── funciones/               # Módulos con funciones en SQL
│   ├── __init__             # Inicializador de módulo
│   ├── agregar              # Función para agregar registros
│   ├── delete               # Función para eliminar registros
│   ├── modificar            # Función para modificar registros
│   └── show                 # Función para visualizar registros
│
├── funcionespostgre/        # Funciones para modificar en Postgre
│   ├── funcionespostgre     # Funciones iguales a las de SQL
│
├── tablas/                  # Organización de tablas de la base de datos
│   ├── categoria            # Tabla de categorías de productos
│   ├── cliente              # Tabla de clientes
│   ├── detalle              # Tabla con detalles adicionales
│   ├── empleado             # Tabla de empleados
│   ├── producto             # Tabla principal de productos
│   ├── subcategoria         # Tabla de subcategorías
│   └── ventas               # Tabla de ventas realizadas
│
├── logo/                    # Icono del proyecto
│
├── interfaz_postg                  # Archivo con configuración de la base de datos
├── interfaz_server                   # Archivo principal del servidor
├── migracion                # Para migrar datos desde SQL a Postgre
└── README.md                # Documentación del proyecto

---

## Funciones  
Las funciones implementadas en el proyecto están organizadas en la carpeta `funciones/` y realizan lo siguiente:  
1. **agregar:** Inserta nuevos registros en la base de datos.  
2. **delete:** Elimina registros existentes.  
3. **modificar:** Actualiza la información de un registro.  
4. **show:** Muestra los datos existentes en las tablas.  

---

## Tablas de la Base de Datos  
Las siguientes tablas permiten organizar la información de la licorería:  
1. **categoria**: Clasificación principal de los productos.  
2. **subcategoria**: Clasificación más específica.  
3. **producto**: Información detallada de los productos.  
4. **cliente**: Datos de los clientes.  
5. **empleado**: Registro de empleados.  
6. **detalle**: Información adicional relacionada con ventas.  
7. **ventas**: Registro de todas las ventas realizadas.  

---

## Instalación  
Sigue los pasos contenido en requeriments

---