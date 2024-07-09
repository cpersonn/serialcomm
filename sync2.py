#input:combo box,bsync eklendi.

import sys
import threading
import time
import random
import queue
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
        self.sent_bytes_port1 = 0
        self.sent_bytes_port2 = 0
        self.received_bits_port1 = 0
        self.received_bits_port2 = 0
        self.received_bytes_port1 = 0
        self.received_bytes_port2 = 0
        self.update_leds = True
        self.led_threads = None
        self.error_bits_port1 = 0
        self.error_bits_port2 = 0
        self.sent_data_port1 = queue.Queue()
        self.sent_data_port2 = queue.Queue()
        self.received_data_port1 = queue.Queue()
        self.received_data_port2 = queue.Queue()
        self.compare_thread = None
        self.stop_compare = threading.Event()
        self.selected_value = ""


    def create_widgets(self):
        # Port 1 (Left Side)
        left_frame = tk.Frame(self.root)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(left_frame, text="Port 1:").grid(row=0, column=0, padx=5, pady=5)
        self.port1_entry = tk.Entry(left_frame)
        self.port1_entry.grid(row=0, column=1, padx=5, pady=5)
        self.port1_entry.insert(0, "MGMP1P1")

        tk.Label(left_frame, text="Input File 1:").grid(row=1, column=0, padx=5, pady=5)
        self.input_file1_combobox = ttk.Combobox(left_frame, values=["aa", "55", "ff","Rand", "Browse"])
        self.input_file1_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.input_file1_combobox.current(0)
        self.input_file1_combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)

        tk.Label(left_frame, text="Output File 1:").grid(row=2, column=0, padx=5, pady=5)
        self.output_file1_entry = tk.Entry(left_frame)
        self.output_file1_entry.insert(0, 'C:/Users/user.name/Desktop/test/output1.txt')
        self.output_file1_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(left_frame, text="Browse", command=lambda: self.browse_file2(self.output_file1_entry)).grid(row=2,column=2,padx=5,pady=5)

        tk.Label(left_frame, text="Port 1 Protocol:").grid(row=3, column=0, padx=5, pady=5)
        self.port1_protocol_var = tk.StringVar()
        self.port1_protocol_combobox = ttk.Combobox(left_frame, textvariable=self.port1_protocol_var, state="readonly")
        self.port1_protocol_combobox['values'] = ("HDLC", "ASYNC","RAW")
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

        tk.Label(left_frame, text="Port 1 Async Rate:").grid(row=8, column=0, padx=5, pady=5)
        self.port1_async_rate_entry = tk.Entry(left_frame)
        self.port1_async_rate_entry.grid(row=8, column=1, padx=5, pady=5)
        self.port1_async_rate_entry.insert(0, '4800')

        tk.Label(left_frame, text="Port 1 Data Bit:").grid(row=9, column=0, padx=5, pady=5)
        self.port1_data_bit_entry = tk.Entry(left_frame)
        self.port1_data_bit_entry.grid(row=9, column=1, padx=5, pady=5)
        self.port1_data_bit_entry.insert(0, '8')

        tk.Label(left_frame, text="Port 1 Stop Bit:").grid(row=10, column=0, padx=5, pady=5)
        self.port1_stop_bit_entry = tk.Entry(left_frame)
        self.port1_stop_bit_entry.grid(row=10, column=1, padx=5, pady=5)
        self.port1_stop_bit_entry.insert(0, '1')

        tk.Label(left_frame, text="Port 1 Parity:").grid(row=11, column=0, padx=5, pady=5)
        self.port1_parity_var = tk.StringVar()
        self.port1_parity_combobox = ttk.Combobox(left_frame, textvariable=self.port1_parity_var, state="readonly")
        self.port1_parity_combobox['values'] = ("OFF", "EVEN", "ODD")
        self.port1_parity_combobox.grid(row=11, column=1, padx=5, pady=5)
        self.port1_parity_combobox.current(0)

        self.dtr_port1_button = tk.Button(left_frame, text="DTR Port 1", command=self.toggle_dtr_port1, bg="red")
        self.dtr_port1_button.grid(row=12, column=0, padx=5, pady=5)

        self.rts_port1_button = tk.Button(left_frame, text="RTS Port 1", command=self.toggle_rts_port1, bg="red")
        self.rts_port1_button.grid(row=12, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="CTS Port 1:").grid(row=14, column=0, padx=1, pady=1)
        self.cts_port1_led = tk.Canvas(left_frame, width=20, height=20, bg="red")
        self.cts_port1_led.grid(row=14, column=1, padx=1, pady=1)

        tk.Label(left_frame, text="DSR Port 1:").grid(row=15, column=0, padx=0, pady=0)
        self.dsr_port1_led = tk.Canvas(left_frame, width=20, height=20, bg="red")
        self.dsr_port1_led.grid(row=15, column=1, padx=0, pady=0)

        tk.Label(left_frame, text="DCD Port 1:").grid(row=16, column=0, padx=5, pady=5)
        self.dcd_port1_led = tk.Canvas(left_frame, width=20, height=20, bg="red")
        self.dcd_port1_led.grid(row=16, column=1, padx=5, pady=5)

        self.port1_send_button = tk.Button(left_frame, text="Port 1 Send", command=self.toggle_send_port1)
        self.port1_send_button.grid(row=17, column=0, padx=5, pady=5)

        self.port1_receive_button = tk.Button(left_frame, text="Port 1 Receive", command=self.toggle_receive_port1)
        self.port1_receive_button.grid(row=17, column=1, padx=5, pady=5)

        self.port1_sent_label = tk.Label(left_frame, text="Port 1 Sent Bits: 0")
        self.port1_sent_label.grid(row=18, column=0, padx=5, pady=5)

        self.port1_received_label = tk.Label(left_frame, text="Port 1 Received Bits: 0")
        self.port1_received_label.grid(row=18, column=1, padx=5, pady=5)

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

        self.port1_error_label = tk.Label(center_frame, text="Port 1 Error Bits: 0")
        self.port1_error_label.grid(row=5, column=0, padx=5, pady=5)
        # Port 2 için hata biti sayacı etiketi ekle
        self.port2_error_label = tk.Label(center_frame, text="Port 2 Error Bits: 0")
        self.port2_error_label.grid(row=6, column=0, padx=5, pady=5)

        # Port 2 (Right Side)
        right_frame = tk.Frame(self.root)
        right_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        tk.Label(right_frame, text="Port 2:").grid(row=0, column=0, padx=5, pady=5)
        self.port2_entry = tk.Entry(right_frame)
        self.port2_entry.grid(row=0, column=1, padx=5, pady=5)
        self.port2_entry.insert(0, "MGMP1P2")

        tk.Label(right_frame, text="Input File 2:").grid(row=1, column=0, padx=5, pady=5)
        self.input_file2_combobox = ttk.Combobox(right_frame, values=["aa", "55", "ff","Rand", "Browse"])
        self.input_file2_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.input_file2_combobox.current(0)
        self.input_file2_combobox.bind("<<ComboboxSelected>>", self.on_combobox_select_2)

        tk.Label(right_frame, text="Output File 2:").grid(row=2, column=0, padx=5, pady=5)
        self.output_file2_entry = tk.Entry(right_frame)
        self.output_file2_entry.insert(0, 'C:/Users/user.name/Desktop/test/output2.txt')
        self.output_file2_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(right_frame, text="Browse", command=lambda: self.browse_file2(self.output_file2_entry)).grid(row=2,column=2,padx=5,pady=5)

        tk.Label(right_frame, text="Port 2 Protocol:").grid(row=3, column=0, padx=5, pady=5)
        self.port2_protocol_var = tk.StringVar()
        self.port2_protocol_combobox = ttk.Combobox(right_frame, textvariable=self.port2_protocol_var, state="readonly")
        self.port2_protocol_combobox['values'] = ("HDLC", "ASYNC","RAW")
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

        tk.Label(right_frame, text="Port 2 Async Rate:").grid(row=8, column=0, padx=5, pady=5)
        self.port2_async_rate_entry = tk.Entry(right_frame)
        self.port2_async_rate_entry.grid(row=8, column=1, padx=5, pady=5)
        self.port2_async_rate_entry.insert(0, '4800')

        tk.Label(right_frame, text="Port 2 Data Bit:").grid(row=9, column=0, padx=5, pady=5)
        self.port2_data_bit_entry = tk.Entry(right_frame)
        self.port2_data_bit_entry.grid(row=9, column=1, padx=5, pady=5)
        self.port2_data_bit_entry.insert(0, '8')

        tk.Label(right_frame, text="Port 2 Stop Bit:").grid(row=10, column=0, padx=5, pady=5)
        self.port2_stop_bit_entry = tk.Entry(right_frame)
        self.port2_stop_bit_entry.grid(row=10, column=1, padx=5, pady=5)
        self.port2_stop_bit_entry.insert(0, '1')

        tk.Label(right_frame, text="Port 2 Parity:").grid(row=11, column=0, padx=5, pady=5)
        self.port2_parity_var = tk.StringVar()
        self.port2_parity_combobox = ttk.Combobox(right_frame, textvariable=self.port1_parity_var, state="readonly")
        self.port2_parity_combobox['values'] = ("OFF", "EVEN", "ODD")
        self.port2_parity_combobox.grid(row=11, column=1, padx=5, pady=5)
        self.port2_parity_combobox.current(0)

        self.dtr_port2_button = tk.Button(right_frame, text="DTR Port 2", command=self.toggle_dtr_port2, bg="red")
        self.dtr_port2_button.grid(row=12, column=0, padx=5, pady=5)

        self.rts_port2_button = tk.Button(right_frame, text="RTS Port 2", command=self.toggle_rts_port2, bg="red")
        self.rts_port2_button.grid(row=12, column=1, padx=5, pady=5)

        tk.Label(right_frame, text="CTS Port 2:").grid(row=13, column=0, padx=5, pady=5)
        self.cts_port2_led = tk.Canvas(right_frame, width=20, height=20, bg="red")
        self.cts_port2_led.grid(row=13, column=1, padx=4, pady=5)

        tk.Label(right_frame, text="DSR Port 2:").grid(row=14, column=0, padx=5, pady=5)
        self.dsr_port2_led = tk.Canvas(right_frame, width=20, height=20, bg="red")
        self.dsr_port2_led.grid(row=14, column=1, padx=5, pady=5)

        tk.Label(right_frame, text="DCD Port 2:").grid(row=15, column=0, padx=5, pady=5)
        self.dcd_port2_led = tk.Canvas(right_frame, width=20, height=20, bg="red")
        self.dcd_port2_led.grid(row=15, column=1, padx=5, pady=5)

        self.port2_send_button = tk.Button(right_frame, text="Port 2 Send", command=self.toggle_send_port2)
        self.port2_send_button.grid(row=16, column=0, padx=5, pady=5)

        self.port2_receive_button = tk.Button(right_frame, text="Port 2 Receive", command=self.toggle_receive_port2)
        self.port2_receive_button.grid(row=16, column=1, padx=5, pady=5)

        self.port2_sent_label = tk.Label(right_frame, text="Port 2 Sent Bits: 0")
        self.port2_sent_label.grid(row=17, column=0, padx=5, pady=5)

        self.port2_received_label = tk.Label(right_frame, text="Port 2 Received Bits: 0")
        self.port2_received_label.grid(row=17, column=1, padx=5, pady=5)

        # Configure grid weights to make frames expandable
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def on_combobox_select(self, event):
        self.send_data_port(port=1)


    def send_data_port (self, port):
        if port == 1:
            selected_value = self.input_file1_combobox.get()
            temp_combo = self.input_file1_combobox
            #temp_file_path=self.input_file1_entry
        else:
            selected_value = self.input_file2_combobox.get()
            temp_combo = self.input_file2_combobox
            #temp_file_path = self.input_file2_entry

        if selected_value == "Browse":
            file_path = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
            if file_path:
                #self.input_file2_entry = file_path
                current_values = temp_combo['values']
                new_values = list(current_values)[:-1] + [file_path, "Browse"]
                temp_combo['values'] = new_values
                temp_combo.set(file_path)
                #with open(file_path, 'r') as file:
                #    return file.read().strip()
        elif selected_value == "aa":
            return selected_value*128
        elif selected_value == "55":
            return selected_value*128
        elif selected_value == "ff":
            return selected_value*128
        elif selected_value == "Rand":
            return "".join(random.choice("0123456789ABCDEF") for _ in range(256))
        else:
            selected_value = temp_combo.get()
            with open(selected_value, 'r') as file:
                return file.read().strip()

    def on_combobox_select_2(self, event):
        self.send_data_port(port=2)


    def browse_file2(self, entry):
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
        port1_async_data_rate = self.port1_async_rate_entry.get()
        port2_async_data_rate = self.port2_async_rate_entry.get()
        port1_data_bit = self.port1_data_bit_entry.get()
        port2_data_bit = self.port2_data_bit_entry.get()
        port1_stop_bit = self.port1_stop_bit_entry.get()
        port2_stop_bit = self.port2_stop_bit_entry.get()
        port1_parity = self.port1_parity_combobox.get()
        port2_parity = self.port2_parity_combobox.get()
        self.error_bits_port1 = 0
        self.error_bits_port2 = 0
        self.port1_error_label.config(text="Port 1 Error Bits: 0")
        self.port2_error_label.config(text="Port 2 Error Bits: 0")
        self.received_bits_port1 = 0
        self.received_bits_port2 = 0
        self.received_bytes_port1 = 0
        self.received_bytes_port2 = 0
        self.sent_bits_port1 = 0
        self.sent_bits_port2 = 0
        self.sent_bytes_port1 = 0
        self.sent_bytes_port2 = 0
        self.start_compare_thread()


        if not port1_name or not port2_name:
            messagebox.showerror("Error", "Port names must be specified")
            return

        try:
            self.port1 = open_port(port1_name)
            configure_port(self.port1, port1_data_rate, port1_transmit_clock, port1_receive_clock, port1_protocol,
                           port1_arayuz, port1_async_data_rate, port1_data_bit, port1_stop_bit, port1_parity)
            self.port1.enable_receiver()
            self.port2 = open_port(port2_name)
            configure_port(self.port2, port2_data_rate, port2_transmit_clock, port2_receive_clock, port2_protocol,
                           port2_arayuz, port2_async_data_rate, port2_data_bit, port2_stop_bit, port2_parity)
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
                self.port1,self.input_file1_combobox.get(),
                lambda: self.running_send_port1, self.port1_sent_label, self.sent_bits_port1,self.sent_bytes_port1)).start()

    def toggle_receive_port1(self):
        if self.running_receive_port1:
            self.running_receive_port1 = False
            self.port1_receive_button.config(text="Port 1 Receive", bg="red")

        else:
            self.running_receive_port1 = True
            self.port1_receive_button.config(text="Port 1 Stop", bg="green")
            threading.Thread(target=self.receive_data, args=(
                self.port1, self.output_file1_entry.get(), lambda: self.running_receive_port1,
                self.port1_received_label, self.received_bits_port1,self.received_bytes_port1)).start()

    def toggle_send_port2(self):
        if self.running_send_port2:
            self.running_send_port2 = False
            self.port2_send_button.config(text="Port 2 Send", bg="red")
        else:
            self.running_send_port2 = True
            self.port2_send_button.config(text="Port 2 Stop", bg="green")
            threading.Thread(target=self.send_data, args=(
                self.port2, self.input_file2_combobox.get(),
                lambda: self.running_send_port2, self.port2_sent_label, self.sent_bits_port2,self.sent_bytes_port2)).start()
            self.start_compare_thread()

    def toggle_receive_port2(self):
        if self.running_receive_port2:
            self.running_receive_port2 = False
            self.port2_receive_button.config(text="Port 2 Receive", bg="red")
        else:
            self.running_receive_port2 = True
            self.port2_receive_button.config(text="Port 2 Stop", bg="green")
            threading.Thread(target=self.receive_data, args=(
                self.port2, self.output_file2_entry.get(), lambda: self.running_receive_port2,
                self.port2_received_label, self.received_bits_port2,self.received_bytes_port1)).start()

    def toggle_dtr_port1(self):
        if self.port1:
            try:
                self.port1.dtr = not self.port1.dtr
                print(f"Port 1 DTR set to: {self.port1.dtr}")  # Debug mesajı
                self.dtr_port1_button.config(bg="green" if self.port1.dtr else "red")
            except AttributeError as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", f"Failed to set DTR for Port 1: {str(e)}")

    def toggle_dtr_port2(self):
        if self.port2:
            try:
                self.port2.dtr = not self.port2.dtr
                print(f"Port 2 DTR set to: {self.port2.dtr}")  # Debug mesajı
                self.dtr_port2_button.config(bg="green" if self.port2.dtr else "red")
            except AttributeError as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", f"Failed to set DTR for Port 2: {str(e)}")

    def toggle_rts_port1(self):
        if self.port1:
            try:
                self.port1.rts = not self.port1.rts
                print(f"Port 1 RTS set to: {self.port1.rts}")  # Debug mesajı
                self.rts_port1_button.config(bg="green" if self.port1.rts else "red")
            except AttributeError as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", f"Failed to set RTS for Port 1: {str(e)}")

    def toggle_rts_port2(self):
        if self.port2:
            try:
                self.port2.rts = not self.port2.rts
                print(f"Port 2 RTS set to: {self.port2.rts}")  # Debug mesajı
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
        self.stop_compare.set()

        self.received_data_port1.empty()
        self.sent_data_port1.empty()
        self.received_data_port2.empty()
        self.sent_data_port2.empty()

        self.port1_send_button.config(text="Port 1 Send", bg="red")
        self.port1_receive_button.config(text="Port 1 Receive", bg="red")
        self.port2_send_button.config(text="Port 2 Send", bg="red")
        self.port2_receive_button.config(text="Port 2 Receive", bg="red")

    def show_results(self):
        messagebox.showinfo(
            "Results",
            f"Port 1 - Total Sent Bits: {self.sent_bits_port1}, Total Received Bits: {self.received_bits_port1}, Error Bits: {self.error_bits_port1}\n"
            f"Port 2 - Total Sent Bits: {self.sent_bits_port2}, Total Received Bits: {self.received_bits_port2}, Error Bits: {self.error_bits_port2}"
        )

    def send_data(self, port, combo, running_check, label, bits_counter, bytes_counter):
        try:

            i = 1
            while running_check():
                if port.name == "MGMP1P1":
                    hex_data = self.send_data_port(port=1)
                    buf_send = bytearray.fromhex(self.send_data_port(port=1))
                else:
                    hex_data = self.send_data_port(port=2)
                    buf_send = bytearray.fromhex(self.send_data_port(port=2))


                #hex_data = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                #buf_send = bytearray.fromhex(hex_data)


                print(f'>>> {port.name} ' + '{:0>9d}'.format(i) + ' send ' + str(len(buf_send)) + ' bytes: ' + hex_data)
                port.write(buf_send)
                port.flush()
                bits_counter += len(buf_send) * 8
                bytes_counter += len(buf_send)
                if port.name == self.port1_entry.get():
                    self.sent_bits_port1 += len(buf_send) * 8
                    self.sent_data_port1.put(buf_send)
                else:
                    self.sent_bits_port2 += len(buf_send) * 8
                    self.sent_data_port2.put(buf_send)
                label.config(text=f"{port.name} Sent Bytes: {bytes_counter}")
                i += 1
        except Exception as e:
            print(f"Error sending data: {e}")

    def receive_data(self, port, output_file, running_check, label, bits_counter, bytes_counter):
        i = 1
        try:
            with open(output_file, 'w') as f:
                while running_check():
                    buf_read = port.read(128)
                    if not buf_read:
                        break
                    hex_data = buf_read.hex()
                    print(f'<<< {port.name} ' + '{:0>9d}'.format(i) + ' received ' + str(len(buf_read)) + ' bytes: ' + hex_data)
                    f.write(hex_data + '\n')
                    bits_counter += len(buf_read) * 8
                    bytes_counter+= len(buf_read)
                    if port.name == self.port1_entry.get():
                        self.received_bits_port1 += len(buf_read) * 8
                        self.received_data_port1.put(buf_read)
                    else:
                        self.received_bits_port2 += len(buf_read) * 8
                        self.received_data_port2.put(buf_read)
                    label.config(text=f"{port.name} Received Bytes: {bytes_counter}")
                    i += 1
        except Exception as e:
            print(f"Error receiving data: {e}")

    def start_compare_thread(self):
        self.stop_compare.clear()
        self.compare_thread = threading.Thread(target=self.compare_data_thread)
        self.compare_thread.start()

    def compare_data_thread(self):
        while not self.stop_compare.is_set():
            self.compare_port_data(1, self.sent_data_port1, self.received_data_port1)
            self.compare_port_data(2, self.sent_data_port2, self.received_data_port2)
            time.sleep(0.05)  # Adjust this value to control how often comparisons are made

    def compare_port_data(self, port_number, sent_queue, received_queue):
        sent_data = bytearray()
        received_data = bytearray()

        # Collect all available sent data
        while not sent_queue.empty():
            try:
                item = sent_queue.get_nowait()
                if isinstance(item, (bytes, bytearray)):
                    sent_data.extend(item)
                else:
                    sent_data.extend(bytes[item])
            except queue.Empty:
                break

        # Collect all available received data
        while not received_queue.empty():
            try:
                item = received_queue.get_nowait()
                if isinstance(item, (bytes, bytearray)):
                    received_data.extend(item)
                else:
                    received_data.extend(bytes[item])
            except queue.Empty:
                break

        # Compare the data
        min_length = min(len(sent_data), len(received_data))
        if min_length > 0:
            self.compare_data(sent_data[:min_length], received_data[:min_length], port_number)
            # Remove compared data from the beginning of each buffer
            if len(sent_data) != len(received_data):
                print(f'(!) LEFT ON SENT QUEUE:    {sent_data.hex()}')
                print(f'(!) LEFT ON RECEIVE QUEUE: {received_data.hex()}')
                del sent_data
                del received_data
            else:
                del sent_data[:min_length]
                del received_data[:min_length]


    def compare_data(self, sent_data, received_data, port_number):
        error_bits = 0
        total_bits = len(received_data) * 8

        for sent_byte, received_byte in zip(sent_data, received_data):
            if sent_byte != received_byte:
                for i in range(8):
                    if (sent_byte >> i) & 1 != (received_byte >> i) & 1:
                        error_bits += 1

        if port_number == 1:
            self.error_bits_port1 += error_bits
            self.port1_error_label.config(text=f"Port 1 Error Bits: {self.error_bits_port1}")
        else:
            self.error_bits_port2 += error_bits
            self.port2_error_label.config(text=f"Port 2 Error Bits: {self.error_bits_port2}")

        error_rate = (error_bits / total_bits) * 100 if total_bits > 0 else 0
        print(f"Port {port_number} - Error rate: {error_rate:.2f}% ({error_bits}/{total_bits} bits)")
        print(f"Sent data:     {sent_data.hex()}")
        print(f"Received data: {received_data.hex()}")


