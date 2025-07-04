import unittest
from app import create_app, db
from app.models import User, UserRole
from app.services.user_service import UserService

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        """Тестирование хеширования пароля"""
        user = User(username='test', email='test@example.com')
        user.set_password('password123')
        self.assertFalse(user.check_password('wrong_password'))
        self.assertTrue(user.check_password('password123'))

    def test_user_creation(self):
        """Тестирование создания пользователя"""
        user = UserService.create_user(
            username='test_user',
            email='test@example.com',
            password='password123'
        )
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test@example.com')

    def test_user_authentication(self):
        """Тестирование аутентификации"""
        # Создаем пользователя
        UserService.create_user(
            username='test_user',
            email='test@example.com',
            password='password123'
        )
        
        # Проверяем аутентификацию
        user = UserService.authenticate('test_user', 'password123')
        self.assertIsNotNone(user)
        
        # Проверяем неверный пароль
        user = UserService.authenticate('test_user', 'wrong_password')
        self.assertIsNone(user)

    def test_user_roles(self):
        """Тестирование ролей пользователей"""
        user = UserService.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=UserRole.ADMIN
        )
        self.assertEqual(user.role, UserRole.ADMIN)

if __name__ == '__main__':
    unittest.main()
