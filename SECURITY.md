# Security

Agent Black Box is intended to help inspect and share agent traces safely, but trace files can still contain sensitive information.

## Current guidance

- treat raw traces as potentially sensitive
- use redaction before sharing traces publicly
- do not commit secrets, tokens, or private production traces to the repository
- prefer local-first workflows for debugging

## Reporting

If you discover a security issue in the project itself, open a private security report through GitHub once the repository is public, or contact the maintainer directly if that path is not yet available.
