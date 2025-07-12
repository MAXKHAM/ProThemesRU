#!/usr/bin/env python3
"""
Скрипт для запуска тестов ProThemes
"""

import sys
import os
import unittest
from pathlib import Path

# Добавляем корневую директорию в путь
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def run_tests():
    """Запуск всех тестов"""
    print("🧪 Запуск тестов ProThemes...")
    
    # Находим все тестовые файлы
    test_dir = root_dir / 'tests'
    test_files = []
    
    if test_dir.exists():
        for file in test_dir.rglob('test_*.py'):
            test_files.append(str(file.relative_to(root_dir)).replace('/', '.').replace('.py', ''))
    
    if not test_files:
        print("❌ Тестовые файлы не найдены")
        return False
    
    print(f"📁 Найдено тестовых файлов: {len(test_files)}")
    
    # Запускаем тесты
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    for test_file in test_files:
        try:
            tests = loader.loadTestsFromName(test_file)
            suite.addTests(tests)
            print(f"✅ Загружен: {test_file}")
        except Exception as e:
            print(f"❌ Ошибка загрузки {test_file}: {e}")
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим результаты
    print("\n" + "="*50)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("="*50)
    print(f"✅ Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Ошибки: {len(result.errors)}")
    print(f"⚠️  Провалы: {len(result.failures)}")
    print(f"📈 Общий результат: {result.testsRun} тестов")
    
    if result.failures:
        print("\n🔍 ПРОВАЛЕННЫЕ ТЕСТЫ:")
        for test, traceback in result.failures:
            print(f"❌ {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n🚨 ОШИБКИ В ТЕСТАХ:")
        for test, traceback in result.errors:
            print(f"💥 {test}: {traceback.split('Exception:')[-1].strip()}")
    
    return len(result.failures) == 0 and len(result.errors) == 0

def run_coverage():
    """Запуск тестов с покрытием кода"""
    try:
        import coverage
        print("📊 Запуск тестов с покрытием кода...")
        
        # Инициализируем coverage
        cov = coverage.Coverage()
        cov.start()
        
        # Запускаем тесты
        success = run_tests()
        
        # Останавливаем coverage
        cov.stop()
        cov.save()
        
        # Генерируем отчет
        print("\n📈 ОТЧЕТ О ПОКРЫТИИ КОДА:")
        cov.report()
        
        # Сохраняем HTML отчет
        cov.html_report(directory='htmlcov')
        print("📁 HTML отчет сохранен в htmlcov/")
        
        return success
        
    except ImportError:
        print("❌ coverage не установлен. Установите: pip install coverage")
        return run_tests()

def run_specific_test(test_name):
    """Запуск конкретного теста"""
    print(f"🎯 Запуск теста: {test_name}")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_name)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return len(result.failures) == 0 and len(result.errors) == 0

def main():
    """Основная функция"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'coverage':
            success = run_coverage()
        elif command == 'test':
            test_name = sys.argv[2] if len(sys.argv) > 2 else None
            if test_name:
                success = run_specific_test(test_name)
            else:
                success = run_tests()
        else:
            print(f"❌ Неизвестная команда: {command}")
            print("Доступные команды: test, coverage")
            return False
    else:
        success = run_tests()
    
    if success:
        print("\n🎉 Все тесты прошли успешно!")
        return True
    else:
        print("\n💥 Некоторые тесты не прошли!")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
