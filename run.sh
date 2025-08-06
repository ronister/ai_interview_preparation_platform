#!/bin/bash

# Set the execution environment flag
IS_EXECUTION_ENVIRONMENT=false

if [ "$IS_EXECUTION_ENVIRONMENT" = true ]; then
    echo "Running in execution environment mode..."
    msb server start --dev
else
    echo "Running in development mode..."
    
    # Run Django server in background
    echo "Starting Django server..."
    . .venv/bin/activate && python manage.py runserver &
    DJANGO_PID=$!
    
    # Run yarn start
    echo "Starting yarn..."
    yarn start &
    YARN_PID=$!
    
    # Function to handle cleanup on script exit
    cleanup() {
        echo "Shutting down servers..."
        kill $DJANGO_PID 2>/dev/null
        kill $YARN_PID 2>/dev/null
        exit
    }
    
    # Set up trap to catch interrupts and perform cleanup
    trap cleanup INT TERM
    
    # Wait for both processes
    wait $DJANGO_PID $YARN_PID
fi
