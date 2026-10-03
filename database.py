"""
Módulo de Base de Datos para el Sistema de Gestión y Fidelización de Lavadero de Autos.
Manejo de SQLite3, creación de tablas, hashing de contraseñas y datos iniciales (seeds).
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'lavadero.db')

def get_db_connection():
    """Establece conexión con la base de datos SQLite retornando filas como diccionarios."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa las tablas de la base de datos e inserta datos de demostración."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabla de Usuarios (Administradores y Clientes)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            phone TEXT DEFAULT '',
            role TEXT DEFAULT 'cliente',
            points INTEGER DEFAULT 200,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabla de Servicios de Lavado
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            duration TEXT NOT NULL,
            description TEXT NOT NULL,
            features TEXT NOT NULL,
            icon TEXT NOT NULL,
            badge TEXT DEFAULT ''
        )
    ''')

    # Tabla de Insumos / Productos Utilizados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            eco_friendly INTEGER DEFAULT 1,
            badge TEXT DEFAULT '',
            icon TEXT NOT NULL
        )
    ''')

    # Tabla de Reservas / Citas (para interacción del cliente)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            date_time TEXT NOT NULL,
            vehicle_plate TEXT NOT NULL,
            vehicle_model TEXT NOT NULL,
            status TEXT DEFAULT 'Confirmado',
            notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
    ''')

    conn.commit()

    # Sembrar Administrador por defecto si no existe
    cursor.execute("SELECT id FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (full_name, username, password_hash, birth_date, phone, role, points)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Administrador General',
            'admin',
            generate_password_hash('admin123'),
            '1990-05-15',
            '+54 9 11 4567-8900',
            'admin',
            9999
        ))

    # Sembrar Clientes de Demostración para pruebas
    sample_users = [
        ('Carlos Méndez', 'carlos_m', 'cliente123', '1995-10-14', '+54 9 11 2345-6789', 'cliente', 450),
        ('Valentina Silva', 'valentina_s', 'cliente123', '1998-03-22', '+54 9 11 8765-4321', 'cliente', 820),
        ('Lucas Torres', 'lucas_t', 'cliente123', '1992-10-28', '+54 9 11 3456-7890', 'cliente', 150),
        ('Sofía Martínez', 'sofia_m', 'cliente123', '2001-07-09', '+54 9 11 9876-5432', 'cliente', 600),
        ('Diego Fernández', 'diego_f', 'cliente123', '1987-12-03', '+54 9 11 5678-1234', 'cliente', 300)
    ]

    for name, user, pwd, bdate, phone, role, pts in sample_users:
        cursor.execute("SELECT id FROM users WHERE username = ?", (user,))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO users (full_name, username, password_hash, birth_date, phone, role, points)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, user, generate_password_hash(pwd), bdate, phone, role, pts))

    # Sembrar Catálogo de Servicios Top
    cursor.execute("SELECT COUNT(*) as count FROM services")
    if cursor.fetchone()['count'] == 0:
        services_data = [
            (
                'Lavado Premium Diamante',
                'Exterior & Detallado',
                8500.0,
                '60 min',
                'Tratamiento intensivo con espuma activa pH neutro, descontaminado rápido de pintura, secado con microfibra de alta absorción y abrillantado cerámico.',
                'Espuma activa de alta densidad|Descontaminado férrico|Secado térmico y microfibra|Aplicación de cera rápida SiO2|Acondicionado de neumáticos satinado',
                'sparkles',
                'Más Solicitado'
            ),
            (
                'Encerado Carnauba Espejo',
                'Protección de Pintura',
                12000.0,
                '90 min',
                'Aplicación artesanal de cera de Carnauba grado 1 biodegradable brasileña. Brinda un brillo profundo efecto mojado y protección hidrofóbica por 60 días.',
                'Cera Carnauba 100% natural|Brillo efecto mojado hiper profundo|Sellado de microporos de laca|Protección contra rayos UV y lluvia ácida|Limpieza profunda de llantas',
                'shield-check',
                'Exclusivo'
            ),
            (
                'Limpieza Profunda de Tapicería y Cueros',
                'Interior & Detailing',
                16500.0,
                '120 min',
                'Desarmado de butacas si aplica, inyección-extracción a vapor de telas, hidratación con bálsamos nutrientes para cueros y neutralización de olores.',
                'Inyección y extracción a vapor 140°C|Eliminación de manchas difíciles|Nutrición de cueros con acabado mate original|Desinfección de conductos de A/C|Aspirado milimétrico',
                'sparkles',
                'Recomendado'
            ),
            (
                'Sellado Cerámico 9H Nano-Shield',
                'Tratamiento Profesional',
                38000.0,
                '4 horas',
                'Corrección de pintura en 2 etapas para eliminar el 85-90% de micro-rayas (swirls), sellado con cuarzo líquido 9H con 18 meses de durabilidad garantizada.',
                'Corrección de barniz en 2 pasos|Protección dureza 9H real|Propiedad anti-estática y súper hidrofóbica|Certificado de garantía por escrito|Lavado de mantenimiento bonificado',
                'award',
                'Gama Alta'
            ),
            (
                'Descontaminado & Lavado de Chasis',
                'Chasis y Motor',
                9800.0,
                '50 min',
                'Lavado inferior a alta presión con desengrasantes ecológicos neutros para eliminar salitre, brea y barro acumulado, protegiendo partes mecánicas.',
                'Agua caliente y desengrasante biodegradable|Limpieza de buches de rueda y suspensión|Inspección visual anticorrosiva|Secado con aire comprimido|Tratamiento protector de plásticos',
                'car',
                'Especializado'
            ),
            (
                'Desinfección & Ozonizado de Cabina',
                'Salud & Bienestar',
                5500.0,
                '30 min',
                'Tratamiento con cañón de ozono de alta potencia que destruye el 99.9% de hongos, bacterias, ácaros y olores residuales de tabaco o mascotas.',
                'Generación de gas ozono activo O3|Esterilización total de ductos de ventilación|Cero químicos ni residuos húmedos|Ideal para personas alérgicas o con niños|Aroma fresco a cabina nueva',
                'heart',
                'Saludable'
            )
        ]
        cursor.executemany('''
            INSERT INTO services (name, category, price, duration, description, features, icon, badge)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', services_data)

    # Sembrar Insumos y Productos de Primera Línea
    cursor.execute("SELECT COUNT(*) as count FROM products")
    if cursor.fetchone()['count'] == 0:
        products_data = [
            (
                'Cera de Carnauba Brasileña Pura Grado 1',
                'Gyeon / Chemical Guys',
                'Ceras y Selladores',
                'Formulada con un 50% de cera natural de Carnauba de origen sustentable. Otorga una calidez y profundidad de reflejo inigualable sin dañar la capa transparente.',
                1,
                '100% Biodegradable',
                'leaf'
            ),
            (
                'Silicona Hi-Gloss Libre de Solventes',
                'Koch-Chemie Alemania',
                'Acondicionadores',
                'Acondicionador a base de agua enriquecido con polímeros protectores UV. Deja un acabado original satinado o brillante según preferencia, sin sensación grasosa ni pegajosa.',
                1,
                'Cero Solventes',
                'check-circle'
            ),
            (
                'Shampoo pH Neutro Nanotecnológico',
                'Meguiar\'s Mirror Glaze',
                'Lavado Exterior',
                'Agentes limpiadores ultra lubricantes de espuma espesa que encapsulan la suciedad para evitar micro-rayas (marcas de remolino). Totalmente seguro para tratamientos cerámicos.',
                1,
                'pH 7.0 Neutro',
                'droplet'
            ),
            (
                'Sellador Cerámico Líquido SiO2',
                'CarPro CQuartz Professional',
                'Protección Nanotecnológica',
                'Dióxido de silicio ultra refinado que crea una barrera física de cuarzo transparente, repeliendo el agua, el barro y la radiación ultravioleta.',
                0,
                'Efecto Loto 9H',
                'shield'
            ),
            (
                'Microfibras Edgeless Coreanas 800 GSM',
                'The Rag Company',
                'Accesorios de Limpieza',
                'Toallas de microfibra de pelo largo cortadas con láser sin costuras ni rebordes plásticos para garantizar cero fricción abrasiva sobre pinturas delicadas.',
                1,
                'Cero Rayones',
                'feather'
            )
        ]
        cursor.executemany('''
            INSERT INTO products (name, brand, category, description, eco_friendly, badge, icon)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', products_data)

    conn.commit()
    conn.close()

# Funciones de Gestión de Usuarios
def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user

def get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    conn.close()
    return users

def create_user(full_name, username, password, birth_date, phone='', role='cliente', points=200):
    """Registra un nuevo usuario con contraseña hasheada."""
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    try:
        cursor.execute('''
            INSERT INTO users (full_name, username, password_hash, birth_date, phone, role, points)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (full_name, username, password_hash, birth_date, phone, role, points))
        conn.commit()
        new_id = cursor.lastrowid
        return {'success': True, 'user_id': new_id}
    except sqlite3.IntegrityError:
        return {'success': False, 'error': 'El nombre de usuario ya está registrado en el sistema.'}
    finally:
        conn.close()

