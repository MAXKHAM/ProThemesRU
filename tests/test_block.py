import unittest
from app import create_app, db
from app.models import SiteBlock
from app.services.block_service import BlockService

class BlockModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_block_creation(self):
        """Тестирование создания блока"""
        block = SiteBlock(
            name='Test Block',
            html_content='<div class="block">Test content</div>',
            css_content='.block { padding: 20px; }',
            js_content='console.log("Block loaded");'
        )
        db.session.add(block)
        db.session.commit()
        
        self.assertIsNotNone(block.id)
        self.assertEqual(block.name, 'Test Block')

    def test_block_service(self):
        """Тестирование сервиса блоков"""
        # Создаем тестовый блок
        block = SiteBlock(
            name='Test Block',
            html_content='<div class="block">Test content</div>',
            css_content='.block { padding: 20px; }',
            js_content='console.log("Block loaded");'
        )
        db.session.add(block)
        db.session.commit()

        # Получаем блок через сервис
        retrieved_block = BlockService.get_block_by_id(block.id)
        self.assertIsNotNone(retrieved_block)
        self.assertEqual(retrieved_block.name, 'Test Block')

        # Тестируем генерацию сайта
        blocks = [block]
        zip_stream = BlockService.generate_site(blocks)
        self.assertIsNotNone(zip_stream)

if __name__ == '__main__':
    unittest.main()
