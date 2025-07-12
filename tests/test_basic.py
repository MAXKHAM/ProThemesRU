import unittest
import json
from app import create_app, db
from app.models import User, Project, Template, Block

class ProThemesTestCase(unittest.TestCase):
    """Базовый класс для тестов"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            self.create_test_data()

    def tearDown(self):
        """Очистка после каждого теста"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        """Создание тестовых данных"""
        # Создаем тестового пользователя
        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('password123')
        db.session.add(user)
        
        # Создаем тестовый шаблон
        template = Template(
            name='Test Template',
            description='Test template description',
            category='business',
            price=0.0
        )
        db.session.add(template)
        
        # Создаем тестовый блок
        block = Block(
            type='text',
            name='Test Block',
            html='<p>Test content</p>',
            styles={'font-size': '1rem'},
            properties={'text': 'Test content'}
        )
        db.session.add(block)
        
        db.session.commit()

    def test_home_page(self):
        """Тест главной страницы"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ProThemes', response.data)

    def test_register_page(self):
        """Тест страницы регистрации"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'register', response.data)

    def test_login_page(self):
        """Тест страницы входа"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data)

    def test_user_registration(self):
        """Тест регистрации пользователя"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post('/register', data=data)
        self.assertEqual(response.status_code, 302)  # Редирект после регистрации

    def test_user_login(self):
        """Тест входа пользователя"""
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post('/login', data=data)
        self.assertEqual(response.status_code, 302)  # Редирект после входа

    def test_api_templates(self):
        """Тест API шаблонов"""
        response = self.client.get('/api/templates')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_api_blocks(self):
        """Тест API блоков"""
        response = self.client.get('/api/blocks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_admin_access(self):
        """Тест доступа к админ панели"""
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 302)  # Редирект на логин

    def test_static_files(self):
        """Тест статических файлов"""
        response = self.client.get('/static/css/style.css')
        self.assertEqual(response.status_code, 200)

    def test_404_error(self):
        """Тест обработки 404 ошибки"""
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)

class APITestCase(unittest.TestCase):
    """Тесты для API endpoints"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            self.create_test_data()

    def tearDown(self):
        """Очистка после каждого теста"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        """Создание тестовых данных"""
        # Создаем тестового пользователя
        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

    def test_auth_register(self):
        """Тест API регистрации"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post('/api/auth/register', 
                                  data=json.dumps(data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_auth_login(self):
        """Тест API входа"""
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/auth/login',
                                  data=json.dumps(data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)

    def test_projects_api(self):
        """Тест API проектов"""
        response = self.client.get('/api/projects')
        self.assertEqual(response.status_code, 401)  # Требуется аутентификация

    def test_templates_api(self):
        """Тест API шаблонов"""
        response = self.client.get('/api/templates')
        self.assertEqual(response.status_code, 200)

class ModelTestCase(unittest.TestCase):
    """Тесты для моделей"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Очистка после каждого теста"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        """Тест создания пользователя"""
        with self.app.app_context():
            user = User(
                username='testuser',
                email='test@example.com',
                role='user'
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            self.assertIsNotNone(user.id)
            self.assertTrue(user.check_password('password123'))

    def test_project_creation(self):
        """Тест создания проекта"""
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            db.session.add(user)
            db.session.commit()
            
            project = Project(
                name='Test Project',
                description='Test description',
                content='<html><body>Test</body></html>',
                user_id=user.id
            )
            db.session.add(project)
            db.session.commit()
            
            self.assertIsNotNone(project.id)
            self.assertEqual(project.author, user)

    def test_template_creation(self):
        """Тест создания шаблона"""
        with self.app.app_context():
            template = Template(
                name='Test Template',
                description='Test description',
                category='business',
                price=0.0
            )
            db.session.add(template)
            db.session.commit()
            
            self.assertIsNotNone(template.id)
            self.assertEqual(template.category, 'business')

    def test_block_creation(self):
        """Тест создания блока"""
        with self.app.app_context():
            block = Block(
                type='text',
                name='Test Block',
                html='<p>Test</p>',
                styles={'font-size': '1rem'},
                properties={'text': 'Test'}
            )
            db.session.add(block)
            db.session.commit()
            
            self.assertIsNotNone(block.id)
            self.assertEqual(block.type, 'text')

if __name__ == '__main__':
    unittest.main() 