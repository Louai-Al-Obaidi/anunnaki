# Security Policy

## Supported versions

Security fixes are provided for the latest Anunnaki release on the default branch.

## Reporting a vulnerability

Please use [GitHub Security Advisories](https://github.com/Louai-Al-Obaidi/anunnaki/security/advisories/new) to report suspected vulnerabilities privately. If advisories are unavailable, contact the repository owner through GitHub without publishing exploit details. Include the affected version, reproduction steps, impact, and a suggested mitigation where possible. Do not include private documents, access tokens, or secrets in a public issue or proof of concept.

## Download verification

Official Windows binaries are published through GitHub Releases with a
`SHA256SUMS.txt` file. Verify a download before use:

```powershell
Get-FileHash .\Anunnaki-Windows-x64.exe -Algorithm SHA256
```

The result must match the value for that filename in `SHA256SUMS.txt` from the same release. Release binaries are not currently code signed, so Microsoft Defender SmartScreen may display a warning for an unsigned application.

## Data handling

Anunnaki processes user-selected files locally. It does not upload document content or send it across the network by default. Optional capabilities exposed by the underlying MarkItDown dependency may have their own configuration and security considerations; users should review those before enabling them.

Treat source and converted files as sensitive when their contents are sensitive.
