#!/bin/bash

# Financial Forecast Dashboard Deployment Script
# This script helps you deploy the dashboard to various platforms

set -e

echo "🚀 Financial Forecast Dashboard Deployment Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[HEADER]${NC} $1"
}

# Check if Python is installed
check_python() {
    if command -v python3 &> /dev/null; then
        print_status "Python 3 found: $(python3 --version)"
    else
        print_error "Python 3 is not installed. Please install Python 3.7+ first."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    if command -v pip3 &> /dev/null; then
        print_status "pip3 found"
    else
        print_error "pip3 is not installed. Please install pip first."
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_header "Installing Python dependencies..."
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
        print_status "Dependencies installed successfully"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Create necessary directories
create_directories() {
    print_header "Creating necessary directories..."
    mkdir -p Input Output/spreadsheets Output/heatmaps Output/charts Output/summaries uploads logs
    print_status "Directories created successfully"
}

# Start the dashboard
start_dashboard() {
    print_header "Starting the Financial Forecast Dashboard..."
    print_status "Dashboard will be available at: http://localhost:5000"
    print_status "Press Ctrl+C to stop the server"
    python3 app.py
}

# Docker deployment
docker_deploy() {
    print_header "Deploying with Docker..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if [ -f "Dockerfile" ]; then
        print_status "Building Docker image..."
        docker build -t financial-dashboard .
        
        print_status "Starting Docker container..."
        docker run -d -p 5000:5000 --name financial-dashboard financial-dashboard
        
        print_status "Dashboard deployed successfully with Docker!"
        print_status "Access at: http://localhost:5000"
        print_status "To stop: docker stop financial-dashboard"
        print_status "To remove: docker rm financial-dashboard"
    else
        print_error "Dockerfile not found"
        exit 1
    fi
}

# Docker Compose deployment
docker_compose_deploy() {
    print_header "Deploying with Docker Compose..."
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    if [ -f "docker-compose.yml" ]; then
        print_status "Starting services with Docker Compose..."
        docker-compose up -d
        
        print_status "Dashboard deployed successfully with Docker Compose!"
        print_status "Access at: http://localhost:5000"
        print_status "To stop: docker-compose down"
        print_status "To view logs: docker-compose logs -f"
    else
        print_error "docker-compose.yml not found"
        exit 1
    fi
}

# Production deployment
production_deploy() {
    print_header "Production Deployment Guide"
    echo ""
    echo "For production deployment, consider the following options:"
    echo ""
    echo "1. Heroku:"
    echo "   - Install Heroku CLI"
    echo "   - Run: heroku create your-app-name"
    echo "   - Run: git push heroku main"
    echo ""
    echo "2. AWS:"
    echo "   - Use AWS Elastic Beanstalk"
    echo "   - Or deploy to EC2 with gunicorn"
    echo ""
    echo "3. Google Cloud:"
    echo "   - Deploy to App Engine"
    echo "   - Or use Cloud Run"
    echo ""
    echo "4. Azure:"
    echo "   - Deploy to App Service"
    echo ""
    echo "5. DigitalOcean:"
    echo "   - Deploy to App Platform"
    echo "   - Or use Droplets with gunicorn"
    echo ""
    echo "For all platforms, ensure you:"
    echo "- Set FLASK_ENV=production"
    echo "- Use a production WSGI server (gunicorn, uwsgi)"
    echo "- Set up proper environment variables"
    echo "- Configure HTTPS/SSL"
    echo "- Set up monitoring and logging"
}

# Show help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  local       - Run dashboard locally (default)"
    echo "  docker      - Deploy with Docker"
    echo "  compose     - Deploy with Docker Compose"
    echo "  production  - Show production deployment guide"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0              # Run locally"
    echo "  $0 docker       # Deploy with Docker"
    echo "  $0 compose      # Deploy with Docker Compose"
    echo "  $0 production   # Show production guide"
}

# Main script logic
main() {
    case "${1:-local}" in
        "local")
            check_python
            check_pip
            install_dependencies
            create_directories
            start_dashboard
            ;;
        "docker")
            docker_deploy
            ;;
        "compose")
            docker_compose_deploy
            ;;
        "production")
            production_deploy
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
