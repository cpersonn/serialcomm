import tkinter as tk
from tkinter import filedialog
import threading
from mgapi import Port  # Senkron haberleşme için gerekli kütüphaneyi ekleyin

class CommunicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Synchronous Communication App")

        # Port 1 widgets
        self.port1_label = tk.Label(root, text="Port 1:")
        self.port1_label.grid(row=0, column=0, padx=5, pady=5)
        self.port1_entry = tk.Entry(root)
        self.port1_entry.grid(row=0, column=1, padx=5, pady=5)
        self.port1_button = tk.Button(root, text="Browse", command=lambda: self.browse_file(self.port1_entry))
        self.port1_button.grid(row=0, column=2, padx=5, pady=5)
        self.port1_entry.insert(0, "MGMP1P1")

        # Port 2 widgets
        self.port2_label = tk.Label(root, text="Port 2:")
        self.port2_label.grid(row=1, column=0, padx=5, pady=5)
        self.port2_entry = tk.Entry(root)
        self.port2_entry.grid(row=1, column=1, padx=5, pady=5)
        self.port2_button = tk.Button(root, text="Browse", command=lambda: self.browse_file(self.port2_entry))
        self.port2_button.grid(row=1, column=2, padx=5, pady=5)
        self.port2_entry.insert(0, "MGMP1P2")

        # Input files widgets
        self.input_file1_label = tk.Label(root, text="Input File 1:")
        self.input_file1_label.grid(row=2, column=0, padx=5, pady=5)
        self.input_file1_entry = tk.Entry(root)
        self.input_file1_entry.grid(row=2, column=1, padx=5, pady=5)
        self.input_file1_button = tk.Button(root, text="Browse", command=lambda: self.browse_file(self.input_file1_entry))
        self.input_file1_button.grid(row=2, column=2, padx=5, pady=5)

        self.input_file2_label = tk.Label(root, text="Input File 2:")
        self.input_file2_label.grid(row=3, column=0, padx=5, pady=5)
        self.input_file2_entry = tk.Entry(root)
        self.input_file2_entry.grid(row=3, column=1, padx=5, pady=5)
        self.input_file2_button = tk.Button(root, text="Browse", command=lambda: self.browse_file(self.input_file2_entry))
        self.input_file2_button.grid(row=3, column=2, padx=5, pady=5)

        # Output files widgets
        self.output_file1_label = tk.Label(root, text="Output File 1:")
        self.output_file1_label.grid(row=4, column=0, padx=5, pady=5)
        self.output_file1_entry = tk.Entry(root)
        self.output_file1_entry.grid(row=4, column=1, padx=5, pady=5)
        self.output_file1_button = tk.Button(root, text="Browse", command=lambda: self.browse_file(self.output_file1_entry))
        self.output_file1_button.grid(row=4, column=2, padx=5, pady=5)

        self.output_file2_label = tk.Label(root, text="Output File 2:")
        self.output_file2_label.grid(row=5, column=0, padx=5, pady=5)
        self.output_file2_entry = tk.Entry(root)
        self.output_file2_entry.grid(row=5, column=1, padx=5, pady=5)
        self.output_file2_button = tk.Button(root, text="Browse", command=lambda: self.browse_file(self.output_file2_entry))
        self.output_file2_button.grid(row=5, column=2, padx=5, pady=5)

        # Data rate widget
        self.data_rate_label = tk.Label(root, text="Data Rate:")
        self.data_rate_label.grid(row=6, column=0, padx=5, pady=5)
        self.data_rate_entry = tk.Entry(root)
        self.data_rate_entry.grid(row=6, column=1, padx=5, pady=5)
        self.data_rate_entry.insert(0, "9600")


        # Start and stop buttons
        self.start_button = tk.Button(root, text="Start Synchronous Communication", command=self.on_start_synchronous)
        self.start_button.grid(row=8, column=1, padx=5, pady=5)
        self.stop_button = tk.Button(root, text="Stop", command=self.on_stop)
        self.stop_button.grid(row=8, column=2, padx=5, pady=5)
        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.grid(row=8, column=3, padx=5, pady=5)

        # Running status
        self.running = False
        self.ports = []

    def browse_file(self, entry):
        file_path = filedialog.askopenfilename()
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def on_start_synchronous(self):
        port1_name = self.port1_entry.get()
        port2_name = self.port2_entry.get()
        input_file1 = self.input_file1_entry.get()
        output_file1 = self.output_file1_entry.get()
        input_file2 = self.input_file2_entry.get()
        output_file2 = self.output_file2_entry.get()
        data_rate = int(self.data_rate_entry.get())


        self.ports = [Port(port1_name), Port(port2_name)]

        for port in self.ports:
            settings = Port.Settings()
            settings.protocol = Port.HDLC
            settings.encoding = Port.NRZ
            settings.crc = Port.OFF
            settings.transmit_clock = Port.TXC_INPUT
            settings.receive_clock = Port.TXC_INPUT
            settings.internal_clock_rate = data_rate
            port.apply_settings(settings)
            port.transmit_idle_pattern = 0xFF
            port.interface = Port.RS232



        self.running = True
        # galiba receiver yapmıyor enable receiver a bak

        threading.Thread(target=self.send_thread_func, args=(self.ports[0], input_file1)).start()
        threading.Thread(target=self.receive_thread_func, args=(self.ports[0], output_file1)).start()
        threading.Thread(target=self.send_thread_func, args=(self.ports[1], input_file2)).start()
        threading.Thread(target=self.receive_thread_func, args=(self.ports[1], output_file2)).start()

    def on_stop(self):
        self.running = False
        for port in self.ports:
            port.close()

    def send_thread_func(self, port, input_file):
        with open(input_file, 'rb') as f:
            i = 1
            while self.running:
                buf = f.read(100)
                if not buf:
                    break
                buf = bytearray(buf)  # Yazılabilir bir buffer yap
                port.write(buf)
                port.flush()
                print(f"[{port.name}] >>> Sent {len(buf)} bytes")
                i += 1

    def receive_thread_func(self, port, output_file):
        with open(output_file, 'wb') as f:
            while self.running:
                buf = bytearray(100)
                bytes_received = port.read(buf)
                if bytes_received:
                    f.write(buf[:bytes_received])
                    f.flush()
                    print(f"[{port.name}] <<< Received {bytes_received} bytes")

if __name__ == "__main__":
    root = tk.Tk()
    app = CommunicationApp(root)
    root.mainloop()
