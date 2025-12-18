# GTKPass Development Roadmap

## Project Goals

Create a modern, secure, and user-friendly password manager for GNOME/Linux that serves as a complete alternative to qtpass while maintaining compatibility with the passwordstore ecosystem.

## Development Phases

### Phase 0: Foundation (Week 1-2)

**Goal**: Establish project structure and core infrastructure

- [x] Create requirements specification
- [x] Create architecture documentation
- [x] Create Claude AI configuration
- [x] Set up project structure
- [x] Configure build system (pyproject.toml)
- [x] Set up testing framework (pytest)
- [x] Configure linting and formatting (ruff, mypy)
- [x] Create basic GTK4 application scaffold
- [x] Create service layer infrastructure
- [x] Create background/threading service
- [ ] Set up CI/CD pipeline
- [ ] Create basic README with setup instructions
- [ ] Create CONTRIBUTING.md guidelines

**Deliverables**:
- Complete project scaffolding
- Working development environment
- Basic CI/CD pipeline
- Documentation framework

### Phase 1: Core Password Management (Week 3-6)

**Goal**: Implement basic password store operations

**Milestone 1.1: Data Layer**
- [ ] Implement Password model (REQ-PM-001 to REQ-PM-008)
- [ ] Implement PasswordStore service (REQ-PS-006 to REQ-PS-011)
- [ ] Implement GPG service (REQ-SEC-001 to REQ-SEC-005)
- [ ] Add unit tests for models and services
- [ ] Test with existing password stores

**Milestone 1.2: Basic UI**
- [ ] Create main application window (REQ-UI-001 to REQ-UI-006)
- [ ] Implement password list view (REQ-PM-004)
- [ ] Implement password detail view (REQ-PM-006 to REQ-PM-008)
- [ ] Add search functionality (REQ-PM-005)
- [ ] Implement clipboard operations (REQ-PM-006, REQ-SEC-008)

**Milestone 1.3: Password Operations**
- [ ] Implement password viewing (REQ-PM-009)
- [ ] Implement password editing (REQ-PM-010)
- [ ] Implement password deletion (REQ-PM-011)
- [ ] Implement password creation (REQ-GEN-009 to REQ-GEN-014)
- [ ] Add confirmation dialogs

**Deliverables**:
- Working password viewer
- Basic CRUD operations
- Clipboard integration
- GTK4 UI with password list and details

### Phase 2: Security & Git Integration (Week 7-9)

**Goal**: Add git operations and enhanced security features

**Milestone 2.1: Git Operations**
- [ ] Implement Git service (REQ-PS-012 to REQ-PS-017)
- [ ] Auto-commit on password changes (REQ-PS-012)
- [ ] Add git sync functionality (REQ-PS-013, REQ-PS-014)
- [ ] Implement git history view (REQ-PS-015)
- [ ] Handle merge conflicts (REQ-PS-016)

**Milestone 2.2: Keyring Integration**
- [ ] Implement Keyring service (REQ-KEY-001 to REQ-KEY-009)
- [ ] Store GPG passphrase in keyring (REQ-SEC-006)
- [ ] Add keyring configuration options
- [ ] Test with different keyring backends

**Milestone 2.3: Security Features**
- [ ] Implement auto-lock (REQ-SEC-007)
- [ ] Add session locking (REQ-SEC-010)
- [ ] Implement secure memory clearing
- [ ] Add audit logging (optional) (REQ-SEC-011)

**Deliverables**:
- Git synchronization
- Keyring integration
- Enhanced security features
- Session management

### Phase 3: Password Generation & Lifecycle (Week 10-12)

**Goal**: Advanced password management features

**Milestone 3.1: Password Generation**
- [ ] Implement password generator (REQ-GEN-001 to REQ-GEN-008)
- [ ] Add passphrase generation (REQ-GEN-006)
- [ ] Implement strength indicator (REQ-GEN-007)
- [ ] Add generator UI (dialog/popover)
- [ ] Configurable generator settings

**Milestone 3.2: Password Health**
- [ ] Track password age (REQ-LIFE-001 to REQ-LIFE-003)
- [ ] Implement age warnings (REQ-LIFE-004)
- [ ] Detect weak passwords (REQ-LIFE-005)
- [ ] Detect duplicates (REQ-LIFE-006, REQ-LIFE-007)
- [ ] Add password health dashboard

**Milestone 3.3: Lifecycle Management**
- [ ] Implement rotation reminders (REQ-LIFE-008)
- [ ] Track rotation history (REQ-LIFE-009)
- [ ] Add maintenance tools (REQ-LIFE-012 to REQ-LIFE-018)
- [ ] Implement backup/restore (REQ-LIFE-014, REQ-LIFE-015)

**Deliverables**:
- Password generator with UI
- Password health monitoring
- Lifecycle management tools
- Backup/restore functionality

### Phase 4: OTP Support (Week 13-14)

**Goal**: Complete OTP functionality

