import sys
import threading
from mgapi import Port
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class CommunicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sync Communication Interface")
        self.create_widgets()
        self.running_send_port1 = False
        self.running_send_port2 = False
        self.running_receive_port1 = False
        self.running_receive_port2 = False
        self.port1 = None
        self.port2 = None
        self.sent_bits_port1 = 0
        self.sent_bits_port2 = 0
        self.received_bits_port1 = 0
        self.received_bits_port2 = 0

    def create_widgets(self):

        # Port 1

        tk.Label(self.root, text="Port 1:").grid(row=0, column=0, padx=5, pady=5)
        self.port1_entry = tk.Entry(self.root)
        self.port1_entry.grid(row=0, column=1, padx=5, pady=5)
        self.port1_entry.insert(0, "MGMP1P1")

        tk.Label(self.root, text="Input File 1:").grid(row=1, column=0, padx=5, pady=5)
        self.input_file1_entry = tk.Entry(self.root)
        self.input_file1_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=lambda: self.browse_file(self.input_file1_entry)).grid(row=1,
                                                                                                           column=2,
                                                                                                           padx=5,
                                                                                                           pady=5)

        tk.Label(self.root, text="Output File 1:").grid(row=2, column=0, padx=5, pady=5)
        self.output_file1_entry = tk.Entry(self.root)
        self.output_file1_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=lambda: self.browse_file(self.output_file1_entry)).grid(row=2,
                                                                                                            column=2,
                                                                                                            padx=5,
                                                                                                            pady=5)

        tk.Label(self.root, text="Port 1 Protocol:").grid(row=3, column=0, padx=5, pady=5)
        self.port1_protocol_var = tk.StringVar()
        self.port1_protocol_combobox = ttk.Combobox(self.root, textvariable=self.port1_protocol_var, state="readonly")
        self.port1_protocol_combobox['values'] = ("HDLC", "RAW", "BISYNC", "ASYNC")
        self.port1_protocol_combobox.grid(row=3, column=1, padx=5, pady=5)
        self.port1_protocol_combobox.current(0)

        tk.Label(self.root, text="Port 1 Data Rate:").grid(row=4, column=0, padx=5, pady=5)
        self.port1_data_rate_entry = tk.Entry(self.root)
        self.port1_data_rate_entry.grid(row=4, column=1, padx=5, pady=5)
        self.port1_data_rate_entry.insert(0, '9600')

        tk.Label(self.root, text="Port 1 Transmit Clock:").grid(row=5, column=0, padx=5, pady=5)
        self.port1_transmit_clock_var = tk.StringVar()
        self.port1_transmit_clock_combobox = ttk.Combobox(self.root, textvariable=self.port1_transmit_clock_var,
                                                          state="readonly")
        self.port1_transmit_clock_combobox['values'] = ("TXC_INPUT", "RXC_INPUT", "INTERNAL")
        self.port1_transmit_clock_combobox.grid(row=5, column=1, padx=5, pady=5)
        self.port1_transmit_clock_combobox.current(0)

        tk.Label(self.root, text="Port 1 Receive Clock:").grid(row=6, column=0, padx=5, pady=5)
        self.port1_receive_clock_var = tk.StringVar()
        self.port1_receive_clock_combobox = ttk.Combobox(self.root, textvariable=self.port1_receive_clock_var,
                                                         state="readonly")
        self.port1_receive_clock_combobox['values'] = ("TXC_INPUT", "RXC_INPUT", "INTERNAL")
        self.port1_receive_clock_combobox.grid(row=6, column=1, padx=5, pady=5)
        self.port1_receive_clock_combobox.current(0)

        # Port 2

        tk.Label(self.root, text="Port 2:").grid(row=7, column=0, padx=5, pady=5)
        self.port2_entry = tk.Entry(self.root)
        self.port2_entry.grid(row=7, column=1, padx=5, pady=5)
        self.port2_entry.insert(0, "MGMP1P2")

        tk.Label(self.root, text="Input File 2:").grid(row=8, column=0, padx=5, pady=5)
        self.input_file2_entry = tk.Entry(self.root)
        self.input_file2_entry.grid(row=8, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=lambda: self.browse_file(self.input_file2_entry)).grid(row=8,
                                                                                                           column=2,
                                                                                                           padx=5,
                                                                                                           pady=5)

        tk.Label(self.root, text="Output File 2:").grid(row=9, column=0, padx=5, pady=5)
        self.output_file2_entry = tk.Entry(self.root)
        self.output_file2_entry.grid(row=9, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=lambda: self.browse_file(self.output_file2_entry)).grid(row=9,
                                                                                                            column=2,
                                                                                                            padx=5,
                                                                                                            pady=5)

        tk.Label(self.root, text="Port 2 Protocol:").grid(row=10, column=0, padx=5, pady=5)
        self.port2_protocol_var = tk.StringVar()
        self.port2_protocol_combobox = ttk.Combobox(self.root, textvariable=self.port2_protocol_var, state="readonly")
        self.port2_protocol_combobox['values'] = ("HDLC", "RAW", "BISYNC", "ASYNC")
        self.port2_protocol_combobox.grid(row=10, column=1, padx=5, pady=5)
        self.port2_protocol_combobox.current(0)

        tk.Label(self.root, text="Port 2 Data Rate:").grid(row=11, column=0, padx=5, pady=5)
        self.port2_data_rate_entry = tk.Entry(self.root)
        self.port2_data_rate_entry.grid(row=11, column=1, padx=5, pady=5)
        self.port2_data_rate_entry.insert(0, '9600')

        tk.Label(self.root, text="Port 2 Transmit Clock:").grid(row=12, column=0, padx=5, pady=5)
        self.port2_transmit_clock_var = tk.StringVar()
        self.port2_transmit_clock_combobox = ttk.Combobox(self.root, textvariable=self.port2_transmit_clock_var,
                                                          state="readonly")
        self.port2_transmit_clock_combobox['values'] = ("TXC_INPUT", "RXC_INPUT", "INTERNAL")
        self.port2_transmit_clock_combobox.grid(row=12, column=1, padx=5, pady=5)
        self.port2_transmit_clock_combobox.current(0)

        tk.Label(self.root, text="Port 2 Receive Clock:").grid(row=13, column=0, padx=5, pady=5)
        self.port2_receive_clock_var = tk.StringVar()
        self.port2_receive_clock_combobox = ttk.Combobox(self.root, textvariable=self.port2_receive_clock_var,
                                                         state="readonly")
        self.port2_receive_clock_combobox['values'] = ("TXC_INPUT", "RXC_INPUT", "INTERNAL")
        self.port2_receive_clock_combobox.grid(row=13, column=1, padx=5, pady=5)
        self.port2_receive_clock_combobox.current(0)

        tk.Button(self.root, text="Configure Ports", command=self.configure_ports).grid(row=14, column=0, padx=5,
                                                                                        pady=5)

        self.port1_send_button = tk.Button(self.root, text="Port 1 Send", command=self.toggle_send_port1)
        self.port1_send_button.grid(row=15, column=0, padx=5, pady=5)

        self.port2_send_button = tk.Button(self.root, text="Port 2 Send", command=self.toggle_send_port2)
        self.port2_send_button.grid(row=15, column=1, padx=5, pady=5)

        self.port1_receive_button = tk.Button(self.root, text="Port 1 Receive", command=self.toggle_receive_port1)
        self.port1_receive_button.grid(row=16, column=0, padx=5, pady=5)

        self.port2_receive_button = tk.Button(self.root, text="Port 2 Receive", command=self.toggle_receive_port2)
        self.port2_receive_button.grid(row=16, column=1, padx=5, pady=5)

        self.stop_button = tk.Button(self.root, text="Stop All", command=self.stop_all)
        self.stop_button.grid(row=17, column=0, padx=5, pady=5)

        self.results_button = tk.Button(self.root, text="Show Results", command=self.show_results)
        self.results_button.grid(row=17, column=1, padx=5, pady=5)

        self.port1_sent_label = tk.Label(self.root, text="Port 1 Sent Bits: 0")
        self.port1_sent_label.grid(row=18, column=0, padx=5, pady=5)

        self.port1_received_label = tk.Label(self.root, text="Port 1 Received Bits: 0")
        self.port1_received_label.grid(row=19, column=0, padx=5, pady=5)

        self.port2_sent_label = tk.Label(self.root, text="Port 2 Sent Bits: 0")
        self.port2_sent_label.grid(row=18, column=1, padx=5, pady=5)

        self.port2_received_label = tk.Label(self.root, text="Port 2 Received Bits: 0")
        self.port2_received_label.grid(row=19, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Quit", command=self.root.quit).grid(row=20, column=0, padx=5, pady=5)

    def browse_file(self, entry):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            entry.delete(0, tk.END)
            entry.insert(0, filename)

    def configure_ports(self):
        if self.port1:
            self.port1.close()
        if self.port2:
            self.port2.close()

        port1_name = self.port1_entry.get()
        port2_name = self.port2_entry.get()
        port1_data_rate = int(self.port1_data_rate_entry.get())
        port2_data_rate = int(self.port2_data_rate_entry.get())
        port1_transmit_clock = self.port1_transmit_clock_combobox.get()
        port2_transmit_clock = self.port2_transmit_clock_combobox.get()
        port1_receive_clock = self.port1_receive_clock_combobox.get()
        port2_receive_clock = self.port2_receive_clock_combobox.get()
        port1_protocol = self.port1_protocol_combobox.get()
        port2_protocol = self.port2_protocol_combobox.get()

        if not port1_name or not port2_name:
            messagebox.showerror("Error", "Port names must be specified")
            return

        try:
            self.port1 = open_port(port1_name)
            configure_port(self.port1, port1_data_rate, port1_transmit_clock, port1_receive_clock, port1_protocol)
            self.port1.enable_receiver()

            self.port2 = open_port(port2_name)
            configure_port(self.port2, port2_data_rate, port2_transmit_clock, port2_receive_clock, port2_protocol)
            self.port2.enable_receiver()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_send_port1(self):
        if self.running_send_port1:
            self.running_send_port1 = False
            self.port1_send_button.config(text="Port 1 Send", bg="red")
        else:
            self.running_send_port1 = True
            self.port1_send_button.config(text="Port 1 Stop", bg="green")
            threading.Thread(target=self.send_data, args=(
                self.port1, self.port1_entry.get(), self.input_file1_entry.get(),
                lambda: self.running_send_port1, self.port1_sent_label, self.sent_bits_port1)).start()

    def toggle_receive_port1(self):
        if self.running_receive_port1:
            self.running_receive_port1 = False
            self.port1_receive_button.config(text="Port 1 Receive", bg="red")

        else:
            self.running_receive_port1 = True
            self.port1_receive_button.config(text="Port 1 Stop", bg="green")
            threading.Thread(target=self.receive_data, args=(
                self.port1, self.output_file1_entry.get(), lambda: self.running_receive_port1,
                self.port1_received_label, self.received_bits_port1)).start()

    def toggle_send_port2(self):
        if self.running_send_port2:
            self.running_send_port2 = False
            self.port2_send_button.config(text="Port 2 Send", bg="red")
        else:
            self.running_send_port2 = True
            self.port2_send_button.config(text="Port 2 Stop", bg="green")
            threading.Thread(target=self.send_data, args=(
                self.port2, self.port2_entry.get(), self.input_file2_entry.get(),
                lambda: self.running_send_port2, self.port2_sent_label, self.sent_bits_port2)).start()

    def toggle_receive_port2(self):
        if self.running_receive_port2:
            self.running_receive_port2 = False
            self.port2_receive_button.config(text="Port 2 Receive", bg="red")
        else:
            self.running_receive_port2 = True
            self.port2_receive_button.config(text="Port 2 Stop", bg="green")
            threading.Thread(target=self.receive_data, args=(
                self.port2, self.output_file2_entry.get(), lambda: self.running_receive_port2,
                self.port2_received_label, self.received_bits_port2)).start()

    def stop_all(self):
        self.running_send_port1 = False
        self.running_send_port2 = False
        self.running_receive_port1 = False
        self.running_receive_port2 = False


        self.port1_send_button.config(text="Port 1 Send", bg="red")
        self.port1_receive_button.config(text="Port 1 Receive", bg="red")
        self.port2_send_button.config(text="Port 2 Send", bg="red")
        self.port2_receive_button.config(text="Port 2 Receive", bg="red")

    def show_results(self):
        messagebox.showinfo(
            "Results",
            f"Port 1 - Total Sent Bits: {self.sent_bits_port1}, Total Received Bits: {self.received_bits_port1}\n"
            f"Port 2 - Total Sent Bits: {self.sent_bits_port2}, Total Received Bits: {self.received_bits_port2}"
        )

    def send_data(self, port, port_name, input_file, running_check, label, bits_counter):
        try:
            with open(input_file, 'r') as f:
                hex_data = f.read().strip()
                buf = bytearray.fromhex(hex_data)

            i = 1
            while running_check():
                print(f'>>> {port_name} ' + '{:0>9d}'.format(i) + ' send ' + str(len(buf)) + ' bytes\n', end='')
                port.write(buf)
                port.flush()
                bits_counter += len(buf) * 8  # Counting bits
                label.config(text=f"{port_name} Sent Bits: {bits_counter}")
                i += 1
        except Exception as e:
            print(f"Error sending data: {e}")
        #finally:
        #    print(`~)port.close()

    def receive_data(self, port, output_file, running_check, label, bits_counter):
        i = 1
        try:
            with open(output_file, 'w') as f:
                while running_check():
                    buf = port.read(100)
                    if not buf:
                        break
                    hex_data = buf.hex()
                    print(f'<<< {port.name} ' + '{:0>9d}'.format(i) + ' received ' + str(len(buf)) + ' bytes: ' + hex_data)
                    f.write(hex_data + '\n')
                    bits_counter += len(buf) * 8  # Counting bits
                    label.config(text=f"{port.name} Received Bits: {bits_counter}")
                    i += 1
        except Exception as e:
            print(f"Error receiving data: {e}")
        #finally:
        #    #port.close()


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


def configure_port(port, data_rate, transmit_clock, receive_clock, protocol):
    settings = Port.Settings()
    settings.protocol = getattr(Port, protocol)
    settings.encoding = Port.NRZ
    settings.crc = Port.CRC16
    settings.transmit_clock = getattr(Port, transmit_clock)
    settings.receive_clock = getattr(Port, receive_clock)
    settings.internal_clock_rate = data_rate
    port.transmit_idle_pattern = 0xE7
    port.interface = Port.RS232
    port.apply_settings(settings)


if __name__ == "__main__":
    root = tk.Tk()
    app = CommunicationApp(root)
    root.mainloop()