def generate_random_data(length):
    """Generate random data of specified length."""
    return bytearray([random.randint(0, 255) for _ in range(length)])


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


def configure_port(port, data_rate, transmit_clock, receive_clock, protocol, arayuz, async_rate, data_bit, stop_bit, parity):
    settings = Port.Settings()
    settings.protocol = getattr(Port, protocol)
    if protocol == "HDLC":
        settings.encoding = Port.NRZ
        settings.crc = Port.CRC16
        settings.transmit_clock = getattr(Port, transmit_clock)
        settings.receive_clock = getattr(Port, receive_clock)
        settings.internal_clock_rate = data_rate
        port.transmit_idle_pattern = 0xE7
        port.interface = getattr(Port, arayuz)
        port.apply_settings(settings)
    if protocol == "ASYNC":
        settings.encoding = Port.NRZ
        settings.async_data_rate = int(async_rate)
        settings.async_data_bits = int(data_bit)
        settings.async_stop_bits = int(stop_bit)
        settings.async_parity = getattr(Port, parity)
        port.interface = getattr(Port, arayuz)
        port.apply_settings(settings)
    if protocol == "RAW":
        settings.protocol = Port.RAW
        settings.encoding = Port.NRZ
        settings.crc = Port.OFF
        settings.transmit_clock = getattr(Port, transmit_clock)
        settings.receive_clock = getattr(Port, receive_clock)
        settings.internal_clock_rate = data_rate
        #port.interface = getattr(Port, arayuz)
        settings.msb_first = True
        port.apply_settings(settings)
        port.transmit_idle_pattern = 0xff


if __name__ == "__main__":
    root = tk.Tk()
    app = CommunicationApp(root)
    root.mainloop()
