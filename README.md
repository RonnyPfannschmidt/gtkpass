# GTKPass

A modern GTK4-based password manager for GNOME/Linux, designed as an alternative to qtpass.

## Overview

GTKPass is a user-friendly password manager that integrates seamlessly with the GNOME desktop environment. It uses the standard passwordstore (pass) format for compatibility with existing tools while providing a modern, native GTK4/Libadwaita interface.

## Features (Planned)

- 🔐 **Secure Password Management**: GPG-encrypted password storage
- 🌳 **Hierarchical Organization**: Organize passwords in folders
- 🔍 **Fast Search**: Quickly find passwords with incremental search
- 🔑 **Password Generation**: Generate secure passwords and passphrases
- 📱 **OTP Support**: Time-based and HMAC-based one-time passwords (TOTP/HOTP)
- 📷 **QR Code Support**: Generate and scan QR codes for OTP secrets
- 🔄 **Git Integration**: Automatic version control and sync
- 🔐 **Keyring Integration**: Secure GPG passphrase storage
- 🎨 **Modern UI**: GTK4 + Libadwaita with dark mode support
- ⚡ **Fast & Native**: Written in Python with native GTK bindings
- 🔄 **Lifecycle Management**: Track password age, detect weak/duplicate passwords

## Status

**This project is currently in the planning and documentation phase.**

The specifications and architecture have been defined. Implementation will begin soon. See [ROADMAP.md](ROADMAP.md) for the development plan.

## Documentation

- [Requirements Specification](REQUIREMENTS.md) - Detailed feature requirements
- [Architecture Overview](ARCHITECTURE.md) - Technical architecture and design
- [Development Roadmap](ROADMAP.md) - Implementation timeline and milestones
- [Claude AI Guide](CLAUDE.md) - Guidelines for AI-assisted development

## Requirements

- Python 3.10+
- GTK4 4.10+
- Libadwaita 1.4+
- GnuPG 2.x
- Git (optional, for version control)

## Installation

**Not yet available** - Installation instructions will be provided when the first release is ready.

Planned distribution methods:
- PyPI package (`pip install gtkpass`)
- Flatpak (Flathub)
- Distribution packages (.deb, .rpm)

## Usage

Coming soon - detailed usage instructions will be provided with the first release.

## Development

### Project Structure

The project will follow this structure:

```
gtkpass/
├── src/gtkpass/          # Main application code
├── tests/                # Test suite
├── data/                 # Icons, desktop files, metadata
├── docs/                 # User and developer documentation
└── pyproject.toml        # Project configuration
```

### Getting Started

Development setup instructions will be provided soon.

### Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Compatibility

GTKPass maintains compatibility with:
- **pass** (passwordstore CLI)
- **qtpass** (can use same password store)
- **pass-otp** (OTP extension)
- **Android Password Store** (via git sync)

## Security

Security is a top priority for GTKPass. The application:
- Uses GPG for encryption/decryption
- Integrates with system keyring for secure storage
- Clears clipboard after configurable timeout
- Supports session locking
- Never logs sensitive data

See [REQUIREMENTS.md](REQUIREMENTS.md#2-security-and-safety) for detailed security requirements.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [passwordstore](https://www.passwordstore.org/) - The original pass utility
- [qtpass](https://qtpass.org/) - Inspiration for this project
- [GNOME](https://www.gnome.org/) - For the excellent GTK toolkit
- All contributors to the password management ecosystem

## Contact

- Issues: [GitHub Issues](https://github.com/RonnyPfannschmidt/gtkpass/issues)
- Discussions: [GitHub Discussions](https://github.com/RonnyPfannschmidt/gtkpass/discussions)

## Roadmap

See [ROADMAP.md](ROADMAP.md) for detailed development plans and timeline.

**Target**: First release (v1.0) in approximately 5-6 months of development.
