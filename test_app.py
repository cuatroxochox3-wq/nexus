"""
Script de verificación y pruebas automatizadas para el Sistema de Lavadero.
"""
import sys
import unittest
from werkzeug.security import check_password_hash
import database
from app import app, calculate_birthday_info

class LavaderoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_01_database_initialization(self):
        """Verifica que las tablas y usuarios iniciales se hayan creado."""
        admin = database.get_user_by_username('admin')
        self.assertIsNotNone(admin)
        self.assertEqual(admin['role'], 'admin')

        services = database.get_services()
        self.assertGreaterEqual(len(services), 6)

        products = database.get_products()
        self.assertGreaterEqual(len(products), 5)
        print("[OK] Base de datos y semillas inicializadas correctamente.")

    def test_02_birthday_calculation(self):
        """Verifica el calculo de cumpleanos y beneficios."""
        info = calculate_birthday_info('1995-10-14')
        self.assertIn('is_birthday_month', info)
        self.assertIn('days_until', info)
        self.assertIn('age', info)
        print(f"[OK] Logica de cumpleanos verificada. Formato: {info['birth_formatted']}, Dias: {info['days_until']}")

    def test_03_index_route(self):
        """Verifica que la pagina de inicio cargue y tenga el boton exacto requerido."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        # Requerimiento exacto: "Regístrate para obtener nuestros beneficios"
        self.assertIn("Regístrate para obtener nuestros beneficios", content)
        print("[OK] Pagina de inicio y boton exacto de registro encontrados.")

    def test_04_user_registration(self):
        """Verifica el registro con los campos obligatorios."""
        import time
        uname = f"testuser_{int(time.time())}"
        response = self.app.post('/register', data={
            'full_name': 'Cliente Prueba',
            'username': uname,
            'password': 'password123',
            'birth_date': '1996-08-20',
            'phone': '+54 9 11 1111-2222'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        user = database.get_user_by_username(uname)
        self.assertIsNotNone(user)
        self.assertEqual(user['full_name'], 'Cliente Prueba')
        self.assertTrue(check_password_hash(user['password_hash'], 'password123'))
        print("[OK] Registro de cliente con campos obligatorios completado.")

    def test_05_admin_login_and_full_edit(self):
        """Verifica el inicio de sesion de admin y la edicion total de cualquier campo de cliente."""
        # 1. Login Admin
        login_resp = self.app.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(login_resp.status_code, 200)

        # 2. Acceso a /admin
        admin_resp = self.app.get('/admin')
        self.assertEqual(admin_resp.status_code, 200)
        self.assertIn("Gestión de Clientes y Fidelización", admin_resp.data.decode('utf-8'))

        # 3. Edicion total de Carlos Mendez
        carlos = database.get_user_by_username('carlos_m')
        self.assertIsNotNone(carlos)
        carlos_id = carlos['id']

        update_resp = self.app.post('/admin/user/update', data={
            'user_id': carlos_id,
            'full_name': 'Carlos Mendez Modificado',
            'username': 'carlos_m',
            'birth_date': '1995-10-15',
            'phone': '+54 9 11 9999-8888',
            'role': 'cliente',
            'points': 550,
            'password': 'nuevacontrasena123'
        })
        self.assertEqual(update_resp.status_code, 200)
        json_data = update_resp.get_json()
        self.assertTrue(json_data['success'])

        # Verificar en base de datos que TODO se actualizo
        carlos_updated = database.get_user_by_id(carlos_id)
        self.assertEqual(carlos_updated['full_name'], 'Carlos Mendez Modificado')
        self.assertEqual(carlos_updated['birth_date'], '1995-10-15')
        self.assertEqual(carlos_updated['points'], 550)
        self.assertEqual(carlos_updated['phone'], '+54 9 11 9999-8888')
        self.assertTrue(check_password_hash(carlos_updated['password_hash'], 'nuevacontrasena123'))
        print("[OK] Edicion total de cliente por parte del administrador verificada con exito.")

if __name__ == '__main__':
    unittest.main()
