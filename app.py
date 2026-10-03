"""
Sistema Web de Gestión y Fidelización para Lavadero de Autos
Desarrollado con Flask, SQLite, HTML5, CSS3 y JavaScript moderno.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date
import database

app = Flask(__name__)
app.secret_key = 'super_secret_lavadero_key_2026_top_carwash'

# Inicializar Base de Datos con catálogo y usuarios semilla
database.init_db()

def calculate_birthday_info(birth_date_str):
    """
    Calcula si es el mes de cumpleaños del cliente, los días que faltan
    y la edad que cumple para la sección de fidelización y promociones.
    """
    try:
        bdate = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = date.today()
        is_birthday_month = (today.month == bdate.month)
        is_birthday_today = (today.month == bdate.month and today.day == bdate.day)

        # Próximo cumpleaños
        next_birthday = date(today.year, bdate.month, bdate.day)
        if next_birthday < today:
            next_birthday = date(today.year + 1, bdate.month, bdate.day)
        
        days_until = (next_birthday - today).days
        current_age = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))

        return {
            'is_birthday_month': is_birthday_month,
            'is_birthday_today': is_birthday_today,
            'days_until': days_until,
            'age': current_age,
            'birth_formatted': bdate.strftime('%d/%m/%Y')
        }
    except Exception:
        return {
            'is_birthday_month': False,
            'is_birthday_today': False,
            'days_until': 999,
            'age': 0,
            'birth_formatted': birth_date_str
        }

# ==============================================================
# RUTAS PÚBLICAS Y DE AUTENTICACIÓN
# ==============================================================

@app.route('/')
def index():
    """Página principal con Login, catálogo público y botón destacado de registro."""
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('client_dashboard'))

    services = database.get_services()
    products = database.get_products()
    return render_template('index.html', services=services, products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Procesa el inicio de sesión para Clientes y Administradores."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Por favor ingrese su usuario y contraseña.', 'error')
            return redirect(url_for('index'))

        user = database.get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']

            flash(f'¡Bienvenido nuevamente, {user["full_name"]}!', 'success')
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('client_dashboard'))
        else:
            flash('Credenciales incorrectas. Verifique usuario y contraseña.', 'error')
            return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    """
    Formulario de Registro con campos obligatorios:
    - Nombre completo
    - Nombre de usuario
    - Contraseña
    - Fecha de nacimiento
    """
    full_name = request.form.get('full_name', '').strip()
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    birth_date = request.form.get('birth_date', '').strip()
    phone = request.form.get('phone', '').strip()

    # Validación de campos obligatorios
    if not full_name or not username or not password or not birth_date:
        flash('Todos los campos marcados con (*) son obligatorios.', 'error')
        return redirect(url_for('index'))

    # Intentar crear el nuevo usuario
    result = database.create_user(
        full_name=full_name,
        username=username,
        password=password,
        birth_date=birth_date,
        phone=phone,
        role='cliente',
        points=250 # Bono de bienvenida por registro
    )

    if result.get('success'):
        # Iniciar sesión automáticamente
        user = database.get_user_by_id(result['user_id'])
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['full_name'] = user['full_name']
        session['role'] = user['role']

        flash('¡Registro completado con éxito! Has obtenido 250 puntos de bienvenida.', 'success')
        return redirect(url_for('client_dashboard'))
    else:
        flash(result.get('error', 'Error al registrar la cuenta.'), 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Cierra la sesión actual y redirige a la página principal."""
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

# ==============================================================
# PANEL DEL CLIENTE (USUARIO REGULAR)
# ==============================================================

@app.route('/dashboard')
def client_dashboard():
    """
    Panel exclusivo del cliente:
    - Catálogo de servicios detallado
    - Insumos y productos de alta gama utilizados
    - Sección de Beneficios / Puntos y regalo por Fecha de Nacimiento
    """
    if 'user_id' not in session:
        flash('Debe iniciar sesión para acceder a su panel.', 'warning')
        return redirect(url_for('index'))

    user = database.get_user_by_id(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('index'))

    services = database.get_services()
    products = database.get_products()
    appointments = database.get_user_appointments(user['id'])
    birthday_info = calculate_birthday_info(user['birth_date'])

    # Determinar categoría de fidelización según puntos
    pts = user['points']
    if pts >= 800:
        tier = {'name': 'Black VIP Diamante', 'color': 'linear-gradient(135deg, #1e293b, #0f172a)', 'discount': 25, 'badge': 'VIP Diamante'}
    elif pts >= 400:
        tier = {'name': 'Gold Exclusive', 'color': 'linear-gradient(135deg, #b45309, #d97706)', 'discount': 15, 'badge': 'Gold'}
    else:
        tier = {'name': 'Silver Member', 'color': 'linear-gradient(135deg, #3b82f6, #1d4ed8)', 'discount': 10, 'badge': 'Silver'}

    return render_template(
        'client_dashboard.html',
        user=user,
        services=services,
        products=products,
        appointments=appointments,
        birthday_info=birthday_info,
        tier=tier
    )

