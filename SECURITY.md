# Security Policy

## Supported versions

Security fixes are provided for the latest Anunnaki release on the default branch.

## Reporting a vulnerability

Please report suspected vulnerabilities privately to the repository owner. Include the affected version, reproduction steps, impact, and a suggested mitigation where possible. Do not include private documents, access tokens, or secrets in a public issue or proof of concept.

## Data handling

Anunnaki processes user-selected files locally. It does not upload document content or send it across the network by default. Optional capabilities exposed by the underlying MarkItDown dependency may have their own configuration and security considerations; users should review those before enabling them.

Treat source and converted files as sensitive when their contents are sensitive.
