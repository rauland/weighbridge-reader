"""Weigh Bridge Module"""
import tkinter as tk
import socket
import threading
import time
import config

class Scale:
    """This represents a scale"""
    def __init__(self, name, host, port) -> None:
        self.name = name
        self.host = host
        self.port = int(port)
        self.stop = False
        self.weight = 0
        self.status = 1
        self.statusmsg = "Connecting..."

    def connection(self):
        """Handles the connection to the physical scale"""
        while not self.stop:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.host, self.port))
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    self.status = 0
                    self.statusmsg = "Connected"
                    while not self.stop:
                        data = s.recv(8096)
                        time.sleep(0.2)
                        data = data.decode()
                        data = data[4:16]
                        self.weight = float(data.split()[0])
            except (socket.timeout, ConnectionError, OSError, IndexError):
                self.weight = 0
                self.status = 1
                self.statusmsg = "Connection Error"
                print(f"Failed to connect to {self.name} on {self.host}:{self.port}. Retrying...")
        if self.stop:
            print(f"{self.name} connection {self.host}: got STOP, exit thread.")

class App:
    """App GUI"""
    def __init__(self) -> None:
        self.weights = []
        self.root = tk.Tk()
        self.root.resizable(0, 0)
        self.root.attributes("-toolwindow", 1,"-topmost", 1)
        self.root.title("🚛 Weigh bridge scale")
        self.root.geometry(config.windowsposition)
        self.frame = tk.Frame(self.root, width=500, height=100, relief="solid")
        self.frame.pack(fill='both', expand=True)
        self.reading = tk.Label(self.frame, text="loading", font=("Helvetica", 20), justify="left", anchor="w")
        self.reading.pack(side="left", padx=10,pady=5)
        self.scales = tk.Label(self.frame, text="⚖️ 0", font=("Helvetica", 15))
        self.scales.pack(side="right", padx=10)
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.start()

    def update(self):
        """Updates values in App's GUI"""
        for scale in self.weights:
            if scale.status > 0:
                netmsg = f"{scale.name}\n{scale.host}:{scale.port}\n{scale.statusmsg}"
                self.reading.configure(text=netmsg, font=("Helvetica", 10))
                self.root.after(100, self.update)
                return
        total = sum(scale.weight for scale in self.weights)
        self.reading.configure(text=total/1000, font=("Helvetica", 20))
        self.scales.configure(text=f"⚖️ {len(self.weights)}")
        print(f"t: {int(total) :<8} s: {len(self.weights) :>1}")
        self.root.after(100, self.update)

    def start(self):
        """Creates connection threads for each scale"""
        for scale in config.scales.items():
            self.weights += [Scale(scale[0],scale[1]['host'],scale[1]['port'])]
        for weight in self.weights:
            threading.Thread(target=weight.connection).start()
        self.root.after(100, self.update)
        self.root.mainloop()

    def stop(self):
        """Stops all connection threads and stops App"""
        print("Shutting down...")
        for connection in self.weights:
            connection.stop = True
        self.root.destroy()

if __name__ == '__main__':
    app = App()