@app.route('/api/book-service', methods=['POST'])
def book_service():
    """Permite al cliente agendar un servicio y sumar puntos de fidelización."""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'No autorizado'}), 401

    service_id = request.form.get('service_id')
    date_time = request.form.get('date_time')
    vehicle_plate = request.form.get('vehicle_plate', '').upper()
    vehicle_model = request.form.get('vehicle_model')
    notes = request.form.get('notes', '')

    if not service_id or not date_time or not vehicle_plate or not vehicle_model:
        return jsonify({'success': False, 'error': 'Por favor complete todos los datos del vehículo y fecha.'}), 400

    result = database.create_appointment(
        user_id=session['user_id'],
        service_id=service_id,
        date_time=date_time,
        vehicle_plate=vehicle_plate,
        vehicle_model=vehicle_model,
        notes=notes
    )

    if result.get('success'):
        return jsonify({'success': True, 'message': '¡Turno reservado exitosamente! Has sumado +50 puntos de fidelización.'})
    else:
        return jsonify({'success': False, 'error': result.get('error')}), 500

# ==============================================================
# PANEL DEL ADMINISTRADOR
# ==============================================================

@app.route('/admin')
def admin_dashboard():
    """
    Panel exclusivo del Administrador:
    - Gestión completa de clientes
    - Edición total de datos (nombre, usuario, contraseña, fecha de nacimiento, contacto)
    - Métricas de fidelización y cumpleaños
    """
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Acceso restringido únicamente para administradores.', 'error')
        return redirect(url_for('index'))

    users = database.get_all_users()
    today = date.today()
    
    # Métricas para el administrador
    total_clients = sum(1 for u in users if u['role'] == 'cliente')
    total_points = sum(u['points'] for u in users)
    birthdays_this_month = 0

    users_with_meta = []
    for u in users:
        u_dict = dict(u)
        b_info = calculate_birthday_info(u['birth_date'])
        u_dict['birthday_info'] = b_info
        if b_info['is_birthday_month']:
            birthdays_this_month += 1
        users_with_meta.append(u_dict)

    return render_template(
        'admin_dashboard.html',
        users=users_with_meta,
        total_clients=total_clients,
        total_points=total_points,
        birthdays_this_month=birthdays_this_month,
        today=today
    )

@app.route('/admin/user/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    """API para obtener los datos de un usuario para cargar en el modal de edición."""
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    user = database.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({
        'id': user['id'],
        'full_name': user['full_name'],
        'username': user['username'],
        'birth_date': user['birth_date'],
        'phone': user['phone'],
        'role': user['role'],
        'points': user['points'],
        'created_at': user['created_at']
    })

@app.route('/admin/user/update', methods=['POST'])
def admin_update_user():
    """
    Permite al administrador editar o actualizar CUALQUIER dato del cliente:
    - Nombre completo
    - Nombre de usuario
    - Contraseña (opcional para restablecerla)
    - Fecha de nacimiento
    - Teléfono / Contacto
    - Puntos de fidelización
    - Rol (cliente / admin)
    """
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'error': 'No autorizado'}), 403

    user_id = request.form.get('user_id')
    full_name = request.form.get('full_name', '').strip()
    username = request.form.get('username', '').strip()
    birth_date = request.form.get('birth_date', '').strip()
    phone = request.form.get('phone', '').strip()
    role = request.form.get('role', 'cliente')
    points = request.form.get('points', type=int)
    password = request.form.get('password', '').strip()

    if not user_id or not full_name or not username or not birth_date:
        return jsonify({'success': False, 'error': 'Los campos Nombre, Usuario y Fecha de Nacimiento son obligatorios.'}), 400

    result = database.update_user(
        user_id=int(user_id),
        full_name=full_name,
        username=username,
        birth_date=birth_date,
        phone=phone,
        role=role,
        points=points,
        password=password if password else None
    )

    if result.get('success'):
        return jsonify({'success': True, 'message': 'Cliente actualizado exitosamente.'})
    else:
        return jsonify({'success': False, 'error': result.get('error', 'Error al actualizar')}), 400

@app.route('/admin/user/create', methods=['POST'])
def admin_create_user():
    """Permite al administrador registrar un nuevo cliente o administrador directamente."""
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'error': 'No autorizado'}), 403

    full_name = request.form.get('full_name', '').strip()
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    birth_date = request.form.get('birth_date', '').strip()
    phone = request.form.get('phone', '').strip()
    role = request.form.get('role', 'cliente')
    points = request.form.get('points', 250, type=int)

    if not full_name or not username or not password or not birth_date:
        return jsonify({'success': False, 'error': 'Nombre, Usuario, Contraseña y Fecha de Nacimiento son obligatorios.'}), 400

    result = database.create_user(
        full_name=full_name,
        username=username,
        password=password,
        birth_date=birth_date,
        phone=phone,
        role=role,
        points=points
    )

    if result.get('success'):
        return jsonify({'success': True, 'message': 'Usuario creado correctamente en el sistema.'})
    else:
        return jsonify({'success': False, 'error': result.get('error')}), 400

@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    """Permite al administrador eliminar a un cliente."""
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'error': 'No autorizado'}), 403

    # Evitar que el admin se elimine a sí mismo
    if user_id == session.get('user_id'):
        return jsonify({'success': False, 'error': 'No puedes eliminar tu propia cuenta de administrador.'}), 400

    result = database.delete_user(user_id)
    if result.get('success'):
        return jsonify({'success': True, 'message': 'Usuario eliminado satisfactoriamente.'})
    else:
        return jsonify({'success': False, 'error': result.get('error')}), 400

if __name__ == '__main__':
    print("=" * 65)
    print("🚗 VELOCE AUTO SPA & DETAILING - SISTEMA WEB DE GESTIÓN")
    print("Servidor activo en: http://127.0.0.1:5000")
    print("Credenciales por defecto Administrador: admin / admin123")
    print("Credenciales por defecto Cliente de prueba: carlos_m / cliente123")
    print("=" * 65)
    app.run(debug=True, host='127.0.0.1', port=5000)
