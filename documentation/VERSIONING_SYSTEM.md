# Versioning System

This project uses a versioned file system similar to Git, where each version is preserved and the current version is clearly labeled.

## Structure

```
Gravel Landing Page Project/
├── versions/
│   ├── v1.0.0/
│   │   └── current/ (symlink or copy of latest)
│   ├── v1.0.1/
│   │   └── current/
│   └── ...
├── current -> versions/v[X.X.X]/current (symlink to active version)
└── VERSIONING_SYSTEM.md (this file)
```

## Version Naming

- **Major version (X.0.0)**: Major structural changes, new plan types
- **Minor version (0.X.0)**: New races added, significant feature additions
- **Patch version (0.0.X)**: Bug fixes, small modifications

## Creating New Versions

When making changes:
1. Copy current version to new version folder
2. Make changes in new version
3. Update "current" symlink to point to new version
4. Old versions remain intact for reference

## Current Version

The `current` folder (or symlink) always points to the active version.

## File Organization

Each version contains:
- All plan templates (JSON + Python)
- All guidelines (nutrition, altitude, technical)
- All documentation
- All race-specific implementations

## Best Practices

- Never modify files directly in version folders
- Always create a new version for changes
- Document changes in version folder's CHANGELOG.md
- Keep "current" clearly labeled
