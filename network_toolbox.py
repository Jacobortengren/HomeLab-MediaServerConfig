import os
import socket
import psutil
from datetime import datetime

LOG_FILE = "toolbox_log.txt"

def log_result(text):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")

def show_ip_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    output = []
    output.append("\n=== IP-information ===")
    output.append(f"Värdnamn: {hostname}")
    output.append(f"IP-adress: {ip_address}")

    net_if_addrs = psutil.net_if_addrs()
    for interface, addrs in net_if_addrs.items():
        output.append(f"\nInterface: {interface}")
        for addr in addrs:
            if addr.family == socket.AF_INET:
                output.append(f"  IPv4: {addr.address}")
                output.append(f"  Nätmask: {addr.netmask}")
                output.append(f"  Broadcast: {addr.broadcast}")

    result = "\n".join(output)
    print(result)
    log_result(result)

def ping_host():
    host = input("Ange IP eller domän att pinga: ")
    param = "-n 4" if os.name == "nt" else "-c 4"
    response = os.system(f"ping {param} {host}")

    if response == 0:
        result = f"{host} är nåbar ✅"
    else:
        result = f"{host} svarar inte ❌"

    print(result)
    log_result(result)

def port_scan():
    target = input("Ange IP-adress att scanna: ")
    ports = [22, 80, 443, 3389]

    output = []
    output.append(f"\n=== Portscanning på {target} ===")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            output.append(f"Port {port} är öppen ✅")
        else:
            output.append(f"Port {port} är stängd ❌")
        sock.close()

    result = "\n".join(output)
    print(result)
    log_result(result)

def main():
    while True:
        print("\n--- Nätverkstekniker Toolbox ---")
        print("1. Visa IP-information")
        print("2. Ping-test")
        print("3. Portscanner (22, 80, 443, 3389)")
        print("4. Avsluta")

        choice = input("Välj ett alternativ: ")

        if choice == "1":
            show_ip_info()
        elif choice == "2":
            ping_host()
        elif choice == "3":
            port_scan()
        elif choice == "4":
            print("Avslutar programmet...")
            break
        else:
            print("Ogiltigt val, försök igen!")

if __name__ == "__main__":
    main()
