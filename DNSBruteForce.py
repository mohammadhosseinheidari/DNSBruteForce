import os
import subprocess
import argparse
import socket

DEFAULT_WORDLIST_URL = "https://wordlists-cdn.assetnote.io/data/manual/2m-subdomains.txt"
DEFAULT_WORDLIST_FILE = "dnsbrute-static-wordlist.txt"

COMMON_RESOLVERS = [
    "1.1.1.1", "1.0.0.1",         # Cloudflare
    "8.8.8.8", "8.8.4.4",         # Google
    "9.9.9.9",                    # Quad9
    "208.67.222.222", "208.67.220.220",  # OpenDNS
    "94.140.14.14",               # AdGuard
]

class ResolverSelector:
    @staticmethod
    def check_alive(ip, port=53, timeout=1.5):
        try:
            socket.setdefaulttimeout(timeout)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b'', (ip, port))
            sock.close()
            return True
        except:
            return False

    @classmethod
    def get_active(cls):
        print("[*] Checking available DNS resolvers...")
        active = [ip for ip in COMMON_RESOLVERS if cls.check_alive(ip)]
        for ip in active:
            print(f"    [+] Active: {ip}")
        return active

    @staticmethod
    def create_default_resolvers_file():
        # اگر هیچ DNS فعال پیدا نشد، فایل پیش‌فرض را ایجاد می‌کنیم
        resolvers_file = "resolvers.txt"
        with open(resolvers_file, "w") as f:
            for resolver in COMMON_RESOLVERS:
                f.write(resolver + "\n")
        print(f"[*] Default DNS resolvers saved to {resolvers_file}")
        return resolvers_file

class WordlistManager:
    @staticmethod
    def ensure_wordlist(path=None):
        if path and os.path.exists(path):
            return path
        if not os.path.exists(DEFAULT_WORDLIST_FILE):
            print("[*] Downloading default static wordlist...")
            subprocess.run(["wget", DEFAULT_WORDLIST_URL, "-O", DEFAULT_WORDLIST_FILE], check=True)
        return DEFAULT_WORDLIST_FILE

class DNSBrute:
    def __init__(self, domain, wordlist, output):
        self.domain = domain
        self.wordlist = wordlist
        self.output = output

    def run(self):
        print(f"[*] Starting DNS brute-force on {self.domain} using wordlist {self.wordlist}")
        cmd = [
            "ksubdomain", "enum",  # اصلاح به "enum" برای عملیات brute-force
            "-d", self.domain,
            "-f", self.wordlist,
            "-o", self.output
        ]
        subprocess.run(cmd, check=True)
        print(f"[+] Brute-force results saved to: {self.output}")

class ResultMerger:
    @staticmethod
    def merge(files, output):
        print("[*] Merging subdomain results...")
        with open(output, "w") as out:
            subprocess.run(f"cat {' '.join(files)} | anew", shell=True, stdout=out)
        print(f"[+] Merged output saved to: {output}")

class DynamicDiscovery:
    def __init__(self, input_file, output_file, band="10m", timeout=3, retry=-1, silent=True, resolvers=None):
        self.input_file = input_file
        self.output_file = output_file
        self.band = band
        self.timeout = timeout
        self.retry = retry
        self.silent = silent
        self.resolvers = resolvers

    def run(self):
        print("[*] Running alterx and ksubdomain verify...")
        altered_file = "altered.tmp"
        try:
            with open(altered_file, "w") as out:
                subprocess.run(f"cat {self.input_file} | alterx -silent", shell=True, stdout=out)
        except FileNotFoundError:
            print("[!] alterx not found! Make sure it's installed and in your PATH.")
            return

        # ذخیره آدرس‌های DNS در یک فایل
        resolvers_file = "resolvers.txt"
        with open(resolvers_file, "w") as f:
            for resolver in self.resolvers:
                f.write(resolver + "\n")

        cmd = [
            "ksubdomain", "verify",
            "-f", altered_file,
            "-o", self.output_file,
            "--band", self.band,
            "--timeout", str(self.timeout),
            "--retry", str(self.retry),
            "--resolvers", resolvers_file
        ]
        if self.silent:
            cmd.append("--silent")

        subprocess.run(cmd, check=True)
        os.remove(altered_file)
        os.remove(resolvers_file)  # حذف فایل resolvers
        print(f"[+] Final dynamic verification results saved to: {self.output_file}")

def main():
    parser = argparse.ArgumentParser(description="🚀 Fast DNS Brute Force + Dynamic Discovery using ksubdomain")

    parser.add_argument("-d", "--domain", required=True, help="Target domain")
    parser.add_argument("-r", "--resolved", required=True, help="Resolved subdomains file (from tools like subfinder)")
    parser.add_argument("-w", "--wordlist", help="Custom wordlist file for static brute-force")

    parser.add_argument("-o", "--output", default="result.dnsbrute", help="Output file for brute results")
    parser.add_argument("-f", "--final", default="result.dynamic", help="Final output file after dynamic discovery")

    args = parser.parse_args()

    wordlist = WordlistManager.ensure_wordlist(args.wordlist)
    resolvers = ResolverSelector.get_active()

    if not resolvers:  # اگر DNS فعال پیدا نشد، از DNSهای پیش‌فرض استفاده کن
        resolvers_file = ResolverSelector.create_default_resolvers_file()
        resolvers = [line.strip() for line in open(resolvers_file).readlines()]

    DNSBrute(args.domain, wordlist, args.output).run()
    ResultMerger.merge([args.output, args.resolved], "resolved.txt")
    DynamicDiscovery("resolved.txt", args.final, resolvers=resolvers).run()

if __name__ == "__main__":
    main()
