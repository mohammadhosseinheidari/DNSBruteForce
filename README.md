# DNS Brute Force and Dynamic Discovery Tool

🚀 A powerful tool for DNS brute-forcing and dynamic discovery, leveraging `ksubdomain`, `alterx`, and custom resolvers to uncover subdomains and verify them efficiently.

---

## Features

- **DNS Brute Force**: Uses a static wordlist to brute-force subdomains quickly.
- **Dynamic Discovery**: Automatically alters and verifies subdomains using `alterx` and `ksubdomain`.
- **Custom Resolvers**: Supports common DNS resolvers and allows active resolver selection.
- **Wordlist Management**: Automatically downloads and ensures the presence of a default wordlist.
- **Result Merging**: Combines multiple subdomain lists and removes duplicates.

---

## Requirements

- Python 3.7+
- [ksubdomain](https://github.com/knownsec/ksubdomain) installed and accessible in your PATH.
- [alterx](https://github.com/projectdiscovery/alterx) installed and accessible in your PATH.
- `wget` for downloading the default wordlist.
- Optional: A resolved subdomain file from tools like `subfinder`.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/dns-brute-dynamic-discovery.git
   cd dns-brute-dynamic-discovery
   ```

2. Install Python dependencies (if any are added in the future):
   ```bash
   pip install -r requirements.txt
   ```

3. Install `ksubdomain`:
   ```bash
   git clone https://github.com/knownsec/ksubdomain
   cd ksubdomain
   go build
   cp ./ksubdomain /usr/local/bin/
   ```

4. Install `alterx`:
   ```bash
   go install -v github.com/projectdiscovery/alterx/cmd/alterx@latest
   ```

5. Ensure `wget` is installed for downloading the default wordlist:
   ```bash
   sudo apt install wget
   ```

---

## Usage

Run the tool with the following command:

```bash
python dns_brute_dynamic.py -d <domain> -r <resolved_file> [OPTIONS]
```

### Arguments

| Option            | Description                                                                                     | Default                       |
|-------------------|-------------------------------------------------------------------------------------------------|-------------------------------|
| `-d, --domain`    | **Required.** Target domain to brute-force.                                                     | N/A                           |
| `-r, --resolved`  | **Required.** Resolved subdomains file (from tools like `subfinder`).                           | N/A                           |
| `-w, --wordlist`  | Custom wordlist file for brute-forcing subdomains.                                              | Downloaded default wordlist.  |
| `-o, --output`    | Output file for brute-force results.                                                            | `result.dnsbrute`             |
| `-f, --final`     | Final output file for dynamically verified results.                                             | `result.dynamic`              |

---

### Examples

1. **Brute force a domain with the default wordlist**:
   ```bash
   python dns_brute_dynamic.py -d example.com -r resolved_subdomains.txt
   ```

2. **Use a custom wordlist**:
   ```bash
   python dns_brute_dynamic.py -d example.com -r resolved_subdomains.txt -w custom_wordlist.txt
   ```

3. **Specify custom output files**:
   ```bash
   python dns_brute_dynamic.py -d example.com -r resolved_subdomains.txt -o brute_output.txt -f final_output.txt
   ```

---

## How It Works

1. **Wordlist Management**:
   - Ensures the presence of a static wordlist. If not provided, downloads the default wordlist from [Assetnote](https://wordlists-cdn.assetnote.io/data/manual/2m-subdomains.txt).

2. **DNS Resolver Selection**:
   - Checks active DNS resolvers from a predefined list (e.g., Cloudflare, Google).
   - Creates a default resolver file if no active resolvers are available.

3. **DNS Brute Force**:
   - Uses `ksubdomain enum` to brute-force subdomains based on the static wordlist.

4. **Result Merging**:
   - Merges the brute-forced results with the resolved subdomains file, ensuring no duplicates.

5. **Dynamic Discovery**:
   - Uses `alterx` to alter subdomains dynamically.
   - Verifies altered subdomains with `ksubdomain verify` using active resolvers.

---

## Output

1. **Brute-Force Results**:
   - Saved in the file specified by `-o` (default: `result.dnsbrute`).

2. **Final Verified Results**:
   - Saved in the file specified by `-f` (default: `result.dynamic`).

3. **Resolvers File**:
   - Active resolvers saved to `resolvers.txt` (temporary).

---

## Troubleshooting

- Ensure `ksubdomain` and `alterx` are installed and accessible in your system's PATH.
- If no active resolvers are found, the tool will fall back to the predefined resolver list.

---

## Disclaimer

This tool is intended for authorized use only. Ensure you have permission to perform DNS brute-forcing and dynamic discovery on the target domain.

---

## License

This project is licensed under the [MIT License](LICENSE).

---


