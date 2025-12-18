#!/bin/bash
# Compile Blueprint files to GTK UI XML files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLUEPRINT_DIR="$SCRIPT_DIR/src/gtkpass/ui/blueprints"

echo "Compiling Blueprint files..."

# Check if blueprint-compiler is available
if ! command -v blueprint-compiler &> /dev/null; then
    echo "Warning: blueprint-compiler not found. Blueprint files will not be compiled."
    echo "Install it with: pip install blueprint-compiler"
    echo "Or on Fedora: sudo dnf install blueprint-compiler"
    echo "Or on Ubuntu: Install from https://github.com/jwestman/blueprint-compiler"
    echo ""
    echo "For development, you can install it with:"
    echo "  pip install blueprint-compiler"
    exit 0
fi

# Compile each .blp file to .ui
for blp_file in "$BLUEPRINT_DIR"/*.blp; do
    if [ -f "$blp_file" ]; then
        ui_file="${blp_file%.blp}.ui"
        echo "  Compiling $(basename "$blp_file") -> $(basename "$ui_file")"
        blueprint-compiler compile "$blp_file" --output "$ui_file"
    fi
done

echo "Blueprint compilation complete!"
