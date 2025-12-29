Sistema web desarrollado con **Django** para la gestión de clientes, membresías y control automático de entradas.

Permite:

* Registro automático de accesos por matrícula
* Validación de membresías activas
* Bloqueo de accesos duplicados
* Panel administrativo completo
* Historial de entradas con fecha y hora reales

---

## 🚀 Requisitos

Antes de comenzar asegúrate de tener instalado:

* **Python 3.11+** (recomendado 3.12)
* **Git**
* **pip**
* **virtualenv** (opcional pero recomendado)

Comprobar versiones:

```bash
python --version
git --version
```

---

## 📥 Clonar el repositorio

```bash
git clone https://github.com/Josspoot/gymcontrol.git
cd gymcontrol
```

---

## 🧪 Crear entorno virtual

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## 📦 Instalar dependencias

```bash
pip install -r requirements.txt
```

Si no existe `requirements.txt`, puedes crearlo con:

```bash
pip freeze > requirements.txt
```

---

## 🗄️ Migraciones de base de datos

> ⚠️ Solo necesarias la **primera vez** o si se cambian modelos

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 👤 Crear superusuario (Admin)

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear el usuario administrador.

---

## ▶️ Ejecutar el servidor

```bash
python manage.py runserver
```

Accede en tu navegador a:

* 🌐 **Página principal (registro de accesos)**
  [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

* 🔐 **Panel de administración**
  [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔑 Flujo del sistema

1. El usuario ingresa su **matrícula** en la página principal
2. El sistema:

   * Valida que el cliente exista
   * Verifica que la membresía esté **activa**
   * Registra automáticamente la entrada
   * Bloquea accesos duplicados
3. El registro aparece automáticamente en:

   * Panel Admin → **Registro de Entradas**

---

## 🛠️ Comandos útiles

### Iniciar servidor

```bash
python manage.py runserver
```

### Acceder a la shell de Django

```bash
python manage.py shell
```

### Crear migraciones

```bash
python manage.py makemigrations
```

### Aplicar migraciones

```bash
python manage.py migrate
```

### Crear superusuario

```bash
python manage.py createsuperuser
```

### Recolectar archivos estáticos (producción)

```bash
python manage.py collectstatic
```

---

## ⏰ Zona horaria

El proyecto usa:

```python
TIME_ZONE = 'America/Mexico_City'
USE_TZ = True
```

Asegúrate de no cambiar esto para mantener horas correctas en todos los dispositivos.

---

## 🧩 Tecnologías usadas

* Python
* Django 6
* SQLite (por defecto)
* HTML / CSS
* Django Admin

---

## 📌 Notas importantes

* No es necesario migrar cada vez que se clona el repo si la base de datos ya existe.
* Para producción se recomienda:

  * PostgreSQL o MySQL
  * DEBUG = False
  * Variables de entorno

---

## 📄 Licencia

Este proyecto es de uso privado/educativo.
Puedes modificarlo y adaptarlo a tus necesidades.

---

## ✨ Autor

Desarrollado por **Josspoot**
