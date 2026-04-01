# CLAUDE.md — Finance Advisory AI

This file defines the rules, conventions, and guidelines for Claude Code when working in this repository.

---

## Project Overview

**Finance Advisory AI** is an AI-powered financial advisory system. It provides intelligent financial analysis, portfolio recommendations, risk assessment, and personalized financial guidance.

---

## Git Flow Rules (MANDATORY)

This project uses **Git Flow**. All contributors and AI agents MUST follow these rules strictly.

### Branch Structure

```
main          ← production-ready code only (protected)
develop       ← integration branch for features (protected)
feature/*     ← new features (branch from develop)
release/*     ← release preparation (branch from develop)
hotfix/*      ← critical production fixes (branch from main)
bugfix/*      ← bug fixes (branch from develop)
claude/*      ← Claude Code task branches (branch from develop)
```

### Branch Naming Conventions

| Type      | Pattern                        | Example                          |
|-----------|--------------------------------|----------------------------------|
| Feature   | `feature/<short-description>`  | `feature/portfolio-analysis`     |
| Release   | `release/<version>`            | `release/1.2.0`                  |
| Hotfix    | `hotfix/<short-description>`   | `hotfix/auth-token-expiry`       |
| Bugfix    | `bugfix/<short-description>`   | `bugfix/calculation-error`       |
| Claude    | `claude/<task-description>`    | `claude/setup-gitflow`           |

### Branch Rules (ENFORCE)

- **NEVER** commit directly to `main` or `develop`
- **NEVER** merge `feature/*` directly into `main`
- **NEVER** push broken/untested code to `develop`
- Features must be merged into `develop` via Pull Request
- Releases branch off `develop`, merge into both `main` AND `develop`
- Hotfixes branch off `main`, merge into both `main` AND `develop`
- All merges to `main` require at least 1 code review approval
- All merges to `develop` require passing CI checks

### Merge Strategy

- Use **squash merges** for `feature/*` → `develop` (clean history)
- Use **merge commits** (no fast-forward) for `release/*` and `hotfix/*`
- Tag `main` after every release: `git tag -a v1.0.0 -m "Release 1.0.0"`

---

## Commit Message Format (MANDATORY)

Use **Conventional Commits** format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### Types

| Type       | When to use                                     |
|------------|-------------------------------------------------|
| `feat`     | New feature                                     |
| `fix`      | Bug fix                                         |
| `docs`     | Documentation changes                           |
| `style`    | Formatting, no logic change                     |
| `refactor` | Code restructure, no feature/fix                |
| `test`     | Adding or modifying tests                       |
| `chore`    | Build process, dependencies, tooling            |
| `perf`     | Performance improvements                        |
| `ci`       | CI/CD configuration changes                     |
| `security` | Security-related changes                        |

### Examples

```
feat(portfolio): add risk-adjusted return calculation
fix(auth): resolve JWT token expiration handling
docs(api): update financial endpoints documentation
security(data): encrypt user financial data at rest
```

---

## Code Standards

### General Rules

- Write **clean, readable, self-documenting** code
- Keep functions small and focused (single responsibility)
- No hardcoded credentials, API keys, or secrets — use environment variables
- All sensitive financial data must be encrypted at rest and in transit
- Input validation on all user-facing and API endpoints
- No `console.log` / `print` debug statements in production code

### Security (Critical for Financial Apps)

- **NEVER** log financial data (account numbers, balances, transactions)
- **NEVER** store plaintext passwords or API keys
- Use parameterized queries — no raw SQL string concatenation
- Validate and sanitize all inputs (prevent XSS, SQL injection)
- Follow OWASP Top 10 guidelines
- All financial calculations must be auditable and traceable

### Testing Requirements

- Unit tests required for all business logic
- Integration tests required for all API endpoints
- Test coverage minimum: **80%**
- All tests must pass before merging to `develop`
- Financial calculation tests must cover edge cases (zero, negative, large numbers)

---

## Project Structure (Planned)

```
Finance-advisory-AI-srg/
├── src/
│   ├── api/          # REST API endpoints
│   ├── services/     # Business logic (financial calculations, AI)
│   ├── models/       # Data models
│   ├── utils/        # Shared utilities
│   └── config/       # Configuration
├── tests/
│   ├── unit/
│   └── integration/
├── docs/             # API and architecture documentation
├── .github/
│   ├── workflows/    # CI/CD pipelines
│   └── PULL_REQUEST_TEMPLATE.md
├── CLAUDE.md         # This file
├── README.md
└── .gitignore
```

---

## Pull Request Rules

Every PR must include:
1. **Description** of what changed and why
2. **Testing** — what was tested and how
3. **Breaking changes** — if any, clearly documented
4. **Security impact** — for any auth/data changes

PR title must follow Conventional Commits format.

---

## What Claude Code Should Do

When working in this repository, Claude Code must:

1. **Always** create branches from the correct parent:
   - `feature/*` → from `develop`
   - `hotfix/*` → from `main`
   - `bugfix/*` → from `develop`
   - `claude/*` → from `develop`

2. **Always** use Conventional Commits format

3. **Never** push directly to `main` or `develop`

4. **Always** ensure tests pass before pushing

5. **Always** check for security issues in financial logic

6. **Never** commit `.env`, secrets, or credentials

7. **Always** push to the designated feature/task branch and open a PR

---

## Environment Variables

Never commit these. Use `.env.local` or secrets manager:

```
DATABASE_URL
API_KEY_OPENAI
JWT_SECRET
ENCRYPTION_KEY
FINANCIAL_DATA_API_KEY
```

---

## Versioning

This project follows [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- `MAJOR` — breaking changes
- `MINOR` — new backwards-compatible features
- `PATCH` — backwards-compatible bug fixes
