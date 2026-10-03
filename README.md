# 🚗 Veloce Auto Spa & Detailing - Sistema de Gestión y Fidelización

Sistema web completo, funcional y de alto impacto visual diseñado para un lavadero de autos de gama alta. Cuenta con arquitectura Full-Stack utilizando **Python (Flask)** en el backend y **HTML5, CSS3 y JavaScript moderno** en el frontend, con base de datos **SQLite3**.

---

## 🌟 Características Principales

### 1. 🔐 Módulo de Autenticación y Registro
* **Login Moderno:** Tarjeta con diseño automotriz oscuro (dark mode), efecto glassmorphism y accesos rápidos de demostración con 1 clic.
* **Botón de Registro Destacado en Azul:** Con el texto exacto requerido:
  > **`"Regístrate para obtener nuestros beneficios"`**
* **Formulario de Registro:** Solicita obligatoriamente:
  * **Nombre completo**
  * **Nombre de usuario**
  * **Contraseña** (hasheada de forma segura)
  * **Fecha de nacimiento** (clave para el motor de beneficios por cumpleaños)
  * *Teléfono / WhatsApp de contacto*

---

### 2. 💎 Panel del Cliente (Usuario Regular)
* **Diseño "Lavadero Top":** Estética de alta gama con acentos en azul eléctrico, cian y dorado VIP.
* **Catálogo Visual de Servicios:**
  * Lavado Premium Diamante
  * Encerado Carnauba Espejo
  * Limpieza Profunda de Tapicería y Cueros
  * Sellado Cerámico 9H Nano-Shield
  * Descontaminado & Lavado de Chasis
  * Desinfección & Ozonizado de Cabina
  * Precios, duración, lista de inclusiones y modal interactivo para agendar turno.
* **Productos e Insumos Utilizados:**
  * Destaca la calidad y compromiso ecológico: Ceras de Carnauba biodegradables, siliconas libres de solventes, shampoos con pH neutro, sellador SiO2 y microfibras 800 GSM anti-rayones.
* **Sección de Fidelización & Beneficios:**
  * **Motor de Cumpleaños:** Detección automática del mes y día de cumpleaños. Si es el mes del cliente, activa una alerta dorada con **Lavado Exterior 100% Bonificado** y descuentos especiales. Si no, muestra la cuenta regresiva en días hacia su próximo festejo.
  * Niveles de membresía (*Silver*, *Gold*, *Black VIP*).
  * Contador de puntos acumulados (+250 de bienvenida y +50 por cada turno agendado).

---

### 3. 🛡️ Panel del Administrador
* **Acceso Exclusivo:** Protegido por sesión y rol de administrador.
* **Métricas KPI en Tiempo Real:** Total de clientes registrados, puntos acumulados emitidos, cumpleañeros del mes y catálogo activo.
* **Gestión Completa de Clientes:** Tabla interactiva con búsqueda reactiva en vivo (filtra por nombre, usuario, teléfono o fecha de nacimiento).
* **Edición Total:** Modal que permite editar **absolutamente todos los datos del cliente**:
  * Nombre completo
  * Nombre de usuario
  * Fecha de nacimiento
  * Contraseña (modificación opcional de clave con re-hasheo automático)
  * Teléfono / WhatsApp
  * Puntos de fidelización
  * Rol (cliente / admin)
* **Altas y Bajas:** Registro de nuevos clientes presenciales y eliminación con confirmación segura.

---

## 🔑 Credenciales de Acceso de Prueba

| Rol | Usuario | Contraseña | Propósito |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin` | `admin123` | Control total, edición de usuarios y métricas |
| **Cliente Regular** | `carlos_m` | `cliente123` | Panel VIP de cliente, catálogo y puntos |
| **Cliente Regular** | `valentina_s` | `cliente123` | Cliente con membresía Gold |

*(También puedes registrar un cliente nuevo usando el botón azul de registro)*

---

## 🚀 Instrucciones para Ponerlo en Marcha

### Requisitos Previos
* Tener instalado **Python 3.8+** (Probado y optimizado en Python 3.14).

### Paso 1: Abrir la terminal o consola en la carpeta del proyecto
```bash
cd c:\ARCHIVOS\Lavadero\lavadero
```

### Paso 2: Instalar las dependencias necesarias
```bash
pip install -r requirements.txt
```

### Paso 3: Iniciar el servidor
```bash
python app.py
```
*(O simplemente hacer doble clic en `run.bat` o `iniciar.bat`)*

### Paso 4: Abrir en el navegador
Visita en tu navegador web:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📁 Estructura del Código

```text
lavadero/
├── app.py                  # Servidor Flask, rutas, lógica de cumpleaños y APIs
├── database.py             # SQLite3, hashing de passwords, inicialización y CRUD
├── requirements.txt        # Dependencias de Python (Flask, Werkzeug)
├── run.bat                 # Script de inicio rápido para Windows
├── README.md               # Documentación completa
├── static/
│   ├── css/
│   │   └── style.css       # Estilos modernos de lujo automotriz y botón azul
│   └── js/
│       ├── main.js         # Modales, toasts, autocompletado demo y reservas
│       └── admin.js        # Búsqueda en vivo y edición total de clientes
└── templates/
    ├── base.html           # Layout común, navbar y contenedor de notificaciones
    ├── index.html          # Login, botón azul de registro y showcase
    ├── client_dashboard.html # Panel VIP con catálogo, insumos y fidelización
    └── admin_dashboard.html  # Panel administrativo con tabla y edición total
```