**Milestone 4.1: OTP Generation**
- [ ] Implement OTP service (REQ-OTP-001 to REQ-OTP-008)
- [ ] Parse otpauth:// URIs (REQ-OTP-003)
- [ ] Display OTP codes with countdown (REQ-OTP-005)
- [ ] Add OTP clipboard copy (REQ-OTP-006)
- [ ] Support custom configurations (REQ-OTP-007, REQ-OTP-008)

**Milestone 4.2: OTP Management**
- [ ] Add OTP to existing passwords (REQ-OTP-009)
- [ ] Edit OTP configuration (REQ-OTP-011)
- [ ] Import from QR code (REQ-OTP-012)
- [ ] Export as QR code (REQ-OTP-013)
- [ ] Ensure pass-otp compatibility (REQ-OTP-014)

**Deliverables**:
- Working TOTP/HOTP generation
- OTP UI integration
- QR code import/export for OTP
- pass-otp compatibility

### Phase 5: QR Code Support (Week 15)

**Goal**: Complete QR code functionality

**Milestone 5.1: QR Generation**
- [ ] Implement QR code generation (REQ-QR-001 to REQ-QR-006)
- [ ] Add QR code display dialog
- [ ] Export QR codes as images
- [ ] Support multiple QR formats (password, OTP, WiFi)

**Milestone 5.2: QR Scanning**
- [ ] Implement webcam scanning (REQ-QR-007)
- [ ] Import from image files (REQ-QR-008)
- [ ] Parse different QR formats (REQ-QR-009, REQ-QR-010)
- [ ] Error handling (REQ-QR-011)

**Deliverables**:
- QR code generation for passwords and OTP
- QR code scanning from camera and files
- Complete QR workflow

### Phase 6: UI Polish & UX (Week 16-18)

**Goal**: Refine user experience and UI

**Milestone 6.1: Modern GTK Features**
- [ ] Convert all UI to Blueprint format (REQ-UI-003)
- [ ] Implement all Libadwaita widgets (REQ-UI-002)
- [ ] Add proper header bar (REQ-UI-007)
- [ ] Implement toast notifications (REQ-UI-011)
- [ ] Add popovers for quick actions (REQ-UI-012)

**Milestone 6.2: User Experience**
- [ ] Add keyboard shortcuts (REQ-UI-015)
- [ ] Implement drag and drop (REQ-UI-016)
- [ ] Add context menus (REQ-UI-017)
- [ ] Quick copy buttons (REQ-UI-018)
- [ ] Visual feedback (REQ-UI-019)
- [ ] Undo/redo (REQ-UI-020)

**Milestone 6.3: Preferences**
- [ ] Create preferences window (REQ-UI-014)
- [ ] Add all configuration options
- [ ] Settings persistence (GSettings)
- [ ] Import/export settings

**Deliverables**:
- Polished modern UI
- Complete keyboard navigation
- Full preferences system
- Smooth user experience

### Phase 7: Documentation & Testing (Week 19-20)

**Goal**: Comprehensive documentation and testing

**Milestone 7.1: User Documentation**
- [ ] Write user manual (REQ-DOC-001)
- [ ] Create getting started guide
- [ ] Document all features
- [ ] Add screenshots and tutorials
- [ ] Create FAQ

**Milestone 7.2: Developer Documentation**
- [ ] Write developer guide (REQ-DOC-002)
- [ ] Document API (REQ-DOC-003)
- [ ] Add code examples
- [ ] Document architecture decisions
- [ ] Create contribution guide (REQ-DOC-005)

**Milestone 7.3: Testing**
- [ ] Achieve 80%+ code coverage (REQ-TEST-001)
- [ ] Write integration tests (REQ-TEST-002)
- [ ] Add UI tests (REQ-TEST-003)
- [ ] Security audit (REQ-TEST-004)
- [ ] Performance testing

**Deliverables**:
- Complete user documentation
- Developer documentation
- Comprehensive test suite
- Security audit report

### Phase 8: Packaging & Release (Week 21-22)

**Goal**: Package and release application

**Milestone 8.1: Distribution Packages**
- [ ] Create PyPI package
- [ ] Build Flatpak package
- [ ] Create AppStream metadata
- [ ] Submit to Flathub
- [ ] Create distribution packages (deb, rpm)

**Milestone 8.2: Release Preparation**
- [ ] Version 1.0.0 release
- [ ] Release notes
- [ ] Migration guide from qtpass
- [ ] Announcement blog post
- [ ] Community outreach

**Deliverables**:
- v1.0.0 release
- Multiple distribution formats
- Release announcement
- Available on Flathub

## Post-Release Roadmap

### Future Features (v1.1+)

**Password Import/Export**
- Import from KeePass, 1Password, LastPass, Bitwarden
- Export to various formats
- Bulk import/export

**Browser Integration**
- Browser extension (Chrome, Firefox)
- Native messaging protocol
- Auto-fill support

**Advanced Features**
- Have I Been Pwned integration
- Password breach checking
- Biometric authentication (fingerprint, face)
- Hardware security key support (YubiKey)

**Platform Support**
- macOS port (GTK on macOS)
- Mobile apps (GNOME mobile, Android)
- Flatpak portal improvements

