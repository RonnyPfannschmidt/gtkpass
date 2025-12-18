# Security Policy

## Supported Versions

GTKPass is currently in development. Once released, we will maintain security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in GTKPass, please follow responsible disclosure:

### How to Report

1. **Email**: Send details to the maintainer (see GitHub profile for contact)
2. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)
3. **GPG**: Encrypt sensitive reports with maintainer's GPG key (if available)

### What to Expect

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 1-7 days
  - High: 1-2 weeks
  - Medium: 2-4 weeks
  - Low: Next release

### Disclosure Policy

- We will work with you to understand and fix the issue
- We will credit you in the security advisory (unless you prefer anonymity)
- We will coordinate public disclosure after a fix is available
- Typical embargo period: 90 days or until fix is released

## Security Measures

GTKPass implements multiple security layers:

### Data Protection

1. **Encryption at Rest**
   - All passwords encrypted with GPG
   - Follows passwordstore standard
   - Multiple GPG keys supported

2. **Encryption in Transit**
   - Git operations use HTTPS/SSH
   - GPG signatures verified

3. **Memory Protection**
   - Sensitive data cleared after use
   - Clipboard auto-cleared after timeout
   - Secure memory allocation when available

### Access Control

1. **Authentication**
   - GPG passphrase required
   - System keyring integration
   - Session locking support

2. **Authorization**
   - GPG key-based access
   - File system permissions
   - User-controlled sharing via GPG recipients

### Input Validation

1. **All user inputs validated**
2. **Path traversal prevention**
3. **GPG command injection prevention**
4. **XSS prevention in UI**

### Secure Coding Practices

1. **Type safety** (Python type hints)
2. **Input sanitization**
3. **Error handling without information leakage**
4. **No logging of sensitive data**
5. **Regular dependency updates**

## Security Features

### Password Storage
- GPG encryption (default RSA 3072-bit or higher)
- Support for multiple encryption keys
- Signature verification
- Encrypted git repository (optional)

### Password Handling
- No plaintext password storage
- Secure clipboard operations
- Auto-clear clipboard (configurable timeout)
- Password masking in UI
- Screenshot prevention (when supported)

### Session Security
- Auto-lock after inactivity
- Manual lock function
- GPG agent integration
- Keyring passphrase caching

### Network Security
- HTTPS for git remotes
- SSH key authentication support
- Certificate validation
- No telemetry or external connections (except git sync)

## Known Limitations

GTKPass cannot protect against:

1. **System Compromise**
   - Malware with root access
   - Keyloggers
   - Memory dumps by privileged processes

2. **Physical Access**
   - Unlocked system access
   - Cold boot attacks
   - Hardware keyloggers

3. **User Behavior**
   - Weak GPG passphrases
   - Sharing GPG keys insecurely
   - Reusing passwords

4. **Third-Party Software**
   - Compromised GPG installation
   - Malicious clipboard managers
   - Screen capture software

## Security Best Practices

### For Users

1. **Use strong GPG passphrases**
   - 20+ characters recommended
   - Use passphrase, not password
   - Unique to GPG key

2. **Protect GPG keys**
   - Backup securely
   - Use separate subkeys
   - Set expiration dates

3. **Configure security settings**
   - Enable auto-lock
   - Set short clipboard timeout
   - Use keyring integration

4. **Keep software updated**
   - Update GTKPass regularly
   - Keep system packages current
   - Update GnuPG

5. **Use git sync carefully**
   - Use private repositories
   - Use SSH keys for authentication
   - Enable GPG signing for commits

### For Developers

1. **Never log sensitive data**
   - Passwords, passphrases, OTP secrets
   - GPG key material
   - User credentials

2. **Validate all inputs**
   - File paths
   - User data
   - External data (git, GPG)

3. **Clear sensitive data**
   - Zero memory when done
   - Clear clipboard
   - No temp file leakage

4. **Use secure APIs**
   - python-gnupg for GPG
   - keyring for credentials
   - secure random for generation

5. **Review dependencies**
   - Keep updated
   - Check for vulnerabilities
   - Minimize dependencies

## Security Audits

### Internal Audits
- Code review for all changes
- Security checklist for PRs
- Regular dependency scanning
- Static analysis (mypy, ruff)

### External Audits
- Community security review
- Penetration testing (planned)
- Third-party audit (planned for v1.0)

## Vulnerability Disclosure History

None yet (project in development).

Once released, disclosed vulnerabilities will be listed here with:
- CVE ID (if applicable)
- Severity rating
- Affected versions
- Fixed version
- Credit to reporter

## Security Contact

For security concerns, contact the maintainers through:
- GitHub Security Advisories (preferred)
- Email (see GitHub profile)
- GPG encrypted email for sensitive issues

## Related Security Documentation

- [REQUIREMENTS.md - Security Requirements](REQUIREMENTS.md#2-security-and-safety)
- [ARCHITECTURE.md - Security Architecture](ARCHITECTURE.md#security-architecture)
- [passwordstore security](https://www.passwordstore.org/)
- [GPG Best Practices](https://riseup.net/en/security/message-security/openpgp/best-practices)

## Compliance

GTKPass aims to follow:
- OWASP Top 10 guidelines
- CWE/SANS Top 25
- GNOME security recommendations
- Python security best practices

## Security Roadmap

Planned security enhancements:
- [ ] Comprehensive security audit
- [ ] Penetration testing
- [ ] Hardware security key support (YubiKey)
- [ ] Biometric authentication
- [ ] Wayland security features
- [ ] TPM integration
- [ ] Memory encryption
- [ ] FIDO2/WebAuthn support

## Acknowledgments

We thank the security research community for helping keep GTKPass secure.

Security researchers who report vulnerabilities responsibly will be acknowledged in:
- Security advisories
- Release notes
- SECURITY.md (this file)

## License

This security policy is part of GTKPass and is licensed under GPL-3.0.

---

**Last Updated**: December 2024
