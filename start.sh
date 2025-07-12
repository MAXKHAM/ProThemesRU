#!/bin/bash

# ProThemesRU Startup Script
# This script provides easy startup and management of the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python() {
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_success "Python $PYTHON_VERSION found"
            return 0
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            return 1
        fi
    else
        print_error "Python 3 not found"
        return 1
    fi
}

# Function to check Node.js version
check_node() {
    if command_exists node; then
        NODE_VERSION=$(node -v)
        if node -e "process.exit(process.version.split('v')[1].split('.')[0] >= 16 ? 0 : 1)"; then
            print_success "Node.js $NODE_VERSION found"
            return 0
        else
            print_error "Node.js 16+ required, found $NODE_VERSION"
            return 1
        fi
    else
        print_error "Node.js not found"
        return 1
    fi
}

# Function to setup virtual environment
setup_venv() {
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    print_status "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Function to install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    print_success "Python dependencies installed"
}

# Function to install Node.js dependencies
install_node_deps() {
    print_status "Installing Node.js dependencies..."
    cd react-canvas-editor
    npm install
    cd ..
    print_success "Node.js dependencies installed"
}

# Function to setup database
setup_database() {
    print_status "Setting up database..."
    python run.py --mode init
    print_success "Database setup complete"
}

# Function to start backend
start_backend() {
    print_status "Starting backend server..."
    python run.py --mode dev &
    BACKEND_PID=$!
    print_success "Backend started (PID: $BACKEND_PID)"
}

# Function to start frontend
start_frontend() {
    print_status "Starting frontend server..."
    cd react-canvas-editor
    npm start &
    FRONTEND_PID=$!
    cd ..
    print_success "Frontend started (PID: $FRONTEND_PID)"
}

# Function to stop servers
stop_servers() {
    print_status "Stopping servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        print_success "Backend stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        print_success "Frontend stopped"
    fi
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    python test_runner.py
    print_success "Tests completed"
}

# Function to show help
show_help() {
    echo "ProThemesRU Startup Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  install    - Install all dependencies"
    echo "  setup      - Setup database and initial configuration"
    echo "  start      - Start both backend and frontend servers"
    echo "  backend    - Start only backend server"
    echo "  frontend   - Start only frontend server"
    echo "  stop       - Stop all servers"
    echo "  test       - Run tests"
    echo "  clean      - Clean up temporary files"
    echo "  help       - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install    # Install dependencies"
    echo "  $0 setup      # Setup database"
    echo "  $0 start      # Start application"
}

# Function to clean up
cleanup() {
    print_status "Cleaning up..."
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -delete
    find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
    print_success "Cleanup complete"
}

# Main script logic
case "${1:-help}" in
    install)
        print_status "Installing ProThemesRU..."
        check_python || exit 1
        check_node || exit 1
        setup_venv
        install_python_deps
        install_node_deps
        print_success "Installation complete!"
        ;;
    setup)
        print_status "Setting up ProThemesRU..."
        setup_venv
        setup_database
        print_success "Setup complete!"
        ;;
    start)
        print_status "Starting ProThemesRU..."
        setup_venv
        start_backend
        sleep 3
        start_frontend
        print_success "ProThemesRU started!"
        print_status "Backend: http://localhost:5000"
        print_status "Frontend: http://localhost:3000"
        print_status "Press Ctrl+C to stop"
        trap stop_servers EXIT
        wait
        ;;
    backend)
        print_status "Starting backend..."
        setup_venv
        start_backend
        print_success "Backend started at http://localhost:5000"
        print_status "Press Ctrl+C to stop"
        trap stop_servers EXIT
        wait
        ;;
    frontend)
        print_status "Starting frontend..."
        start_frontend
        print_success "Frontend started at http://localhost:3000"
        print_status "Press Ctrl+C to stop"
        trap stop_servers EXIT
        wait
        ;;
    stop)
        stop_servers
        ;;
    test)
        setup_venv
        run_tests
        ;;
    clean)
        cleanup
        ;;
    help|*)
        show_help
        ;;
esac 