# Security Policy

## Supported Versions

The following table indicates which versions of the project currently receive security updates.

| Version | Supported |
|---------|-----------|
| main | ✅ |
| Previous versions | ❌ |

---

## Reporting a Vulnerability

If you discover a security vulnerability, please do not create a public GitHub Issue.

Instead:

1. Contact the project maintainer privately.
2. Provide a detailed description of the vulnerability.
3. Include steps to reproduce the issue.
4. If possible, include a proposed solution.

The vulnerability will be reviewed as soon as possible.

---

## Security Best Practices

This project follows several security practices:

- Passwords are securely hashed using bcrypt.
- Authentication is performed using JWT.
- Role-Based Access Control (RBAC).
- SQLAlchemy ORM is used to prevent SQL Injection.
- Input validation is performed with Pydantic.
- Sensitive configuration is stored using environment variables.
- Uploaded files are validated before storage.
- Automated security scans are executed through GitHub Actions.

---

## Future Improvements

The following security enhancements are planned:

- Refresh Tokens
- Multi-Factor Authentication (MFA)
- Login Rate Limiting
- Email Verification
- Password Recovery
- Audit Dashboard
- Antivirus scanning for uploaded files
- Object Storage (AWS S3 / MinIO)