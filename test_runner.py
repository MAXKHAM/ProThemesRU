#!/usr/bin/env python3
"""
Test Runner for ProThemesRU
This script runs all tests and generates a comprehensive report.
"""

import unittest
import sys
import os
import coverage
from datetime import datetime

def run_tests_with_coverage():
    """Run tests with coverage reporting"""
    # Start coverage measurement
    cov = coverage.Coverage()
    cov.start()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Stop coverage measurement
    cov.stop()
    cov.save()
    
    # Generate coverage report
    print("\n" + "="*50)
    print("COVERAGE REPORT")
    print("="*50)
    cov.report()
    
    # Generate HTML coverage report
    cov.html_report(directory='htmlcov')
    print(f"\nHTML coverage report generated in 'htmlcov' directory")
    
    return result.wasSuccessful()

def run_specific_test(test_name):
    """Run a specific test"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_name)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def main():
    """Main test runner function"""
    print("🧪 ProThemesRU Test Runner")
    print("="*50)
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        print(f"Running specific test: {test_name}")
        success = run_specific_test(test_name)
    else:
        print("Running all tests with coverage...")
        success = run_tests_with_coverage()
    
    print("\n" + "="*50)
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == '__main__':
    main() 