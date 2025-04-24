"""Weigh Bridge Module"""
import tkinter as tk
import socket
import threading
import time
import config

class Scale:
    """This class represents a scale"""
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = int(port)
        self.stop = False
        self.weight = 0
        self.status = 1

    def connection(self):
        """Handles the connection to the scale"""
        while not self.stop:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.host, self.port))
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    self.status = 0
                    while not self.stop:
                        data = s.recv(8096)
                        time.sleep(0.2)
                        data = data.decode()
                        data = data[4:16]
                        self.weight = float(data.split()[0])
            except (socket.timeout, ConnectionError, OSError, IndexError):
                self.weight = 0
                self.status = 1
                print(f"Failed to connect to {self.host}:{self.port}. Retrying...")
                # time.sleep(5)
        if self.stop:
            print(f"connection {self.host}: got STOP, exiting...")

class App:
    """APP GUI Class"""
    def __init__(self) -> None:
        self.weights = []
        self.root = tk.Tk()
        self.root.resizable(0, 0)
        # root.overrideredirect(1)
        self.root.attributes("-toolwindow", 1,"-topmost", 1)
        self.root.title("🚛 Weigh bridge scale")
        self.root.geometry(config.windowsposition)

        self.frame = tk.Frame(self.root, width=500, height=100, relief="solid")
        self.frame.pack(fill='both', expand=True)

        self.reading = tk.Label(self.frame, text="loading", font=("Helvetica", 20))
        self.reading.pack(side="left", padx=10,pady=10)

        self.scales = tk.Label(self.frame, text="⚖️ 0", font=("Helvetica", 15))
        self.scales.pack(side="right", padx=10)

        self.start()

    def update(self):
        """Updates values in GUI"""
        neterror = False
        total = 0
        for scale in self.weights:
            if not scale.status > 0:
                total += scale.weight
            else:
                neterror = True
                netmsg = f"{scale.host} lost"
                break
        if neterror:
            self.reading.configure(text=netmsg)
        else:
            self.reading.configure(text=total/1000)
            self.scales.configure(text=f"⚖️ {len(self.weights)}")
            print(f"t: {int(total) :<8} s: {len(self.weights) :>1}")
        self.root.after(100, self.update)

    def start(self):
        """Creates connection threads for each scale"""
        for scale in config.scales.items():
            self.weights += [Scale(scale[1]['ip'],scale[1]['port'])]
        for weight in self.weights:
            threading.Thread(target=weight.connection).start()
        self.root.after(100, self.update)
        self.root.mainloop()

if __name__ == '__main__':
    # Create tinker app
    app = App()
    # Stop Connection threads
    for connection in app.weights:
        connection.stop = True