**Team Features**
- Improved multi-user support
- Role-based access control
- Audit trail for team passwords
- Team management UI

## Development Metrics

### Success Criteria

**Code Quality**
- [ ] 80%+ test coverage
- [ ] Zero critical security issues
- [ ] All CI checks passing
- [ ] Type hints on 100% of public APIs

**Performance**
- [ ] Startup time < 2 seconds
- [ ] Search results < 100ms for 1000+ passwords
- [ ] Smooth UI (60 FPS)

**User Adoption**
- [ ] 100+ GitHub stars
- [ ] Available on Flathub
- [ ] 5+ positive reviews
- [ ] Active community

**Security**
- [ ] Security audit completed
- [ ] No known vulnerabilities
- [ ] Secure coding practices
- [ ] Regular security updates

## Technology Decisions

### Confirmed Technologies

- **Language**: Python 3.10+
- **UI Framework**: GTK4 + Libadwaita
- **UI Definition**: Blueprint (.blp)
- **Password Store**: passwordstore compatible format
- **Encryption**: GPG/GnuPG
- **Version Control**: Git
- **OTP**: pyotp library
- **QR Codes**: qrcode + opencv/zxing
- **Keyring**: python-keyring
- **Testing**: pytest
- **Linting**: ruff + mypy
- **Build**: setuptools or meson

### Under Consideration

- **Build System**: setuptools vs meson (meson preferred for GTK apps)
- **QR Scanner**: opencv-python vs python-zxing
- **Git Library**: GitPython vs pygit2
- **Async**: asyncio vs threading for background tasks

## Risk Management

### Technical Risks

1. **GTK4 Adoption**
   - Risk: GTK4 still relatively new
   - Mitigation: Active GNOME community, good documentation

2. **Blueprint Format**
   - Risk: Blueprint is newer format
   - Mitigation: Fallback to XML if needed, good tooling

3. **Security Issues**
   - Risk: Handling sensitive data
   - Mitigation: Security audit, follow best practices, testing

4. **Platform Compatibility**
   - Risk: Linux-only initially
   - Mitigation: Focus on Linux first, expand later

### Project Risks

1. **Scope Creep**
   - Risk: Adding too many features
   - Mitigation: Strict roadmap, MVP focus

2. **Community Adoption**
   - Risk: Users stick with qtpass
   - Mitigation: Better UX, modern design, active development

3. **Maintenance Burden**
   - Risk: Single maintainer
   - Mitigation: Good documentation, contributor-friendly

## Communication Plan

### Project Visibility

- [ ] GitHub repository
- [ ] Project website/documentation site
- [ ] GNOME GitLab mirror (optional)
- [ ] Social media presence
- [ ] Blog/changelog

### Community Engagement

- [ ] GitHub Discussions
- [ ] Issue templates
- [ ] Pull request guidelines
- [ ] Code of conduct
- [ ] Regular updates/releases

### Marketing

- [ ] Submit to apps.gnome.org
- [ ] Post on r/gnome, r/linux
- [ ] Hacker News announcement
- [ ] GNOME planet blog
- [ ] Password management communities

## Success Metrics

### Month 1 (Post-Release)
- [ ] 50+ GitHub stars
- [ ] 10+ active users
- [ ] 5+ bug reports/feature requests
- [ ] Available on Flathub

### Month 3
- [ ] 200+ GitHub stars
- [ ] 100+ active users
- [ ] First external contribution
- [ ] Positive reviews on Flathub

### Month 6
- [ ] 500+ GitHub stars
- [ ] 500+ active users
- [ ] Active contributor community
- [ ] v1.1 release with new features

### Year 1
- [ ] 1000+ GitHub stars
- [ ] 2000+ active users
- [ ] Mentioned in password manager comparisons
- [ ] v2.0 with major new features

## Resource Requirements

### Development Time
- **Total Estimated**: 22 weeks (5.5 months)
- **Full-time equivalent**: 1 developer
- **Part-time (20h/week)**: 11 months

### Skills Required
- Python development
- GTK/GNOME development
- Security best practices
- UI/UX design
- Documentation writing

### Tools & Services
- GitHub (repository, CI/CD)
- Flathub (distribution)
- ReadTheDocs or similar (documentation)
- Testing infrastructure
- Development machine with GNOME

## Contingency Plans

### If Behind Schedule
1. Reduce scope of initial release
2. Delay non-critical features to v1.1
3. Focus on core password management only
4. Skip some polish items

### If Ahead of Schedule
1. Add import/export features early
2. Start browser extension work
3. Improve documentation
4. Add more tests

### If Critical Issues Found
1. Security issues: Immediate fix and release
2. Data loss bugs: High priority fix
3. UI bugs: Fix in next release
4. Feature requests: Backlog for future

## Conclusion

This roadmap provides a structured approach to developing GTKPass over approximately 5-6 months. The phased approach ensures that core functionality is delivered first, with advanced features and polish added incrementally. Regular milestones and deliverables allow for progress tracking and course correction as needed.
