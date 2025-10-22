#!/bin/bash

# Master build script to run all adapter Makefiles
# Traverses sub-projects with pyproject.toml and Makefile, activates .venv, runs make, deactivates .venv
# Stops on first failure

set -e  # Exit immediately if any command fails

echo "=== Master Build Script ==="
echo "Building all adapter sub-projects..."
echo

# Store original directory
ORIGINAL_DIR=$(pwd)

# Function to clean up on exit
cleanup() {
    cd "$ORIGINAL_DIR"
    if [[ -n "$VIRTUAL_ENV" ]]; then
        deactivate 2>/dev/null || true
    fi
}

# Set trap to ensure cleanup on script exit
trap cleanup EXIT

# Find all directories with both pyproject.toml and Makefile, excluding project-template
SUBPROJECTS=$(find . -name "pyproject.toml" -exec dirname {} \; | while read dir; do
    if [ -f "$dir/Makefile" ] && [ "$dir" != "./project-template" ]; then
        echo "$dir"
    fi
done | sort)

if [ -z "$SUBPROJECTS" ]; then
    echo "No sub-projects found with both pyproject.toml and Makefile"
    exit 1
fi

echo "Found sub-projects:"
echo "$SUBPROJECTS"
echo

# Build each sub-project
for project in $SUBPROJECTS; do
    echo "================================================"
    echo "Building project: $project"
    echo "================================================"
    
    # Change to project directory
    cd "$ORIGINAL_DIR/$project"
    
    # Check if .venv exists and activate it
    if [ ! -d ".venv" ]; then
        echo "Warning: No .venv found in $project"
        echo "Attempting to run make without virtual environment..."
    else
        echo "Activating virtual environment..."
        source .venv/bin/activate
    fi
    uv sync --all-groups
    
    # Check if .env exists and source it for PYTHONPATH/PATH settings
    if [ -f ".env" ]; then
        echo "Sourcing .env file for environment variables..."
        source ./.env
    else
        echo "Warning: No .env found in $project"
    fi
    
    # Run make
    echo "Running make..."
    if ! make; then
        echo "ERROR: Make failed in $project"
        exit 1
    fi
    
    # Deactivate virtual environment if it was activated
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "Deactivating virtual environment..."
        deactivate
    fi
    
    echo "✓ Successfully built $project"
    echo
done

# Return to original directory
cd "$ORIGINAL_DIR"

echo "================================================"
echo "✓ All sub-projects built successfully!"
echo "================================================"
