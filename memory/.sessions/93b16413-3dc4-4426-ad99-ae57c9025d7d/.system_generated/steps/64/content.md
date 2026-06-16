Title: Live Content

Description: Fetched live

Source: https://raw.githubusercontent.com/hackclub/terminal-wakatime/main/install.sh

---

#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO="hackclub/terminal-wakatime"
BINARY_NAME="terminal-wakatime"
INSTALL_DIR="/usr/local/bin"
WAKATIME_DIR="$HOME/.wakatime"

# Function to print colored output
print_status() {
    printf "${BLUE}[INFO]${NC} %s\n" "$1"
}

print_success() {
    printf "${GREEN}[SUCCESS]${NC} %s\n" "$1"
}

print_warning() {
    printf "${YELLOW}[WARNING]${NC} %s\n" "$1"
}

print_error() {
    printf "${RED}[ERROR]${NC} %s\n" "$1"
}

# Function to detect OS and architecture
detect_platform() {
    local os=""
    local arch=""
    
    # Detect OS
    case "$(uname -s)" in
        Linux*)     os="linux";;
        Darwin*)    os="darwin";;
        CYGWIN*|MINGW*|MSYS*) os="windows";;
        *)          print_error "Unsupported operating system: $(uname -s)"; exit 1;;
    esac
    
    # Detect architecture
    case "$(uname -m)" in
        x86_64|amd64)   arch="amd64";;
        arm64|aarch64)  arch="arm64";;
        *)              print_error "Unsupported architecture: $(uname -m)"; exit 1;;
    esac
    
    # Set platform-specific values
    if [ "$os" = "windows" ]; then
        PLATFORM="${os}-${arch}.exe"
        BINARY_NAME="${BINARY_NAME}.exe"
    else
        PLATFORM="${os}-${arch}"
    fi
    
    print_status "Detected platform: $PLATFORM"
}

# Function to get latest release version
get_latest_version() {
    print_status "Fetching latest release information..."
    
    # Try to get latest release from GitHub API
    if command -v curl >/dev/null 2>&1; then
        LATEST_VERSION=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep '"tag_name":' | cut -d '"' -f 4)
    elif command -v wget >/dev/null 2>&1; then
        LATEST_VERSION=$(wget -qO- "https://api.github.com/repos/$REPO/releases/latest" | grep '"tag_name":' | cut -d '"' -f 4)
    else
        print_error "Neither curl nor wget is available. Please install one of them."
        exit 1
    fi
    
    if [ -z "$LATEST_VERSION" ]; then
        print_error "Failed to fetch latest version"
        exit 1
    fi
    
    print_status "Latest version: $LATEST_VERSION"
}

# Function to download binary
download_binary() {
    local download_url="https://github.com/$REPO/releases/download/$LATEST_VERSION/terminal-wakatime-$PLATFORM"
    local temp_file="/tmp/$BINARY_NAME"
    
    print_status "Downloading from: $download_url"
    
    if command -v curl >/dev/null 2>&1; then
        curl -L "$download_url" -o "$temp_file"
    elif command -v wget >/dev/null 2>&1; then
        wget "$download_url" -O "$temp_file"
    else
        print_error "Neither curl nor wget is available"
        exit 1
    fi
    
    if [ ! -f "$temp_file" ]; then
        print_error "Download failed"
        exit 1
    fi
    
    chmod +x "$temp_file"
    print_success "Binary downloaded successfully"
}

# Function to install binary
install_binary() {
    local temp_file="/tmp/$BINARY_NAME"
    
    # Try to install to /usr/local/bin first (system-wide)
    if [ -w "$INSTALL_DIR" ] || sudo -n true 2>/dev/null; then
        print_status "Installing to $INSTALL_DIR (system-wide)..."
        if [ -w "$INSTALL_DIR" ]; then
            mv "$temp_file" "$INSTALL_

