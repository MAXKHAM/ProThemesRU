import unittest
import json
import tempfile
import os
from app import app, db, User, Site, MediaFile, ScrapingProfile
from werkzeug.security import generate_password_hash

class ProThemesRUTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            
            # Create test user
            test_user = User(
                username='testuser',
                email='test@example.com',
                password_hash=generate_password_hash('password123'),
                role='user'
            )
            db.session.add(test_user)
            db.session.commit()
            self.test_user_id = test_user.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def get_auth_token(self):
        """Get authentication token for test user"""
        response = self.app.post('/api/auth/login', 
                               json={'email': 'test@example.com', 'password': 'password123'})
        data = json.loads(response.data)
        return data['access_token']

    def test_register(self):
        """Test user registration"""
        response = self.app.post('/api/auth/register', 
                               json={
                                   'username': 'newuser',
                                   'email': 'new@example.com',
                                   'password': 'password123'
                               })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_login(self):
        """Test user login"""
        response = self.app.post('/api/auth/login', 
                               json={'email': 'test@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.assertIn('user', data)

    def test_create_site(self):
        """Test site creation"""
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        response = self.app.post('/api/sites', 
                               json={'name': 'Test Site'},
                               headers=headers)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Test Site')

    def test_get_sites(self):
        """Test getting user sites"""
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create a test site first
        with app.app_context():
            site = Site(
                user_id=self.test_user_id,
                name='Test Site',
                elements='[]',
                canvas_settings='{}'
            )
            db.session.add(site)
            db.session.commit()
        
        response = self.app.get('/api/sites', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_upload_media(self):
        """Test media file upload"""
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create a temporary test file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            tmp.write(b'fake image data')
            tmp_path = tmp.name
        
        try:
            with open(tmp_path, 'rb') as f:
                response = self.app.post('/api/media',
                                       data={'file': (f, 'test.jpg')},
                                       headers=headers,
                                       content_type='multipart/form-data')
            
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertIn('id', data)
            self.assertIn('filename', data)
        finally:
            os.unlink(tmp_path)

    def test_get_media(self):
        """Test getting media files"""
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create a test media file
        with app.app_context():
            media_file = MediaFile(
                filename='test.jpg',
                original_filename='test.jpg',
                file_path='/tmp/test.jpg',
                file_size=1024,
                mime_type='image/jpeg',
                user_id=self.test_user_id
            )
            db.session.add(media_file)
            db.session.commit()
        
        response = self.app.get('/api/media', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_create_scraping_profile(self):
        """Test scraping profile creation"""
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        response = self.app.post('/api/scraping/profiles',
                               json={
                                   'name': 'Test Profile',
                                   'url': 'https://example.com',
                                   'sections': [],
                                   'fields': [],
                                   'options': {}
                               },
                               headers=headers)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Test Profile')

    def test_get_scraping_profiles(self):
        """Test getting scraping profiles"""
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create a test profile
        with app.app_context():
            profile = ScrapingProfile(
                name='Test Profile',
                url='https://example.com',
                sections='[]',
                fields='[]',
                options='{}'
            )
            db.session.add(profile)
            db.session.commit()
        
        response = self.app.get('/api/scraping/profiles', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_publish_site(self):
        """Test site publishing"""
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create a test site
        with app.app_context():
            site = Site(
                user_id=self.test_user_id,
                name='Test Site',
                elements='[{"type": "text", "content": "Hello World"}]',
                canvas_settings='{"backgroundColor": "#ffffff"}'
            )
            db.session.add(site)
            db.session.commit()
            site_id = site.id
        
        response = self.app.post(f'/api/sites/{site_id}/publish', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('published_url', data)

    def test_unauthorized_access(self):
        """Test unauthorized access to protected endpoints"""
        response = self.app.get('/api/sites')
        self.assertEqual(response.status_code, 401)

    def test_invalid_login(self):
        """Test invalid login credentials"""
        response = self.app.post('/api/auth/login',
                               json={'email': 'test@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)

    def test_duplicate_registration(self):
        """Test duplicate user registration"""
        # First registration
        self.app.post('/api/auth/register',
                     json={
                         'username': 'duplicate',
                         'email': 'duplicate@example.com',
                         'password': 'password123'
                     })
        
        # Second registration with same email
        response = self.app.post('/api/auth/register',
                               json={
                                   'username': 'duplicate2',
                                   'email': 'duplicate@example.com',
                                   'password': 'password123'
                               })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main() 