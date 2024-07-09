import sys
import threading
import time
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
        self.update_leds = True
        self.led_threads = None

    def create_widgets(self):
                  # Port 1 (Left Side)
            left_frame = tk.Frame(self.root)
            left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            tk.Label(left_frame, text="Port 1:").grid(row=0, column=0, padx=5, pady=5)
            self.port1_entry = tk.Entry(left_frame)
            self.port1_entry.grid(row=0, column=1, padx=5, pady=5)
            self.port1_entry.insert(0, "MGMP1P1")

            tk.Label(left_frame, text="Input File 1:").grid(row=1, column=0, padx=5, pady=5)
            self.input_file1_entry = tk.Entry(left_frame)
            self.input_file1_entry.grid(row=1, column=1, padx=5, pady=5)
            tk.Button(left_frame, text="Browse", command=lambda: self.browse_file(self.input_file1_entry)).grid(row=1,
                                                                                                                column=2,
                                                                                                                padx=5,
                                                                                                                pady=5)

            tk.Label(left_frame, text="Output File 1:").grid(row=2, column=0, padx=5, pady=5)
            self.output_file1_entry = tk.Entry(left_frame)
            self.output_file1_entry.grid(row=2, column=1, padx=5, pady=5)
            tk.Button(left_frame, text="Browse", command=lambda: self.browse_file(self.output_file1_entry)).grid(row=2,
                                                                                                                 column=2,
                                                                                                                 padx=5,
                                                                                                                 pady=5)

            tk.Label(left_frame, text="Port 1 Protocol:").grid(row=3, column=0, padx=5, pady=5)
            self.port1_protocol_var = tk.StringVar()
            self.port1_protocol_combobox = ttk.Combobox(left_frame, textvariable=self.port1_protocol_var,
                                                        state="readonly")
            self.port1_protocol_combobox['values'] = ("HDLC", "ASYNC")
            self.port1_protocol_combobox.grid(row=3, column=1, padx=5, pady=5)
            self.port1_protocol_combobox.current(0)

            tk.Label(left_frame, text="Port 1 Arayuz:").grid(row=4, column=0, padx=5, pady=5)
            self.port1_arayuz_var = tk.StringVar()
            self.port1_arayuz_combobox = ttk.Combobox(left_frame, textvariable=self.port1_arayuz_var, state="readonly")
            self.port1_arayuz_combobox['values'] = ("RS232", "RS422")
            self.port1_arayuz_combobox.grid(row=4, column=1, padx=5, pady=5)
            self.port1_arayuz_combobox.current(0)

            tk.Label(left_frame, text="Port 1 Data Rate:").grid(row=5, column=0, padx=5, pady=5)
            self.port1_data_rate_entry = tk.Entry(left_frame)
            self.port1_data_rate_entry.grid(row=5, column=1, padx=5, pady=5)
            self.port1_data_rate_entry.insert(0, '9600')

            tk.Label(left_frame, text="Port 1 Transmit Clock:").grid(row=6, column=0, padx=5, pady=5)
            self.port1_transmit_clock_var = tk.StringVar()
            self.port1_transmit_clock_combobox = ttk.Combobox(left_frame, textvariable=self.port1_transmit_clock_var,
                                                              state="readonly")
            self.port1_transmit_clock_combobox['values'] = ("TXC_INPUT", "RXC_INPUT", "INTERNAL")
            self.port1_transmit_clock_combobox.grid(row=6, column=1, padx=5, pady=5)
            self.port1_transmit_clock_combobox.current(2)

            tk.Label(left_frame, text="Port 1 Receive Clock:").grid(row=7, column=0, padx=5, pady=5)
            self.port1_receive_clock_var = tk.StringVar()
            self.port1_receive_clock_combobox = ttk.Combobox(left_frame, textvariable=self.port1_receive_clock_var,
                                                             state="readonly")
            self.port1_receive_clock_combobox['values'] = ("TXC_INPUT", "RXC_INPUT", "INTERNAL")
            self.port1_receive_clock_combobox.grid(row=7, column=1, padx=5, pady=5)
            self.port1_receive_clock_combobox.current(2)

            self.dtr_port1_button = tk.Button(left_frame, text="DTR Port 1", command=self.toggle_dtr_port1, bg="red")
            self.dtr_port1_button.grid(row=8, column=0, padx=5, pady=5)

            self.rts_port1_button = tk.Button(left_frame, text="RTS Port 1", command=self.toggle_rts_port1, bg="red")
            self.rts_port1_button.grid(row=8, column=1, padx=5, pady=5)

            tk.Label(left_frame, text="CTS Port 1:").grid(row=9, column=0, padx=1, pady=1)
            self.cts_port1_led = tk.Canvas(left_frame, width=20, height=20, bg="red")
            self.cts_port1_led.grid(row=9, column=1, padx=1, pady=1)

            tk.Label(left_frame, text="DSR Port 1:").grid(row=10, column=0, padx=0, pady=0)
            self.dsr_port1_led = tk.Canvas(left_frame, width=20, height=20, bg="red")
            self.dsr_port1_led.grid(row=10, column=1, padx=0, pady=0)

            tk.Label(left_frame, text="DCD Port 1:").grid(row=11, column=0, padx=5, pady=5)
            self.dcd_port1_led = tk.Canvas(left_frame, width=20, height=20, bg="red")
            self.dcd_port1_led.grid(row=11, column=1, padx=5, pady=5)

            self.port1_send_button = tk.Button(left_frame, text="Port 1 Send", command=self.toggle_send_port1)
            self.port1_send_button.grid(row=12, column=0, padx=5, pady=5)

            self.port1_receive_button = tk.Button(left_frame, text="Port 1 Receive", command=self.toggle_receive_port1)
            self.port1_receive_button.grid(row=12, column=1, padx=5, pady=5)

            self.port1_sent_label = tk.Label(left_frame, text="Port 1 Sent Bits: 0")
            self.port1_sent_label.grid(row=13, column=0, padx=5, pady=5)

            self.port1_received_label = tk.Label(left_frame, text="Port 1 Received Bits: 0")
            self.port1_received_label.grid(row=13, column=1, padx=5, pady=5)

            # Common Buttons (Center)
            center_frame = tk.Frame(self.root)
            center_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

            tk.Button(center_frame, text="Configure Ports", command=self.configure_ports).grid(row=0, column=0, padx=5,
                                                                                               pady=5)
            self.stop_button = tk.Button(center_frame, text="Stop All", command=self.stop_all)
            self.stop_button.grid(row=1, column=0, padx=5, pady=5)
            self.led_thread_button = tk.Button(center_frame, text="LED Thread", command=self.toggle_led_thread)
            self.led_thread_button.grid(row=2, column=0, padx=5, pady=10)
            self.results_button = tk.Button(center_frame, text="Show Results", command=self.show_results)
            self.results_button.grid(row=3, column=0, padx=5, pady=5)
            tk.Button(center_frame, text="Quit", command=self.root.quit).grid(row=4, column=0, padx=5, pady=5)

            # Port 2 (Right Side)
            right_frame = tk.Frame(self.root)
            right_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

            tk.Label(right_frame, text="Port 2:").grid(row=0, column=0, padx=5, pady=5)
            self.port2_entry = tk.Entry(right_frame)
            self.port2_entry.grid(row=0, column=1, padx=5, pady=5)
            self.port2_entry.insert(0, "MGMP1P2")

            tk.Label(right_frame, text="Input File 2:").grid(row=1, column=0, padx=5, pady=5)
            self.input_file2_entry = tk.Entry(right_frame)
            self.input_file2_entry.grid(row=1, column=1, padx=5, pady=5)
            tk.Button(right_frame, text="Browse", command=lambda: self.browse_file(self.input_file2_entry)).grid(row=1,
                                                                                                                 column=2,
                                                                                                                 padx=5,
                                                                                                                 pady=5)

            tk.Label(right_frame, text="Output File 2:").grid(row=2, column=0, padx=5, pady=5)
            self.output_file2_entry = tk.Entry(right_frame)
            self.output_file2_entry.grid(row=2, column=1, padx=5, pady=5)
            tk.Button(right_frame, text="Browse", command=lambda: self.browse_file(self.output_file2_entry)).grid(row=2,
                                                                                                                  column=2,
                                                                                                                  padx=5,
                                                                                                                  pady=5)

            tk.Label(right_frame, text="Port 2 Protocol:").grid(row=3, column=0, padx=5, pady=5)
            self.port2_protocol_var = tk.StringVar()
            self.port2_protocol_combobox = ttk.Combobox(right_frame, textvariable=self.port2_protocol_var,
                                                        state="readonly")
            self.port2_protocol_combobox['values'] = ("HDLC", "ASYNC")
            self.port2_protocol_combobox.grid(row=3, column=1, padx=5, pady=5)
            self.port2_protocol_combobox.current(0)

            tk.Label(right_frame, text="Port 2 Arayuz:").grid(row=4, column=0, padx=5, pady=5)
            self.port2_arayuz_var = tk.StringVar()
            self.port2_arayuz_combobox = ttk.Combobox(right_frame, textvariable=self.port2_arayuz_var, state="readonly")
            self.port2_arayuz_combobox['values'] = ("RS232", "RS422")
            self.port2_arayuz_combobox.grid(row=4, column=1, padx=5, pady=5)
            self.port2_arayuz_combobox.current(0)

            tk.Label(right_frame, text="Port 2 Data Rate:").grid(row=5, column=0, padx=5, pady=5)
            self.port2_data_rate_entry = tk.Entry(right_frame)
            self.port2_data_rate_entry.grid(row=5, column=1, padx=5, pady=5)
            self.port2_data_rate_entry.insert(0, '9600')

            tk.Label(right_frame, text="Port 2 Transmit Clock:").grid(row=6, column=0, padx=5, pady=5)
            self.port2_transmit_clock_var = tk.StringVar()
            self.port2_transmit_clock_combobox = ttk.Combobox(right_frame, textvariable=self.port2_transmit_clock_var,
                                                              state="readonly")
            self.port2_transmit_clock_combobox['values'] = ("TXC_INPUT", "RXC_INPUT", "INTERNAL")
            self.port2_transmit_clock_combobox.grid(row=6, column=1, padx=5, pady=5)
            self.port2_transmit_clock_combobox.current(0)

            tk.Label(right_frame, text="Port 2 Receive Clock:").grid(row=7, column=0, padx=5, pady=5)
            self.port2_receive_clock_var = tk.StringVar()
            self.port2_receive_clock_combobox = ttk.Combobox(right_frame, textvariable=self.port2_receive_clock_var,
                                                             state="readonly")
            self.port2_receive_clock_combobox['values'] = ("TXC_INPUT", "RXC_INPUT", "INTERNAL")
            self.port2_receive_clock_combobox.grid(row=7, column=1, padx=5, pady=5)
            self.port2_receive_clock_combobox.current(0)

            self.dtr_port2_button = tk.Button(right_frame, text="DTR Port 2", command=self.toggle_dtr_port2, bg="red")
            self.dtr_port2_button.grid(row=8, column=0, padx=5, pady=5)

            self.rts_port2_button = tk.Button(right_frame, text="RTS Port 2", command=self.toggle_rts_port2, bg="red")
            self.rts_port2_button.grid(row=8, column=1, padx=5, pady=5)

            tk.Label(right_frame, text="CTS Port 2:").grid(row=9, column=0, padx=5, pady=5)
            self.cts_port2_led = tk.Canvas(right_frame, width=20, height=20, bg="red")
            self.cts_port2_led.grid(row=9, column=1, padx=4, pady=5)

            tk.Label(right_frame, text="DSR Port 2:").grid(row=10, column=0, padx=5, pady=5)
            self.dsr_port2_led = tk.Canvas(right_frame, width=20, height=20, bg="red")
            self.dsr_port2_led.grid(row=10, column=1, padx=5, pady=5)

            tk.Label(right_frame, text="DCD Port 2:").grid(row=11, column=0, padx=5, pady=5)
            self.dcd_port2_led = tk.Canvas(right_frame, width=20, height=20, bg="red")
            self.dcd_port2_led.grid(row=11, column=1, padx=5, pady=5)

            self.port2_send_button = tk.Button(right_frame, text="Port 2 Send", command=self.toggle_send_port2)
            self.port2_send_button.grid(row=12, column=0, padx=5, pady=5)

            self.port2_receive_button = tk.Button(right_frame, text="Port 2 Receive", command=self.toggle_receive_port2)
            self.port2_receive_button.grid(row=12, column=1, padx=5, pady=5)

            self.port2_sent_label = tk.Label(right_frame, text="Port 2 Sent Bits: 0")
            self.port2_sent_label.grid(row=13, column=0, padx=5, pady=5)

            self.port2_received_label = tk.Label(right_frame, text="Port 2 Received Bits: 0")
            self.port2_received_label.grid(row=13, column=1, padx=5, pady=5)

            # Configure grid weights to make frames expandable
            self.root.grid_columnconfigure(0, weight=1)
            self.root.grid_columnconfigure(1, weight=1)
            self.root.grid_columnconfigure(2, weight=1)
            self.root.grid_rowconfigure(0, weight=1)


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
        port1_arayuz = self.port1_arayuz_combobox.get()
        port2_arayuz = self.port2_arayuz_combobox.get()

        if not port1_name or not port2_name:
            messagebox.showerror("Error", "Port names must be specified")
            return

        try:
            self.port1 = open_port(port1_name)
            configure_port(self.port1, port1_data_rate, port1_transmit_clock, port1_receive_clock, port1_protocol,port1_arayuz)
            self.port1.enable_receiver()
            self.port2 = open_port(port2_name)
            configure_port(self.port2, port2_data_rate, port2_transmit_clock, port2_receive_clock, port2_protocol,port2_arayuz)
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

    def toggle_dtr_port1(self):
        if self.port1:
            try:
                self.port1.dtr = not self.port1.dtr
                print(f"Port 1 DTR set to: {self.port1.dtr}")  # Debug mesaji
                self.dtr_port1_button.config(bg="green" if self.port1.dtr else "red")
            except AttributeError as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", f"Failed to set DTR for Port 1: {str(e)}")

    def toggle_dtr_port2(self):
        if self.port2:
            try:
                self.port2.dtr = not self.port2.dtr
                print(f"Port 2 DTR set to: {self.port2.dtr}")  # Debug mesaji
                self.dtr_port2_button.config(bg="green" if self.port2.dtr else "red")
            except AttributeError as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", f"Failed to set DTR for Port 2: {str(e)}")

    def toggle_rts_port1(self):
        if self.port1:
            try:
                self.port1.rts = not self.port1.rts
                print(f"Port 1 RTS set to: {self.port1.rts}")  # Debug mesaji
                self.rts_port1_button.config(bg="green" if self.port1.rts else "red")
            except AttributeError as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", f"Failed to set RTS for Port 1: {str(e)}")

    def toggle_rts_port2(self):
        if self.port2:
            try:
                self.port2.rts = not self.port2.rts
                print(f"Port 2 RTS set to: {self.port2.rts}")  # Debug mesaji
                self.rts_port2_button.config(bg="green" if self.port2.rts else "red")
            except AttributeError as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", f"Failed to set RTS for Port 2: {str(e)}")

    def update_led_states(self):
        while self.update_leds:
            if self.port1:
                # Update CTS LED for Port 1
                if self.port1.cts:
                    self.cts_port1_led.config(bg="green")
                else:
                    self.cts_port1_led.config(bg="red")

                # Update DSR LED for Port 1
                if self.port1.dsr:
                    self.dsr_port1_led.config(bg="green")
                else:
                    self.dsr_port1_led.config(bg="red")

                if self.port1.dcd:
                    self.dcd_port1_led.config(bg="green")
                else:
                    self.dcd_port1_led.config(bg="red")

            if self.port2:
                # Update CTS LED for Port 2
                if self.port2.cts:
                    self.cts_port2_led.config(bg="green")
                else:
                    self.cts_port2_led.config(bg="red")
                # Update DSR LED for Port 2
                if self.port2.dsr:
                    self.dsr_port2_led.config(bg="green")
                else:
                    self.dsr_port2_led.config(bg="red")
                # Update DCD LED for Port 2
                if self.port2.dcd:
                    self.dcd_port2_led.config(bg="green")
                else:
                    self.dcd_port2_led.config(bg="red")

            # Delay before updating LEDs again (adjust as needed)
            time.sleep(0.5)

    def toggle_led_thread(self):
        if self.update_leds:
            # Stop the LED update thread
            self.update_leds = False
            if self.led_thread:
                self.led_thread.join()  # Wait for the thread to finish
            self.led_thread_button.config(text="LED Thread")
        else:
            # Start the LED update thread
            self.update_leds = True
            self.led_thread = threading.Thread(target=self.update_led_states)
            self.led_thread.start()
            self.led_thread_button.config(text="Stop LED Thread")

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
            #print('receive sonlandirildi.')


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


def configure_port(port, data_rate, transmit_clock, receive_clock, protocol, arayuz):
    settings = Port.Settings()
    settings.protocol = getattr(Port, protocol)
    settings.encoding = Port.NRZ
    settings.crc = Port.CRC16
    settings.transmit_clock = getattr(Port, transmit_clock)
    settings.receive_clock = getattr(Port, receive_clock)
    settings.internal_clock_rate = data_rate
    port.transmit_idle_pattern = 0xE7
    port.interface = getattr(Port, arayuz)
    port.apply_settings(settings)


if __name__ == "__main__":
    root = tk.Tk()
    app = CommunicationApp(root)
    root.mainloop()
