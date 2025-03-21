# Contributing to Executive Orders Archive

Thank you for your interest in contributing to the Executive Orders Archive project! This document provides guidelines and instructions for contributing.

## Development Process

### Branching Strategy

We follow a modified Git Flow branching strategy:

1. **Main Branch (`main`)**
   - Contains production-ready code
   - Protected branch - no direct commits
   - Only accepts merges from `develop` or hotfix branches

2. **Development Branch (`develop`)**
   - Integration branch for features
   - Protected branch - no direct commits
   - Features and bugfixes are merged here first

3. **Feature Branches (`feature/*`)**
   - Created from: `develop`
   - Merge back into: `develop`
   - Naming convention: `feature/feature-name`
   - Example: `feature/timeline-visualization`

4. **Bugfix Branches (`bugfix/*`)**
   - Created from: `develop`
   - Merge back into: `develop`
   - Naming convention: `bugfix/bug-description`
   - Example: `bugfix/fix-date-parsing`

5. **Release Branches (`release/*`)**
   - Created from: `develop`
   - Merge back into: `main` and `develop`
   - Naming convention: `release/version`
   - Example: `release/1.0.0`

### Branch Protection Rules

- `main` and `develop` branches are protected
- Pull request required for merging into protected branches
- Code review required before merging
- CI checks must pass before merging

## Development Workflow

1. **Starting New Work**
   ```powershell
   # Update your local develop branch
   git checkout develop
   git pull origin develop

   # Create a new feature branch
   git checkout -b feature/your-feature-name
   ```

2. **Making Changes**
   - Make your changes in small, logical commits
   - Write clear commit messages
   - Keep your branch up to date with develop

3. **Submitting Changes**
   - Push your branch to GitHub
   - Create a pull request to `develop`
   - Fill out the pull request template
   - Request code review

## Code Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for functions and classes

### JavaScript/TypeScript Code Style (Frontend)

- Use ESLint configuration
- Follow Prettier formatting
- Use TypeScript for new code
- Maximum line length: 100 characters

### Commit Messages

Follow the conventional commits specification:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Code style changes
- refactor: Code refactoring
- test: Adding tests
- chore: Maintenance tasks

### Pull Request Process

1. Update the README.md if necessary
2. Update the documentation
3. Add or update tests
4. Get approval from at least one reviewer
5. Ensure CI checks pass
6. Squash and merge when ready

## Setting Up Development Environment

See the main [README.md](README.md) for detailed setup instructions.

## Questions or Problems?

- Check existing issues
- Create a new issue if needed
- Tag appropriate maintainers
- Join our development discussions

Thank you for contributing to the Executive Orders Archive project!