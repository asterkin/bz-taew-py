#!/bin/bash

# Python version upgrade script
# Traverses sub-projects with pyproject.toml and upgrades Python version using uv
# Stops on first failure

set -e  # Exit immediately if any command fails

# Check if Python version argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <python-version>"
    echo "Example: $0 3.13.7"
    exit 1
fi

PYTHON_VERSION="$1"

echo "=== Python Version Upgrade Script ==="
echo "Upgrading all adapter sub-projects to Python $PYTHON_VERSION..."
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

# Find all directories with pyproject.toml, excluding project-template
SUBPROJECTS=$(find . -name "pyproject.toml" -exec dirname {} \; | while read dir; do
    if [ "$dir" != "./project-template" ]; then
        echo "$dir"
    fi
done | sort)

if [ -z "$SUBPROJECTS" ]; then
    echo "No sub-projects found with pyproject.toml"
    exit 1
fi

echo "Found sub-projects:"
echo "$SUBPROJECTS"
echo

# Upgrade Python version in each sub-project
for project in $SUBPROJECTS; do
    echo "================================================"
    echo "Upgrading Python version in project: $project"
    echo "================================================"
    
    # Change to project directory
    cd "$ORIGINAL_DIR/$project"
    
    # Check if .venv exists and activate it
    if [ ! -d ".venv" ]; then
        echo "Warning: No .venv found in $project"
        echo "Skipping virtual environment activation..."
    else
        echo "Activating virtual environment..."
        source .venv/bin/activate
    fi
    
    # Pin Python version using uv
    echo "Pinning Python version to $PYTHON_VERSION..."
    if ! uv python pin "$PYTHON_VERSION"; then
        echo "ERROR: Failed to pin Python version in $project"
        exit 1
    fi
    
    # Sync dependencies
    echo "Syncing dependencies..."
    if ! uv sync; then
        echo "ERROR: Failed to sync dependencies in $project"
        exit 1
    fi
    
    # Deactivate virtual environment if it was activated
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "Deactivating virtual environment..."
        deactivate
    fi
    
    echo "✓ Successfully upgraded Python version in $project"
    echo
done

# Return to original directory
cd "$ORIGINAL_DIR"

echo "================================================"
echo "✓ All sub-projects upgraded to Python $PYTHON_VERSION successfully!"
echo "================================================"
