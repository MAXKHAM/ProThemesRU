import unittest
import os
import sys

# Добавляем путь к проекту в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == '__main__':
    # Запускаем все тесты в директории tests
    loader = unittest.TestLoader()
    tests = loader.discover('tests')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(tests)
    
    # Выходим с кодом ошибки, если тесты не прошли
    if not result.wasSuccessful():
        sys.exit(1)
