# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

## Descripción
Aplicación de consola en Python que administra clientes, servicios y reservas mediante programación orientada a objetos. No utiliza bases de datos. Los objetos y listas se mantienen en memoria; los archivos se destinan exclusivamente al registro de eventos y errores.

## Requisitos
- Python 3.12 o superior.
- Git.
- Visual Studio Code (recomendado).

## Ejecución
Desde la carpeta raíz del proyecto:

```bash
python main.py
```

El programa realiza 15 operaciones demostrativas. El archivo `logs/software_fj.log` se crea automáticamente al ejecutar el sistema.

## Pruebas
```bash
python -m unittest discover -s tests -v
```

## Arquitectura
- `software_fj/entidades.py`: clase abstracta Entidad.
- `software_fj/cliente.py`: cliente y encapsulación.
- `software_fj/servicio.py`: clase abstracta Servicio y tres especializaciones.
- `software_fj/reserva.py`: estados y ciclo de vida de las reservas.
- `software_fj/gestor.py`: administración de listas en memoria.
- `software_fj/excepciones.py`: excepciones personalizadas.
- `software_fj/registro.py`: configuración del logger.
- `main.py`: menú demostrativo y ejecución protegida de operaciones.
- `tests/`: pruebas unitarias.

## Principios POO demostrados
- Abstracción: `Entidad` y `Servicio` son clases abstractas.
- Herencia: `Cliente` y los servicios concretos heredan de sus clases base.
- Encapsulación: atributos privados y propiedades de acceso.
- Polimorfismo: cada servicio implementa su propio cálculo, validación y descripción.
- Sobrecarga simulada: `calcular_costo(cantidad, impuesto=0.0, descuento=0.0)` permite distintas formas de invocación mediante parámetros opcionales. Python no implementa sobrecarga tradicional por firma como Java o C++.

## Manejo de errores
Se utilizan excepciones personalizadas, `try/except/else/finally`, `logger.exception()` y encadenamiento mediante `raise ... from error`.

## Trabajo colaborativo
Cada integrante debe realizar aportes identificables mediante ramas, commits y pull requests. No se deben compartir credenciales ni sobrescribir cambios sin revisión.
