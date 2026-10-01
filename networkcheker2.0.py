#!/usr/bin/env python3

import socket
import subprocess
import platform
from datetime import datetime


def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"


def check_internet():
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=3)
        return True
    except OSError:
        return False


def check_dns():
    try:
        socket.gethostbyname("google.com")
        return True
    except socket.gaierror:
        return False


def get_hostname():
    return socket.gethostname()


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "Unavailable"


def main():
    print("=" * 45)
    print("        NETWORK DIAGNOSTIC TOOL")
    print("=" * 45)

    print(f"Time:       {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"OS:         {platform.system()} {platform.release()}")
    print(f"Hostname:   {get_hostname()}")
    print(f"Local IP:   {get_local_ip()}")

    print("\nNetwork status:")

    internet = check_internet()
    dns = check_dns()

    print(f"[{'OK' if internet else 'FAIL'}] Internet connection")
    print(f"[{'OK' if dns else 'FAIL'}] DNS resolution")

    if platform.system() == "Linux":
        print("\nNetwork interfaces:")
        print(run_command(["ip", "-br", "addr"]))

        print("\nRouting table:")
        print(run_command(["ip", "route"]))

    print("\n" + "=" * 45)


if __name__ == "__main__":
    main()
