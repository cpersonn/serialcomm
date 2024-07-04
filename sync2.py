import sys
import threading
from mgapi import Port
import tkinter as tk
from tkinter import filedialog, messagebox

class CommunicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sync Communication Interface")
        self.create_widgets()
        self.running = False

    def create_widgets(self):
        tk.Label(self.root, text="Port 1:").grid(row=0, column=0, padx=5, pady=5)
        self.port1_entry = tk.Entry(self.root)
        self.port1_entry.grid(row=0, column=1, padx=5, pady=5)
        self.port1_entry.insert(0, "MGMP1P1")

        tk.Label(self.root, text="Input File 1:").grid(row=1, column=0, padx=5, pady=5)
        self.input_file1_entry = tk.Entry(self.root)
        self.input_file1_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=lambda: self.browse_file(self.input_file1_entry)).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(self.root, text="Output File 1:").grid(row=2, column=0, padx=5, pady=5)
        self.output_file1_entry = tk.Entry(self.root)
        self.output_file1_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=lambda: self.browse_file(self.output_file1_entry)).grid(row=2, column=2, padx=5, pady=5)

        tk.Label(self.root, text="Port 2:").grid(row=3, column=0, padx=5, pady=5)
        self.port2_entry = tk.Entry(self.root)
        self.port2_entry.grid(row=3, column=1, padx=5, pady=5)
        self.port2_entry.insert(0, "MGMP1P2")

        tk.Label(self.root, text="Input File 2:").grid(row=4, column=0, padx=5, pady=5)
        self.input_file2_entry = tk.Entry(self.root)
        self.input_file2_entry.grid(row=4, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=lambda: self.browse_file(self.input_file2_entry)).grid(row=4, column=2, padx=5, pady=5)

        tk.Label(self.root, text="Output File 2:").grid(row=5, column=0, padx=5, pady=5)
        self.output_file2_entry = tk.Entry(self.root)
        self.output_file2_entry.grid(row=5, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=lambda: self.browse_file(self.output_file2_entry)).grid(row=5, column=2, padx=5, pady=5)

        tk.Label(self.root, text="Data Rate:").grid(row=6, column=0, padx=5, pady=5)
        self.data_rate_entry = tk.Entry(self.root)
        self.data_rate_entry.grid(row=6, column=1, padx=5, pady=5)
        self.data_rate_entry.insert(0, '9600')


        tk.Button(self.root, text="Start", command=self.on_start).grid(row=10, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Stop", command=self.on_stop).grid(row=10, column=2, padx=5, pady=5)
        tk.Button(self.root, text="Quit", command=self.root.quit).grid(row=10, column=3, padx=5, pady=5)

    def browse_file(self, entry):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            entry.delete(0, tk.END)
            entry.insert(0, filename)

    def on_start(self):
        port1 = self.port1_entry.get()
        port2 = self.port2_entry.get()
        input_file1 = self.input_file1_entry.get()
        output_file1 = self.output_file1_entry.get()
        input_file2 = self.input_file2_entry.get()
        output_file2 = self.output_file2_entry.get()
        data_rate = int(self.data_rate_entry.get())


        if not port1 or not port2 or not input_file1 or not output_file1 or not input_file2 or not output_file2:
            messagebox.showerror("Error", "All fields must be filled")
            return

        self.running = True
        self.thread = threading.Thread(target=self.start_communication, args=(port1, port2, input_file1, output_file1, input_file2, output_file2, data_rate))
        self.thread.start()

    def on_stop(self):
        self.running = False

    def start_communication(self, port1_name, port2_name, input_file1, output_file1, input_file2, output_file2, data_rate):
        port1 = open_port(port1_name)
        port2 = open_port(port2_name)

        configure_port(port1, data_rate)
        configure_port(port2, data_rate)

        print('Press Ctrl-C to stop the program')

        port1.enable_receiver()
        port2.enable_receiver()

        receive_thread1 = threading.Thread(target=receive_thread_func, args=(port1, port1_name, output_file1, lambda: self.running))
        receive_thread2 = threading.Thread(target=receive_thread_func, args=(port2, port2_name, output_file2, lambda: self.running))
        receive_thread1.start()
        receive_thread2.start()

        with open(input_file1, 'r') as f1, open(input_file2, 'r') as f2:
            hex_data1 = f1.read().strip()
            buf1 = bytearray.fromhex(hex_data1)

            hex_data2 = f2.read().strip()
            buf2 = bytearray.fromhex(hex_data2)

        try:
            i = 1
            while self.running:
                print(f'>>> {port1_name} ' + '{:0>9d}'.format(i) + ' send ' + str(len(buf1)) + ' bytes\n', end='')
                port1.write(buf1)
                port1.flush()

                print(f'>>> {port2_name} ' + '{:0>9d}'.format(i) + ' send ' + str(len(buf2)) + ' bytes\n', end='')
                port2.write(buf2)
                port2.flush()
                i += 1
        except KeyboardInterrupt:
            print('Ctrl-C pressed')
        finally:
            port1.close()
            port2.close()

def receive_thread_func(port, port_name, output_file, running_check):
    i = 1
    with open(output_file, 'w') as f:
        while running_check():
            buf = port.read(100)
            if not buf:
                break
            hex_data = buf.hex()
            print(f'<<< {port_name} ' + '{:0>9d}'.format(i) + ' received ' + str(len(buf)) + ' bytes: ' + hex_data)
            f.write(hex_data + '\n')
            i += 1
        f.close()

def open_port(port_name):
    port = Port(port_name)
    print(f'Port {port_name} opening...')
    try:
        port.open()
    except FileNotFoundError:
        print(f'Port {port_name} not found')
        sys.exit()
    except PermissionError:
        print(f'Access denied or {port_name} in use')
        sys.exit()
    except OSError:
        print(f'Open error on {port_name}')
        sys.exit()
    return port

def configure_port(port, data_rate):
    settings = Port.Settings()
    settings.protocol = Port.HDLC
    settings.encoding = Port.NRZ
    settings.crc = Port.CRC16
    settings.transmit_clock = Port.TXC_INPUT
    settings.receive_clock = Port.RXC_INPUT
    settings.internal_clock_rate = data_rate
    port.transmit_idle_pattern = 0xE7
    port.interface = Port.RS232
    port.apply_settings(settings)


if __name__ == "__main__":
    root = tk.Tk()
    app = CommunicationApp(root)
    root.mainloop()