def update_user(user_id, full_name, username, birth_date, phone='', role='cliente', points=None, password=None):
    """Actualiza cualquier campo del usuario. Si se pasa contraseña, se vuelve a hashear."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Verificar si el nuevo username está ocupado por otro usuario
        existing = cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (username, user_id)).fetchone()
        if existing:
            return {'success': False, 'error': 'El nombre de usuario ya pertenece a otra persona.'}

        if password and password.strip():
            new_hash = generate_password_hash(password.strip())
            if points is not None:
                cursor.execute('''
                    UPDATE users
                    SET full_name = ?, username = ?, birth_date = ?, phone = ?, role = ?, points = ?, password_hash = ?
                    WHERE id = ?
                ''', (full_name, username, birth_date, phone, role, points, new_hash, user_id))
            else:
                cursor.execute('''
                    UPDATE users
                    SET full_name = ?, username = ?, birth_date = ?, phone = ?, role = ?, password_hash = ?
                    WHERE id = ?
                ''', (full_name, username, birth_date, phone, role, new_hash, user_id))
        else:
            if points is not None:
                cursor.execute('''
                    UPDATE users
                    SET full_name = ?, username = ?, birth_date = ?, phone = ?, role = ?, points = ?
                    WHERE id = ?
                ''', (full_name, username, birth_date, phone, role, points, user_id))
            else:
                cursor.execute('''
                    UPDATE users
                    SET full_name = ?, username = ?, birth_date = ?, phone = ?, role = ?
                    WHERE id = ?
                ''', (full_name, username, birth_date, phone, role, user_id))

        conn.commit()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    finally:
        conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    finally:
        conn.close()

def get_services():
    conn = get_db_connection()
    services = conn.execute("SELECT * FROM services ORDER BY price ASC").fetchall()
    conn.close()
    return services

def get_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products ORDER BY id ASC").fetchall()
    conn.close()
    return products

def create_appointment(user_id, service_id, date_time, vehicle_plate, vehicle_model, notes=''):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO appointments (user_id, service_id, date_time, vehicle_plate, vehicle_model, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, service_id, date_time, vehicle_plate, vehicle_model, notes))
        # Otorgar 50 puntos de fidelización por agendar
        cursor.execute("UPDATE users SET points = points + 50 WHERE id = ?", (user_id,))
        conn.commit()
        return {'success': True, 'appointment_id': cursor.lastrowid}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    finally:
        conn.close()

def get_user_appointments(user_id):
    conn = get_db_connection()
    appointments = conn.execute('''
        SELECT a.*, s.name as service_name, s.price as service_price
        FROM appointments a
        JOIN services s ON a.service_id = s.id
        WHERE a.user_id = ?
        ORDER BY a.id DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return appointments
