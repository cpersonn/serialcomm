#
# This file is part of the mgapi package that implements an
# interface to the Microgate serial API for Windows.
#
# Copyright (C) 2019 Microgate Systems, Ltd.
#

import ctypes
from ctypes import wintypes
from copy import deepcopy

#
# Win32 definitions
#

kernel32_dll = ctypes.windll.LoadLibrary("kernel32.dll")

ERROR_ACCESS_DENIED = 5
ERROR_NOT_READY = 21
ERROR_GEN_FAILURE = 31
ERROR_OPEN_FAILED = 110
ERROR_BUSY = 170
ERROR_IO_PENDING = 997
ERROR_BAD_DEVICE = 1200
ERROR_DEVICE_IN_USE = 2404

INFINITE = 0xFFFFFFFF
WAIT_ABANDONED = 0x80
WAIT_OBJECT_0 = 0
WAIT_TIMEOUT = 0x102

HANDLE = wintypes.HANDLE
ULONG = wintypes.ULONG
UCHAR = ctypes.c_byte
LPVOID = wintypes.LPVOID
DWORD = wintypes.DWORD
LPCSTR = wintypes.LPCSTR
BOOL = wintypes.BOOL

class OVERLAPPED(ctypes.Structure):
    _fields_ = [
        ("Internal", LPVOID),
        ("InternalHigh", LPVOID),
        ("Offset", ULONG),
        ("OffsetHigh", ULONG),
        ("hEvent", HANDLE)
    ]

    def __init__(self):
        self.Internal = 0
        self.InternalHigh = 0
        self.Offset = 0
        self.OffsetHigh = 0
        self.hEvent = 0

    def __repr__(self):
        return 'OVERLAPPED object at ' + hex(id(self)) + '\n'

    def __str__(self):
        return self.__repr__()


# DWORD GetLastError();
c_GetLastError = kernel32_dll.GetLastError
c_GetLastError.argtypes = []
c_GetLastError.restype = DWORD

def GetLastError() -> int:
    """Return last Win32 error code."""
    return c_GetLastError()


# DWORD WaitForSingleObject(HANDLE hHandle, DWORD dwMilliseconds);
c_WaitForSingleObject = kernel32_dll.WaitForSingleObject
c_WaitForSingleObject.argtypes = [HANDLE, DWORD]
c_WaitForSingleObject.restype = DWORD

def WaitForSingleObject(handle: HANDLE, timeout: int) -> int:
    """Wait for Win32 object to be signalled."""
    return c_WaitForSingleObject(handle, DWORD(timeout))


# HANDLE CreateEventA(LPSECURITY_ATTRIBUTES lpEventAttributes,
#            BOOL bManualReset, BOOL bInitialState, LPCSTR lpName);
c_CreateEvent = kernel32_dll.CreateEventA
c_CreateEvent.argtypes = [wintypes.LPVOID, wintypes.BOOL,
                          wintypes.BOOL, wintypes.LPCSTR]
c_CreateEvent.restype = HANDLE

def CreateEvent(manual_reset: bool, initial_state: bool) -> HANDLE:
    """Create Win32 event object."""
    return c_CreateEvent(wintypes.LPVOID(0), wintypes.BOOL(manual_reset),
            wintypes.BOOL(initial_state), wintypes.LPCSTR(0))


# BOOL ResetEvent(HANDLE hEvent);
c_ResetEvent = kernel32_dll.ResetEvent
c_ResetEvent.argtypes = [HANDLE]
c_ResetEvent.restype = wintypes.BOOL

def ResetEvent(handle: HANDLE) -> int:
    """Reset Win32 event object."""
    return c_ResetEvent(handle)


# BOOL CloseHandle(HANDLE hObject);
c_CloseHandle = kernel32_dll.CloseHandle
c_CloseHandle.argtypes = [HANDLE]
c_CloseHandle.restype = wintypes.BOOL

def CloseHandle(handle: HANDLE) -> int:
    """Close handle to Win32 object."""
    return c_CloseHandle(handle)


#
# Microgate API definitions
#

mghdlc_dll = ctypes.windll.LoadLibrary("mghdlc.dll")

MGSL_MAX_PORTS = 200
HDLC_MAX_FRAME_SIZE = 65535
MAX_ASYNC_TRANSMIT = 4096

ASYNC_PARITY_NONE = 0
ASYNC_PARITY_EVEN = 1
ASYNC_PARITY_ODD = 2

HDLC_FLAG_UNDERRUN_ABORT7 = 0x0000
HDLC_FLAG_UNDERRUN_ABORT15 = 0x0001
HDLC_FLAG_UNDERRUN_FLAG = 0x0002
HDLC_FLAG_UNDERRUN_CRC = 0x0004
HDLC_FLAG_SHARE_ZERO = 0x0010
HDLC_FLAG_AUTO_CTS = 0x0020
HDLC_FLAG_AUTO_DCD = 0x0040
HDLC_FLAG_AUTO_RTS = 0x0080
HDLC_FLAG_RXC_DPLL = 0x0100
HDLC_FLAG_RXC_BRG = 0x0200
HDLC_FLAG_RXC_TXCPIN = 0x8000
HDLC_FLAG_RXC_RXCPIN = 0x0000
HDLC_FLAG_TXC_DPLL = 0x0400
HDLC_FLAG_TXC_BRG = 0x0800
HDLC_FLAG_TXC_TXCPIN = 0x0000
HDLC_FLAG_TXC_RXCPIN = 0x0008
HDLC_FLAG_DPLL_DIV8 = 0x1000
HDLC_FLAG_DPLL_DIV16 = 0x2000
HDLC_FLAG_DPLL_DIV32 = 0x0000
HDLC_FLAG_HDLC_LOOPMODE = 0x4000
HDLC_FLAG_RXC_INV = 0x0002
HDLC_FLAG_TXC_INV = 0x0004

HDLC_CRC_NONE = 0
HDLC_CRC_16_CCITT = 1
HDLC_CRC_32_CCITT = 2
HDLC_CRC_MODE = 0x00ff
HDLC_CRC_RETURN_CRCERR_FRAME = 0x8000
HDLC_CRC_RETURN_CRC = 0x4000

HDLC_TXIDLE_FLAGS = 0
HDLC_TXIDLE_ALT_ZEROS_ONES = 1
HDLC_TXIDLE_ZEROS = 2
HDLC_TXIDLE_ONES = 3
HDLC_TXIDLE_ALT_MARK_SPACE = 4
HDLC_TXIDLE_SPACE = 5
HDLC_TXIDLE_MARK = 6
HDLC_TXIDLE_CUSTOM_8 = 0x10000000
HDLC_TXIDLE_CUSTOM_16 = 0x20000000

HDLC_ENCODING_NRZ = 0
HDLC_ENCODING_NRZB = 1
HDLC_ENCODING_NRZI_MARK = 2
HDLC_ENCODING_NRZI_SPACE = 3
HDLC_ENCODING_NRZI = HDLC_ENCODING_NRZI_SPACE
HDLC_ENCODING_BIPHASE_MARK = 4
HDLC_ENCODING_BIPHASE_SPACE = 5
HDLC_ENCODING_BIPHASE_LEVEL = 6
HDLC_ENCODING_DIFF_BIPHASE_LEVEL = 7

HDLC_PREAMBLE_LENGTH_8BITS = 0
HDLC_PREAMBLE_LENGTH_16BITS = 1
HDLC_PREAMBLE_LENGTH_32BITS = 2
HDLC_PREAMBLE_LENGTH_64BITS = 3

HDLC_PREAMBLE_PATTERN_NONE = 0
HDLC_PREAMBLE_PATTERN_ZEROS = 1
HDLC_PREAMBLE_PATTERN_FLAGS = 2
HDLC_PREAMBLE_PATTERN_10 = 3
HDLC_PREAMBLE_PATTERN_01 = 4
HDLC_PREAMBLE_PATTERN_ONES = 5

MGSL_MODE_ASYNC = 1
MGSL_MODE_HDLC = 2
MGSL_MODE_MONOSYNC = 3
MGSL_MODE_BISYNC = 4
MGSL_MODE_EXTERNALSYNC = 6
MGSL_MODE_RAW = MGSL_MODE_EXTERNALSYNC
MGSL_MODE_TDM = 7

# definitions for building MGSL_OPT_TDM value

# TDM sync frame [bit 20]
TDM_SYNC_FRAME_OFF = 0
TDM_SYNC_FRAME_ON  = 1 << 20

# TDM sync to data delay [bits 19:18]
TDM_SYNC_DELAY_NONE = 0
TDM_SYNC_DELAY_1BIT = 1 << 18
TDM_SYNC_DELAY_2BITS = 2 << 18

# TDM transmit sync width [bit 17]
TDM_TX_SYNC_WIDTH_SLOT = 0
TDM_TX_SYNC_WIDTH_BIT = 1 << 17

# TDM Sync polarity [bit 16]
TDM_SYNC_POLARITY_NORMAL = 0
TDM_SYNC_POLARITY_INVERT = 1 << 16

# TDM RX FRAME COUNT [bits 15:8]
def TDM_RX_FRAME_COUNT(frame_count:int) -> int:
    """Return frame count field specified by frame count."""
    return (frame_count - 1) << 8

# TDM slot count [bits 7:3] : 0=384 slots, 1-31 = 2-32 slots
def TDM_SLOT_COUNT(slot_count:int) -> int:
    """Return slot count field specified by slot count."""
    if slot_count == 384:
        return 0
    return ((slot_count - 1) & 0x1f) << 3

# TDM slot size [bits 2:0]
TDM_SLOT_SIZE_8BITS = 1
TDM_SLOT_SIZE_12BITS = 2
TDM_SLOT_SIZE_16BITS = 3
TDM_SLOT_SIZE_20BITS = 4
TDM_SLOT_SIZE_24BITS = 5
TDM_SLOT_SIZE_28BITS = 6
TDM_SLOT_SIZE_32BITS = 7


class MGSL_PARAMS(ctypes.Structure):
    _pack_ = 8
    _fields_ = [
        ("Mode", ULONG),  # protocol selection (MGSL_MODE_XXX)
        ("Loopback", UCHAR),  # 0=normal operation, 1=internal loopback
        ("Flags", wintypes.USHORT),  # misc options (HDLC_FLAG_XXX)
        ("Encoding", UCHAR),  # data encoding (NRZI, NRZ, etc)
        ("ClockSpeed", ULONG),  # BRG/DPLL rate (sync modes)
        ("Addr", UCHAR),  # HDLC address filter (0xFF=receive all)
        ("CrcType", wintypes.USHORT),  # frame check selection (HDLC only)
        ("PreambleLength", UCHAR),  # preamble length (8,16,32,64 bits)
        ("PreamblePattern", UCHAR),  # sync mode preamble pattern
        ("DataRate", ULONG),  # async mode data rate
        ("DataBits", UCHAR),  # async mode data bits (5..8)
        ("StopBits", UCHAR),  # async mode stop bits (1..2)
        ("Parity", UCHAR)  # async mode parity bit
    ]

    def mode_str(self):
        if self.Mode == MGSL_MODE_ASYNC:
            return 'MGSL_MODE_ASYNC'
        elif self.Mode == MGSL_MODE_HDLC:
            return 'MGSL_MODE_HDLC'
        elif self.Mode == MGSL_MODE_MONOSYNC:
            return 'MGSL_MODE_MONOSYNC'
        elif self.Mode == MGSL_MODE_BISYNC:
            return 'MGSL_MODE_BISYNC'
        elif self.Mode == MGSL_MODE_RAW:
            return 'MGSL_MODE_RAW'
        elif self.Mode == MGSL_MODE_TDM:
            return 'MGSL_MODE_TDM'
        else:
            return 'unknown mode = ' + hex(self.Mode)

    def flags_str(self):
        d = ''
        if self.Flags & HDLC_FLAG_UNDERRUN_ABORT7:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_UNDERRUN_ABORT7'
        if self.Flags & HDLC_FLAG_UNDERRUN_ABORT15:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_UNDERRUN_ABORT15'
        if self.Flags & HDLC_FLAG_UNDERRUN_FLAG:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_UNDERRUN_FLAG'
        if self.Flags & HDLC_FLAG_UNDERRUN_CRC:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_UNDERRUN_CRC'
        if self.Flags & HDLC_FLAG_SHARE_ZERO:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_SHARE_ZERO'
        if self.Flags & HDLC_FLAG_AUTO_CTS:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_AUTO_CTS'
        if self.Flags & HDLC_FLAG_AUTO_DCD:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_AUTO_DCD'
        if self.Flags & HDLC_FLAG_AUTO_RTS:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_AUTO_RTS'
        if self.Flags & HDLC_FLAG_RXC_DPLL:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_RXC_DPLL'
        if self.Flags & HDLC_FLAG_RXC_BRG:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_RXC_BRG'
        if not (self.Flags & (HDLC_FLAG_RXC_TXCPIN | HDLC_FLAG_RXC_DPLL | HDLC_FLAG_RXC_BRG)):
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_RXC_RXCPIN'
        if self.Flags & HDLC_FLAG_RXC_TXCPIN:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_RXC_TXCPIN'
        if self.Flags & HDLC_FLAG_TXC_DPLL:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_TXC_DPLL'
        if self.Flags & HDLC_FLAG_TXC_BRG:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_TXC_BRG'
        if not (self.Flags & (HDLC_FLAG_TXC_RXCPIN | HDLC_FLAG_TXC_DPLL | HDLC_FLAG_TXC_BRG)):
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_TXC_TXCPIN'
        if self.Flags & HDLC_FLAG_TXC_RXCPIN:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_TXC_RXCPIN'
        if self.Flags & HDLC_FLAG_DPLL_DIV8:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_DPLL_DIV8'
        if self.Flags & HDLC_FLAG_DPLL_DIV16:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_DPLL_DIV16'
        if self.Flags & (HDLC_FLAG_RXC_DPLL | HDLC_FLAG_TXC_DPLL) and \
           not (self.Flags & (HDLC_FLAG_DPLL_DIV8 | HDLC_FLAG_DPLL_DIV16)):
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_DPLL_DIV32'
        if self.Flags & HDLC_FLAG_HDLC_LOOPMODE:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_HDLC_LOOPMODE'
        if self.Flags & HDLC_FLAG_RXC_INV:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_RXC_INV'
        if self.Flags & HDLC_FLAG_TXC_INV:
            if len(d) > 0:
                d += ' + '
            d += 'HDLC_FLAG_TXC_INV'
        return d

    def encoding_str(self):
        if self.Encoding == HDLC_ENCODING_NRZ:
            return 'HDLC_ENCODING_NRZ'
        elif self.Encoding == HDLC_ENCODING_NRZB:
            return 'HDLC_ENCODING_NRZB'
        elif self.Encoding == HDLC_ENCODING_NRZI_MARK:
            return 'HDLC_ENCODING_NRZI_MARK'
        elif self.Encoding == HDLC_ENCODING_NRZI_SPACE:
            return 'HDLC_ENCODING_NRZI_SPACE'
        elif self.Encoding == HDLC_ENCODING_NRZI:
            return 'HDLC_ENCODING_NRZI'
        elif self.Encoding == HDLC_ENCODING_BIPHASE_MARK:
            return 'HDLC_ENCODING_BIPHASE_MARK'
        elif self.Encoding == HDLC_ENCODING_BIPHASE_SPACE:
            return 'HDLC_ENCODING_BIPHASE_SPACE'
        elif self.Encoding == HDLC_ENCODING_BIPHASE_LEVEL:
            return 'HDLC_ENCODING_BIPHASE_LEVEL'
        elif self.Encoding == HDLC_ENCODING_DIFF_BIPHASE_LEVEL:
            return 'HDLC_ENCODING_DIFF_BIPHASE_LEVEL'
        else:
            return 'unknown ' + hex(self.Encoding)

    def crc_type_str(self):
        d = ''
        if self.CrcType & HDLC_CRC_MODE == HDLC_CRC_NONE:
            d += 'HDLC_CRC_NONE'
        elif self.CrcType & HDLC_CRC_MODE == HDLC_CRC_16_CCITT:
            d += 'HDLC_CRC_16_CCITT'
        elif self.CrcType & HDLC_CRC_MODE == HDLC_CRC_32_CCITT:
            d += 'HDLC_CRC_32_CCITT'
        else:
            return 'unknown ' + hex(self.CrcType)
        if self.CrcType & HDLC_CRC_RETURN_CRCERR_FRAME:
            d += " | HDLC_CRC_RETURN_CRCERR_FRAME"
        if self.CrcType & HDLC_CRC_RETURN_CRC:
            d += " | HDLC_CRC_RETURN_CRC"
        return d

    def preamble_length_str(self):
        if self.PreambleLength == HDLC_PREAMBLE_LENGTH_8BITS:
            return 'HDLC_PREAMBLE_LENGTH_8BITS'
        elif self.PreambleLength == HDLC_PREAMBLE_LENGTH_16BITS:
            return 'HDLC_PREAMBLE_LENGTH_16BITS'
        elif self.PreambleLength == HDLC_PREAMBLE_LENGTH_32BITS:
            return 'HDLC_PREAMBLE_LENGTH_32BITS'
        elif self.PreambleLength == HDLC_PREAMBLE_LENGTH_64BITS:
            return 'HDLC_PREAMBLE_LENGTH_64BITS'
        else:
            return 'unknown ' + hex(self.PreambleLength)

    def preamble_pattern_str(self):
        if self.PreamblePattern == HDLC_PREAMBLE_PATTERN_NONE:
            return 'HDLC_PREAMBLE_PATTERN_NONE'
        elif self.PreamblePattern == HDLC_PREAMBLE_PATTERN_ZEROS:
            return 'HDLC_PREAMBLE_PATTERN_ZEROS'
        elif self.PreamblePattern == HDLC_PREAMBLE_PATTERN_FLAGS:
            return 'HDLC_PREAMBLE_PATTERN_FLAGS'
        elif self.PreamblePattern == HDLC_PREAMBLE_PATTERN_10:
            return 'HDLC_PREAMBLE_PATTERN_10'
        elif self.PreamblePattern == HDLC_PREAMBLE_PATTERN_01:
            return 'HDLC_PREAMBLE_PATTERN_01'
        elif self.PreamblePattern == HDLC_PREAMBLE_PATTERN_ONES:
            return 'HDLC_PREAMBLE_PATTERN_ONES'
        else:
            return 'unknown ' + hex(self.PreamblePattern)

    def parity_str(self):
        if self.Parity == ASYNC_PARITY_NONE:
            return 'ASYNC_PARITY_NONE'
        elif self.Parity == ASYNC_PARITY_EVEN:
            return 'ASYNC_PARITY_EVEN'
        elif self.Parity == ASYNC_PARITY_ODD:
            return 'ASYNC_PARITY_ODD'
        else:
            return 'unknown ' + hex(self.Parity)

    def __init__(self):
        self.Mode = MGSL_MODE_HDLC
        self.Loopback = False
        self.Flags = HDLC_FLAG_RXC_RXCPIN | HDLC_FLAG_TXC_TXCPIN
        self.Encoding = HDLC_ENCODING_NRZ
        self.ClockSpeed = 0
        self.Addr = 0xff
        self.CrcType = HDLC_CRC_16_CCITT
        self.PreambleLength = HDLC_PREAMBLE_LENGTH_8BITS
        self.PreamblePattern = HDLC_PREAMBLE_PATTERN_NONE
        self.DataRate = 9600
        self.DataBits = 8
        self.StopBits = 1
        self.Parity = ASYNC_PARITY_NONE
 
    def __repr__(self):
        return 'MGSL_PARAMS object at ' + hex(id(self)) + '\n' + \
            'Mode = ' + self.mode_str() + '\n' + \
            'Loopback = ' + str(self.Loopback) + '\n' + \
            'Flags = ' + self.flags_str() + '\n' + \
            'Encoding = ' + self.encoding_str() + '\n' + \
            'ClockSpeed = ' + str(self.ClockSpeed) + '\n' + \
            'Addr = ' + hex(self.Addr) + '\n' + \
            'CrcType = ' + self.crc_type_str() + '\n' + \
            'PreambleLength = ' + self.preamble_length_str() + '\n' + \
            'PreamblePattern = ' + self.preamble_pattern_str() + '\n' + \
            'DataRate = ' + str(self.DataRate) + '\n' + \
            'DataBits = ' + str(self.DataBits) + '\n' + \
            'StopBits = ' + str(self.StopBits) + '\n' + \
            'Parity = ' + self.parity_str() + '\n'

    def __str__(self):
        return self.__repr__()


class MGSL_PORT_CONFIG_EX(ctypes.Structure):
    _pack_ = 8
    _fields_ = [
        ("Size", ULONG),          # structure size in bytes
        ("BaseAddress", ULONG),   # obsolete, unused
        ("IrqLevel", ULONG),      # obsolete, unused
        ("DmaChannel", ULONG),    # obsolete, unused
        ("BusType", ULONG),       # ISA, PCI, USB
        ("BusNumber", ULONG),
        ("DeviceID", ULONG),      # serial hardware identifier
        ("MaxFrameSize", ULONG),  # max frame size in bytes (default 4096)
        ("Flags", ULONG)          # misc driver load time options
    ]

    def __init__(self):
        self.Size = ctypes.sizeof(self)
        self.BaseAddress = 0
        self.IrqLevel = 0
        self.DmaChannel = 0
        self.BusType = 0
        self.DeviceID = 0
        self.MaxFrameSize = 4096
        self.Flags = 0

    def flags_str(self):
        d = '(' + hex(self.Flags) + ')'
        interface = self.Flags & MGSL_INTERFACE_MASK
        if interface == MGSL_INTERFACE_DISABLE:
            d += ' MGSL_INTERFACE_DISABLE'
        elif interface == MGSL_INTERFACE_RS232:
            d += ' MGSL_INTERFACE_RS232'
        elif interface == MGSL_INTERFACE_V35:
            d += ' MGSL_INTERFACE_V35'
        elif interface == MGSL_INTERFACE_RS422:
            d += ' MGSL_INTERFACE_RS422'
        elif interface == MGSL_INTERFACE_RS530A:
            d += ' MGSL_INTERFACE_RS530A'
        else:
            d += ' unknown interface=' + hex(interface)
        if self.Flags & MGSL_RTS_DRIVER_CONTROL:
            d += ' MGSL_RTS_DRIVER_CONTROL'
        if self.Flags & MGSL_NO_TERMINATION:
            d += ' MGSL_NO_TERMINATION'
        return d

    def __repr__(self):
        return 'MGSL_PORT_CONFIG_EX object at ' + hex(id(self)) + '\n' + \
            'DeviceID = ' + device_id_str(self.DeviceID) + '\n' + \
            'MaxFrameSize = ' + str(self.MaxFrameSize) + '\n' + \
            'Flags = ' + self.flags_str() + '\n'

    def __str__(self):
        return self.__repr__()


# used in Flags member of MGSL_PORT_CONFIG_EX structure
MGSL_INTERFACE_MASK = 0xf
MGSL_INTERFACE_DISABLE = 0
MGSL_INTERFACE_RS232 = 1
MGSL_INTERFACE_V35 = 2
MGSL_INTERFACE_RS422 = 3
MGSL_INTERFACE_RS530A = 4
MGSL_RTS_DRIVER_CONTROL = 0x0010
MGSL_NO_TERMINATION = 0x0020

MICROGATE_VENDOR_ID = 0x13c0
SYNCLINK_DEVICE_ID = 0x0010
SYNCLINK_SCC_DEVICE_ID = 0x0020
SYNCLINK_SCA_DEVICE_ID = 0x0030
SYNCLINK_T1_DEVICE_ID = 0x0040
SYNCLINK_PCCARD_DEVICE_ID = 0x0050
SYNCLINK_MSC_DEVICE_ID = 0x0060
SYNCLINK_GT_DEVICE_ID = 0x0070
SYNCLINK_GT4_DEVICE_ID = 0x0080
SYNCLINK_AC_DEVICE_ID = 0x0090
SYNCLINK_GT2_DEVICE_ID = 0x00A0
SYNCLINK_USB_DEVICE_ID = 0x00B0
MGSL_MAX_SERIAL_NUMBER = 30


def device_id_str(device_id):
    if device_id == SYNCLINK_DEVICE_ID:
        return 'SYNCLINK_DEVICE_ID'
    elif device_id == SYNCLINK_SCC_DEVICE_ID:
        return 'SYNCLINK_SCC_DEVICE_ID'
    elif device_id == SYNCLINK_SCA_DEVICE_ID:
        return 'SYNCLINK_SCA_DEVICE_ID'
    elif device_id == SYNCLINK_T1_DEVICE_ID:
        return 'SYNCLINK_T1_DEVICE_ID'
    elif device_id == SYNCLINK_PCCARD_DEVICE_ID:
        return 'SYNCLINK_PCCARD_DEVICE_ID'
    elif device_id == SYNCLINK_MSC_DEVICE_ID:
        return 'SYNCLINK_MSC_DEVICE_ID'
    elif device_id == SYNCLINK_GT_DEVICE_ID:
        return 'SYNCLINK_GT_DEVICE_ID'
    elif device_id == SYNCLINK_GT4_DEVICE_ID:
        return 'SYNCLINK_GT4_DEVICE_ID'
    elif device_id == SYNCLINK_AC_DEVICE_ID:
        return 'SYNCLINK_AC_DEVICE_ID'
    elif device_id == SYNCLINK_GT2_DEVICE_ID:
        return 'SYNCLINK_GT2_DEVICE_ID'
    elif device_id == SYNCLINK_USB_DEVICE_ID:
        return 'SYNCLINK_USB_DEVICE_ID'
    else:
        return 'unknown device ID =' + hex(device_id)


class MGSL_ASSIGNED_RESOURCES(ctypes.Structure):
    """Assigned resources structure."""
    _pack_ = 8
    _fields_ = [
        ("BusType", ULONG),           # bus type: ISA, PCI, USB
        ("BusNumber", ULONG),         # bus index
        ("DeviceNumber", ULONG),      # device and function numbers
        ("IrqLevel", ULONG),          # interrupt request level
        ("DmaChannel", ULONG),        # DMA channel
        ("IoAddress1", ULONG),        # I/O address range 1
        ("IoAddress2", ULONG),        # I/O address range 2
        ("IoAddress3", ULONG),        # I/O address range 3
        ("MemAddress1", ULONG),       # memory address range 1
        ("MemAddress2", ULONG),       # memory address range 2
        ("MemAddress3", ULONG),       # memory address range 3
        ("DeviceId", ULONG),          # primary hardware identifier
        ("SubsystemId", ULONG),       # secondary hardware identifier
        ("SerialNumber", UCHAR * 30)   # serial number if present
    ]

    def __init__(self):
        self.BusType = 0
        self.BusNumber = 0
        self.DeviceNumber = 0
        self.IrqLevel = 0
        self.DmaChannel = 0
        self.IoAddress1 = 0
        self.IoAddress2 = 0
        self.IoAddress3 = 0
        self.MemAddress1 = 0
        self.MemAddress2 = 0
        self.MemAddress3 = 0
        self.DeviceId = 0
        self.SubsystemId = 0
        for i in range(0,30):
            self.SerialNumber[i] = 0

    def serial_number(self):
        """Return string representation of serial number."""
        sernum = ''
        for c in self.SerialNumber:
            if not c:
                break
            sernum += chr(c)
        return sernum

    def __repr__(self):
        return 'MGSL_ASSIGNED_RESOURCES object at ' + hex(id(self)) + '\n' + \
            'DeviceId = ' + device_id_str(self.DeviceId) + '\n' + \
            'SerialNumber = ' + self.serial_number() + '\n'

    def __str__(self):
        return self.__repr__()


def BUSNUM(a):
    return a & 0xffff


def DEVNUM(a):
    return a >> 16


def BUSDEV(a, b):
    return a + (b << 16)


class GPIO_DESC(ctypes.Structure):
    """General Purpose I/O Descriptor"""
    _pack_ = 8
    _fields_ = [
        ("state", ULONG),     # signal states
        ("smask", ULONG),     # state mask
        ("dir", ULONG),       # signal directions
        ("dmask", ULONG)      # direction mask
    ]

    def __init__(self):
        self.state = 0
        self.smask = 0
        self.dir = 0
        self.dmask = 0

    def __repr__(self):
        return 'GPIO_DESC object at ' + hex(id(self)) + '\n' + \
            'state = ' + hex(self.state) + '\n' + \
            'smask = ' + hex(self.smask) + '\n' + \
            'dir = ' + hex(self.dir) + '\n' + \
            'dmask = ' + hex(self.dmask) + '\n'

    def __str__(self):
        return self.__repr__()


MGSL_INVALID_HANDLE = -1
INT = ctypes.c_ulong

#
# Option IDs used with MgslSetOption/MgslGetOption
#
MGSL_OPT_RX_DISCARD_TOO_LARGE = 1
MGSL_OPT_UNDERRUN_RETRY_LIMIT = 2
MGSL_OPT_ENABLE_LOCALLOOPBACK = 3
MGSL_OPT_ENABLE_REMOTELOOPBACK = 4
MGSL_OPT_JCR = 5
MGSL_OPT_INTERFACE = 6
MGSL_OPT_RTS_DRIVER_CONTROL = 7
MGSL_OPT_RX_ERROR_MASK = 8
MGSL_OPT_CLOCK_SWITCH = 9
MGSL_OPT_CLOCK_BASE_FREQ = 10
MGSL_OPT_HALF_DUPLEX = 11
MGSL_OPT_MSB_FIRST = 12
MGSL_OPT_RX_COUNT = 13
MGSL_OPT_TX_COUNT = 14
MGSL_OPT_CUSTOM = 15
MGSL_OPT_RX_POLL = 16
MGSL_OPT_TX_POLL = 17
MGSL_OPT_NO_TERMINATION = 18
MGSL_OPT_TDM = 19
MGSL_OPT_AUXCLK_ENABLE = 20
MGSL_OPT_UNDERRUN_COUNT = 21
MGSL_OPT_TX_IDLE_COUNT = 22
MGSL_OPT_DPLL_RESET = 23
MGSL_OPT_RS422_OE = 24

#
# Returned status values for MgslReceive
#
RxStatus_OK = 0
RxStatus_CrcError = 1
RxStatus_FifoOverrun = 2
RxStatus_ShortFrame = 3
RxStatus_Abort = 4
RxStatus_BufferOverrun = 5
RxStatus_Cancel = 6
RxStatus_BufferTooSmall = 7

#
# Event bit flags for use with MgslWaitEvent
#
MgslEvent_DsrActive = 0x0001
MgslEvent_DsrInactive = 0x0002
MgslEvent_Dsr = 0x0003
MgslEvent_CtsActive = 0x0004
MgslEvent_CtsInactive = 0x0008
MgslEvent_Cts = 0x000c
MgslEvent_DcdActive = 0x0010
MgslEvent_DcdInactive = 0x0020
MgslEvent_Dcd = 0x0030
MgslEvent_RiActive = 0x0040
MgslEvent_RiInactive = 0x0080
MgslEvent_Ri = 0x00c0
MgslEvent_ExitHuntMode = 0x0100
MgslEvent_IdleReceived = 0x0200


class MGSL_PORT(ctypes.Structure):
    """Structure used to enumerate ports."""
    _pack_ = 8
    _fields_ = [
        ("PortID", ULONG),      # numerical port ID
        ("DeviceID", ULONG),    # device ID
        ("BusType", ULONG),     # obsolete, not used
        ("DeviceName", UCHAR * 25)   # textual device (port) name
    ]

    def __init__(self):
        self.PortID = 0
        self.DeviceID = 0
        self.BusType = 0
        for i in range(0,25):
            self.DeviceName[i] = 0

    def port_name(self):
        """Convert fixed length byte array to string."""
        name = ''
        for c in self.DeviceName:
            if not c:
                break
            name += chr(c)
        return name

    def __repr__(self):
        return 'MGSL_PORT object at ' + hex(id(self)) + '\n' + \
            'PortID = ' + hex(self.PortID) + '\n' + \
            'DeviceID = ' + device_id_str(self.DeviceID) + '\n' + \
            'DeviceName = ' + self.port_name() + '\n'

    def __str__(self):
        return self.__repr__()


SerialSignal_DCD = 0x01  # Data Carrier Detect (output)
SerialSignal_TXD = 0x02  # Transmit Data (output)
SerialSignal_RI = 0x04   # Ring Indicator (input)
SerialSignal_RXD = 0x08  # Receive Data (input)
SerialSignal_CTS = 0x10  # Clear to Send (input)
SerialSignal_RTS = 0x20  # Request to Send (output)
SerialSignal_DSR = 0x40  # Data Set Ready (input)
SerialSignal_DTR = 0x80  # Data Terminal Ready (output)


#
# Device Access Functions
#

# ULONG __stdcall MgslOpen(ULONG PortID, PHANDLE pHandle);
c_MgslOpen = mghdlc_dll.MgslOpen
c_MgslOpen.argtypes = [ULONG, LPVOID]
c_MgslOpen.restype = ULONG

def MgslOpen(port_id: int, port: HANDLE) -> int:
    """Open handle to port identified by integer port ID."""
    return c_MgslOpen(ULONG(port_id), ctypes.byref(port))


# ULONG __stdcall MgslOpenByName(char *PortName, PHANDLE pHandle);
c_MgslOpenByName = mghdlc_dll.MgslOpenByName
c_MgslOpenByName.argtypes = [LPCSTR, LPVOID]
c_MgslOpenByName.restype = ULONG

def MgslOpenByName(name: str, port: HANDLE) -> int:
    """Open handle to port identified by name."""
    return c_MgslOpenByName(LPCSTR(name.encode('utf-8')), ctypes.byref(port))


# ULONG __stdcall MgslClose(HANDLE hDevice);
c_MgslClose = mghdlc_dll.MgslClose
c_MgslClose.argtypes = [LPVOID]
c_MgslClose.restype = ULONG

def MgslClose(port: HANDLE) -> int:
    """Close port identified by open handle."""
    rc = c_MgslClose(port)
    if rc == 0:
        port.value = MGSL_INVALID_HANDLE
    return rc


#
# Device Configuration Functions
#

# ULONG __stdcall MgslSetParams(HANDLE hDevice, PMGSL_PARAMS pParams);
c_MgslSetParams = mghdlc_dll.MgslSetParams
c_MgslSetParams.argtypes = [LPVOID, LPVOID]
c_MgslSetParams.restype = ULONG

def MgslSetParams(port: HANDLE, params: MGSL_PARAMS) -> int:
    """Set configuration parameters for open port."""
    return c_MgslSetParams(port, ctypes.byref(params))


# ULONG __stdcall MgslGetParams(HANDLE hDevice, PMGSL_PARAMS pParams);
c_MgslGetParams = mghdlc_dll.MgslGetParams
c_MgslGetParams.argtypes = [LPVOID, LPVOID]
c_MgslGetParams.restype = ULONG

def MgslGetParams(port: HANDLE, params: MGSL_PARAMS) -> int:
    """Get configuration parameters for open port."""
    return c_MgslGetParams(port, ctypes.byref(params))


# ULONG __stdcall MgslSetOption(HANDLE hDevice, UINT option_id, UINT value);
c_MgslSetOption = mghdlc_dll.MgslSetOption
c_MgslSetOption.argtypes = [HANDLE, wintypes.UINT, wintypes.UINT]
c_MgslSetOption.restype = ULONG

def MgslSetOption(port: HANDLE, option_id: int, option_value: int) -> int:
    """Set option value for specified option ID."""
    return c_MgslSetOption(port, wintypes.UINT(option_id),
                           wintypes.UINT(option_value))


# ULONG __stdcall MgslGetOption(HANDLE hDevice, UINT option_id, UINT *value);
c_MgslGetOption = mghdlc_dll.MgslGetOption
c_MgslGetOption.argtypes = [HANDLE, wintypes.UINT, LPVOID]
c_MgslGetOption.restype = ULONG

def MgslGetOption(port: HANDLE, option_id: int, option_value: INT) -> int:
    """Get option value for specified option ID."""
    return c_MgslGetOption(port, wintypes.UINT(option_id),
                           ctypes.byref(option_value))


# ULONG __stdcall MgslGetPortConfigEx(ULONG PortID, PMGSL_PORT_CONFIG_EX pConfig);
c_MgslGetPortConfigEx = mghdlc_dll.MgslGetPortConfigEx
c_MgslGetPortConfigEx.argtypes = [ULONG, LPVOID]
c_MgslGetPortConfigEx.restype = ULONG

def MgslGetPortConfigEx(port_id: int, port_config: MGSL_PORT_CONFIG_EX) -> int:
    """Get driver load time options for port."""
    port_config.Size = ctypes.sizeof(port_config)
    return c_MgslGetPortConfigEx(ULONG(port_id), ctypes.byref(port_config))


# ULONG __stdcall MgslSetPortConfigEx(ULONG PortID, PMGSL_PORT_CONFIG_EX pConfig);
c_MgslSetPortConfigEx = mghdlc_dll.MgslSetPortConfigEx
c_MgslSetPortConfigEx.argtypes = [ULONG, LPVOID]
c_MgslSetPortConfigEx.restype = ULONG

def MgslSetPortConfigEx(port_id: int, port_config: MGSL_PORT_CONFIG_EX) -> int:
    """Set driver load time options for port."""
    port_config.Size = ctypes.sizeof(port_config)
    return c_MgslSetPortConfigEx(ULONG(port_id), ctypes.byref(port_config))


#
# Device Control/Status Functions
#

def serial_signals_str(signals: int) -> str:
    """Return string representation of serial signal value."""
    d = '(' + hex(signals) + ')'
    if signals & SerialSignal_DTR:
        d += ' DTR'
    if signals & SerialSignal_DSR:
        d += ' DSR'
    if signals & SerialSignal_RTS:
        d += ' RTS'
    if signals & SerialSignal_CTS:
        d += ' CTS'
    if signals & SerialSignal_DCD:
        d += ' DCD'
    if signals & SerialSignal_RI:
        d += ' RI'
    if signals & SerialSignal_TXD:
        d += ' TXD'
    if signals & SerialSignal_RXD:
        d += ' RXD'
    return d


# ULONG __stdcall MgslSetSerialSignals(HANDLE hDevice, UCHAR NewSignals);
c_MgslSetSerialSignals = mghdlc_dll.MgslSetSerialSignals
c_MgslSetSerialSignals.argtypes = [LPVOID, UCHAR]
c_MgslSetSerialSignals.restype = ULONG

def MgslSetSerialSignals(port: HANDLE, signals: int) -> int:
    """Set control output states for open port."""
    return c_MgslSetSerialSignals(port, UCHAR(signals))


# ULONG __stdcall MgslGetSerialSignals(HANDLE hDevice, PUCHAR pReturnedSignals);
c_MgslGetSerialSignals = mghdlc_dll.MgslGetSerialSignals
c_MgslGetSerialSignals.argtypes = [LPVOID, LPVOID]
c_MgslGetSerialSignals.restype = ULONG

def MgslGetSerialSignals(port: HANDLE, signals: INT) -> int:
    """Get control and status signal states for open port."""
    local_signals = UCHAR(signals.value)
    rc = c_MgslGetSerialSignals(port, ctypes.byref(local_signals))
    signals.value = local_signals.value & 0xff
    return rc


# ULONG __stdcall MgslWaitEvent(HANDLE hDevice, ULONG EventMask,
# 			PULONG pEvents, LPOVERLAPPED pOverlapped);
c_MgslWaitEvent = mghdlc_dll.MgslWaitEvent
c_MgslWaitEvent.argtypes = [LPVOID, ULONG, LPVOID, LPVOID]
c_MgslWaitEvent.restype = ULONG

def MgslWaitEvent(port: HANDLE, event_mask: int, events: INT, ol: OVERLAPPED) -> int:
    """Wait for serial port event."""
    return c_MgslWaitEvent(port, ULONG(event_mask), ctypes.byref(events), ctypes.byref(ol))


# ULONG __stdcall MgslCancelWaitEvent(HANDLE hDevice);
c_MgslCancelWaitEvent = mghdlc_dll.MgslCancelWaitEvent
c_MgslCancelWaitEvent.argtypes = [LPVOID]
c_MgslCancelWaitEvent.restype = ULONG

def MgslCancelWaitEvent(port: HANDLE) -> int:
    """Cancel wait for serial port event."""
    return c_MgslCancelWaitEvent(port)


#
# General Purpose I/O Control/Status Functions
#

# ULONG __stdcall MgslSetGpio(HANDLE hDevice, GPIO_DESC *gpio);
c_MgslSetGpio = mghdlc_dll.MgslSetGpio
c_MgslSetGpio.argtypes = [LPVOID, LPVOID]
c_MgslSetGpio.restype = ULONG

def MgslSetGpio(port: HANDLE, gpio: GPIO_DESC) -> int:
    """Set GPIO states."""
    return c_MgslSetGpio(port, ctypes.byref(gpio))


# ULONG __stdcall MgslGetGpio( HANDLE hDevice, GPIO_DESC *gpio );
c_MgslGetGpio = mghdlc_dll.MgslGetGpio
c_MgslGetGpio.argtypes = [LPVOID, LPVOID]
c_MgslGetGpio.restype = ULONG

def MgslGetGpio(port: HANDLE, gpio: GPIO_DESC) -> int:
    """Get GPIO states."""
    return c_MgslGetGpio(port, ctypes.byref(gpio))


# ULONG __stdcall MgslWaitGpio(HANDLE hDevice, GPIO_DESC *gpio, LPOVERLAPPED ol);
c_MgslWaitGpio = mghdlc_dll.MgslWaitGpio
c_MgslWaitGpio.argtypes = [LPVOID, LPVOID, LPVOID]
c_MgslWaitGpio.restype = ULONG

def MgslWaitGpio(port: HANDLE, gpio: GPIO_DESC, ol: OVERLAPPED) -> int:
    """Wait for general purpose I/O event."""
    return c_MgslWaitGpio(port, ctypes.byref(gpio), ctypes.byref(ol))


# ULONG __stdcall MgslCancelWaitGpio(HANDLE hDevice);
c_MgslCancelWaitGpio = mghdlc_dll.MgslCancelWaitGpio
c_MgslCancelWaitGpio.argtypes = [LPVOID]
c_MgslCancelWaitGpio.restype = ULONG

def MgslCancelWaitGpio(port: HANDLE) -> int:
    """Cancel wait for general purpose I/O event."""
    return c_MgslCancelWaitGpio(port)


#
# Data Communication Functions
#

# ULONG __stdcall MgslCancelTransmit(HANDLE hDevice);
c_MgslCancelTransmit = mghdlc_dll.MgslCancelTransmit
c_MgslCancelTransmit.argtypes = [HANDLE]
c_MgslCancelTransmit.restype = ULONG

def MgslCancelTransmit(port: HANDLE) -> int:
    """Cancel blocked write."""
    return c_MgslCancelTransmit(port)


# ULONG __stdcall MgslEnableTransmitter(HANDLE hDevice, BOOL EnableFlag);
c_MgslEnableTransmitter = mghdlc_dll.MgslEnableTransmitter
c_MgslEnableTransmitter.argtypes = [HANDLE, BOOL]
c_MgslEnableTransmitter.restype = ULONG

def MgslEnableTransmitter(port: HANDLE, enable: int) -> int:
    """Enable or disable transmitter for open port."""
    return c_MgslEnableTransmitter(port, BOOL(enable))


# ULONG __stdcall MgslSetIdleMode(HANDLE hDevice, ULONG IdleMode);
c_MgslSetIdleMode = mghdlc_dll.MgslSetIdleMode
c_MgslSetIdleMode.argtypes = [HANDLE, ULONG]
c_MgslSetIdleMode.restype = ULONG

def MgslSetIdleMode(port: HANDLE, mode: int) -> int:
    """Select transmit idle mode or sync pattern (monosync/bisync)."""
    return c_MgslSetIdleMode(port, mode)


# int __stdcall MgslWrite(HANDLE hDevice, unsigned char *buf, int size);
c_MgslWrite = mghdlc_dll.MgslWrite
c_MgslWrite.argtypes = [HANDLE, LPCSTR, ctypes.c_int]
c_MgslWrite.restype = ctypes.c_int

def MgslWrite(port: HANDLE, buf: bytearray, size: int) -> int:
    """Send data on open port."""
    char_array = ctypes.c_char * len(buf)
    if size > len(buf):
        size = len(buf)
    return c_MgslWrite(port, char_array.from_buffer(buf), size)


# int __stdcall MgslWaitAllSent(HANDLE hDevice);
c_MgslWaitAllSent = mghdlc_dll.MgslWaitAllSent
c_MgslWaitAllSent.argtypes = [HANDLE]
c_MgslWaitAllSent.restype = ctypes.c_int

def MgslWaitAllSent(port: HANDLE) -> int:
    """Wait for all send data to complete on port."""
    return c_MgslWaitAllSent(port)


# ULONG __stdcall MgslCancelReceive(HANDLE hDevice);
c_MgslCancelReceive = mghdlc_dll.MgslCancelReceive
c_MgslCancelReceive.argtypes = [LPVOID]
c_MgslCancelReceive.restype = ULONG

def MgslCancelReceive(port: HANDLE) -> int:
    """Cancel blocked read."""
    return c_MgslCancelReceive(port)


# ULONG __stdcall MgslEnableReceiver(HANDLE hDevice, BOOL EnableFlag);
c_MgslEnableReceiver = mghdlc_dll.MgslEnableReceiver
c_MgslEnableReceiver.argtypes = [HANDLE, BOOL]
c_MgslEnableReceiver.restype = ULONG

def MgslEnableReceiver(port: HANDLE, enable: int) -> int:
    return c_MgslEnableReceiver(port, enable)


# int __stdcall MgslRead(HANDLE hDevice, unsigned char *buf, int size);
c_MgslRead = mghdlc_dll.MgslRead
c_MgslRead.argtypes = [HANDLE, LPCSTR, ctypes.c_int]
c_MgslRead.restype = ctypes.c_int

def MgslRead(port: HANDLE, buf: bytearray, size: int) -> int:
    """Receive data from open port."""
    char_array = ctypes.c_char * len(buf)
    if size > len(buf):
        size = len(buf)
    return c_MgslRead(port, char_array.from_buffer(buf), size)


# int __stdcall MgslReadWithStatus(HANDLE hDevice, unsigned char *buf,
#                   int size, int *status);
c_MgslReadWithStatus = mghdlc_dll.MgslReadWithStatus
c_MgslReadWithStatus.argtypes = [HANDLE, LPCSTR, ctypes.c_int, LPVOID]
c_MgslReadWithStatus.restype = ctypes.c_int

def MgslReadWithStatus(port: HANDLE, buf: bytearray,
                       size: int, status: INT) -> int:
    char_array = ctypes.c_char * len(buf)
    if size > len(buf):
        size = len(buf)
    return c_MgslReadWithStatus(port, char_array.from_buffer(buf),
                                size, ctypes.byref(status))


#
# Misc Functions
#

# ULONG __stdcall MgslGetAssignedResources(HANDLE hDevice,
#                     PMGSL_ASSIGNED_RESOURCES pRes);
c_MgslGetAssignedResources = mghdlc_dll.MgslGetAssignedResources
c_MgslGetAssignedResources.argtypes = [HANDLE, LPVOID]
c_MgslGetAssignedResources.restype = ULONG

def MgslGetAssignedResources(port: HANDLE, port_res: MGSL_ASSIGNED_RESOURCES) -> int:
    """Get system assigned resources for port."""
    return c_MgslGetAssignedResources(port, ctypes.byref(port_res))


# ULONG __stdcall MgslEnumeratePorts(PMGSL_PORT pPorts,
#                     ULONG BufferSize, PULONG pPortCount);
c_MgslEnumeratePorts = mghdlc_dll.MgslEnumeratePorts
c_MgslEnumeratePorts.argtypes = [LPVOID, ULONG, LPVOID]
c_MgslEnumeratePorts.restype = ULONG

def MgslEnumeratePorts(ports: []) -> int:
    """Enumerate configured ports. Listed ports may not be plugged in."""
    local_ports = (MGSL_PORT * MGSL_MAX_PORTS)()
    count = ULONG()
    rc = c_MgslEnumeratePorts(ctypes.pointer(local_ports),
                              ctypes.sizeof(local_ports), ctypes.byref(count))
    ports.clear()
    for i in range(0, count.value):
        ports.append(local_ports[i])
    return rc


def MgslWaitEventTimed(port: HANDLE, event_mask: int, events: INT, timeout: int) -> int:
    """
    Wait for serial port event.
    event_mask = one or more desired events (bitmask)
    events     = if success, contains completion state/events
    timeout    = timeout in milliseconds
    returns 0 on success, WAIT_TIMEOUT if timeout or error code
    """

    # create Win32 overlapped structure and event to monitor wait progress
    ol = OVERLAPPED()
    ol.hEvent = CreateEvent(True, False)
    if ol.hEvent == 0:
        return ERROR_GEN_FAILURE

    # MgslWaitEvent returns immediately with code:
    # 0 = in desired state (no wait needed)
    # ERROR_IO_PENDING = wait for desired state (monitor event)
    # other = error, request failed
    rc = MgslWaitEvent(port, event_mask, events, ol)
    if rc == ERROR_IO_PENDING:
        # wait for desired state
        rc = WaitForSingleObject(ol.hEvent, timeout)
        if rc == WAIT_TIMEOUT:
            # timeout waiting for desired state
            # cancel wait and wait for cancel to complete
            MgslCancelWaitEvent(port)
            WaitForSingleObject(ol.hEvent, INFINITE)

    CloseHandle(ol.hEvent)
    return rc


def MgslWaitGpioTimed(port: HANDLE, gpio: GPIO_DESC, timeout: int) -> int:
    """
    Wait for general purpose I/O event.
    gpio = on entry contains desired states
           on success contains completing states
    timeout    = timeout in milliseconds
    returns 0 on success, WAIT_TIMEOUT if timeout or error code
    """

    # create Win32 overlapped structure and event to monitor wait progress
    ol = OVERLAPPED()
    ol.hEvent = CreateEvent(True, False)
    if ol.hEvent == 0:
        return ERROR_GEN_FAILURE

    # MgslGpioEvent returns immediately with code:
    # 0 = in desired state (no wait needed)
    # ERROR_IO_PENDING = wait for desired state (monitor event)
    # other = error, request failed
    rc = MgslWaitGpio(port, gpio, ol)
    if rc == ERROR_IO_PENDING:
        # wait for desired state
        rc = WaitForSingleObject(ol.hEvent, timeout)
        if rc == WAIT_TIMEOUT:
            # timeout waiting for desired state
            # cancel wait and wait for cancel to complete
            MgslCancelWaitGpio(port)
            WaitForSingleObject(ol.hEvent, INFINITE)

    CloseHandle(ol.hEvent)
    return rc


#
# Object oriented API
#

import os.path

class Port():
    """Object representing a serial communications port."""

    @classmethod
    def enumerate(cls):
        """Return list of port names."""
        ports = []
        names = []
        MgslEnumeratePorts(ports)
        for p in ports:
            handle = HANDLE()
            error = MgslOpenByName(p.port_name(), handle)
            if error == ERROR_BAD_DEVICE:
                continue
            if not error:
                MgslClose(handle)
            names.append(p.port_name())
        return names

    # class constants

    # serial signal bit flags
    DCD = SerialSignal_DCD  # Data Carrier Detect (output)
    TXD = SerialSignal_TXD  # Transmit Data (output)
    RI = SerialSignal_RI  # Ring Indicator (input)
    RXD = SerialSignal_RXD  # Receive Data (input)
    CTS = SerialSignal_CTS  # Clear to Send (input)
    RTS = SerialSignal_RTS  # Request to Send (output)
    DSR = SerialSignal_DSR  # Data Set Ready (input)
    DTR = SerialSignal_DTR  # Data Terminal Ready (output)

    # Event bit flags for use with wait_event
    DSR_ON = MgslEvent_DsrActive
    DSR_OFF = MgslEvent_DsrInactive
    CTS_ON = MgslEvent_CtsActive
    CTS_OFF = MgslEvent_CtsInactive
    DCD_ON = MgslEvent_DcdActive
    DCD_OFF = MgslEvent_DcdInactive
    RI_ON = MgslEvent_RiActive
    RI_OFF = MgslEvent_RiInactive
    RECEIVE_ACTIVE = MgslEvent_ExitHuntMode
    RECEIVE_IDLE = MgslEvent_IdleReceived

    # serial protocols
    ASYNC = MGSL_MODE_ASYNC
    HDLC = MGSL_MODE_HDLC
    MONOSYNC = MGSL_MODE_MONOSYNC
    BISYNC = MGSL_MODE_BISYNC
    RAW = MGSL_MODE_EXTERNALSYNC
    TDM = MGSL_MODE_TDM

    # serial encodings
    NRZ = HDLC_ENCODING_NRZ
    NRZB = HDLC_ENCODING_NRZB
    NRZI_MARK = HDLC_ENCODING_NRZI_MARK
    NRZI_SPACE = HDLC_ENCODING_NRZI_SPACE
    NRZI = NRZI_SPACE
    FM1 = HDLC_ENCODING_BIPHASE_MARK
    FM0 = HDLC_ENCODING_BIPHASE_SPACE
    MANCHESTER = HDLC_ENCODING_BIPHASE_LEVEL
    DIFF_BIPHASE_LEVEL = HDLC_ENCODING_DIFF_BIPHASE_LEVEL

    # clock sources
    TXC_INPUT = 1
    RXC_INPUT = 2
    INTERNAL = 3
    RECOVERED = 4

    # used with any setting requiring 0
    OFF = 0

    # asynchronous parity
    EVEN = 1
    ODD = 2

    # HDLC/SDLC frame check
    CRC16 = 1
    CRC32 = 2

    # serial interface selection
    RS232 = 1
    V35 = 2
    RS422 = 3
    RS530A = 4

    def name_to_id(self, name:str) -> int:
        """Convert string name to integer port identifier."""
        ports = []
        MgslEnumeratePorts(ports)
        for p in ports:
            if p.port_name() == name.upper():
                return p.PortID
        return None

    def events_str(self, events):
        s = ''
        if events & Port.DSR_ON:
            s += 'DSR_ON '
        elif events & Port.DSR_OFF:
            s += 'DSR_OFF '
        if events & Port.CTS_ON:
            s += 'CTS_ON '
        elif events & Port.CTS_OFF:
            s += 'CTS_OFF '
        if events & Port.DCD_ON:
            s += 'DCD_ON '
        elif events & Port.DCD_OFF:
            s += 'DCD_OFF '
        if events & Port.RI_ON:
            s += 'RI_ON '
        elif events & Port.RI_OFF:
            s += 'RI_OFF '
        if events & Port.RECEIVE_ACTIVE:
            s += 'RECEIVE_ACTIVE '
        if events & Port.RECEIVE_IDLE:
            s += 'RECEIVE_IDLE'
        return s

    class Defaults():
        """Persistent default options."""

        def __init__(self):
            self.max_data_size = 4096
            self.interface = Port.OFF
            self.rts_output_enable = False
            self.termination = True

        def interface_str(self):
            if self.interface == Port.OFF:
                return 'OFF'
            elif self.interface == Port.RS232:
                return 'RS232'
            elif self.interface == Port.V35:
                return 'V35'
            elif self.interface == Port.RS422:
                return 'RS422'
            elif self.interface == Port.RS530A:
                return 'RS530A'
            else:
                return 'Unknown=' + str(self.interface)

        def __repr__(self):
            return 'Defaults object at ' + hex(id(self)) + '\n' + \
                'max_data_size = ' + str(self.max_data_size) + '\n' + \
                'interface = ' + self.interface_str() + '\n' + \
                'rts_output_enable = ' + str(self.rts_output_enable) + '\n' + \
                'termination = ' + str(self.termination) + '\n'

        def __str__(self):
            return self.__repr__()

    class Settings():
        """Port settings."""

        def protocol_str(self):
            if self.protocol == Port.ASYNC:
                return 'ASYNC'
            elif self.protocol == Port.HDLC:
                return 'HDLC'
            elif self.protocol == Port.MONOSYNC:
                return 'MONOSYNC'
            elif self.protocol == Port.BISYNC:
                return 'BISYNC'
            elif self.protocol == Port.RAW:
                return 'RAW'
            elif self.protocol == Port.TDM:
                return 'TDM'
            else:
                return 'unknown protocol = ' + hex(self.protocol)

        def encoding_str(self):
            if self.encoding == Port.NRZ:
                return 'NRZ'
            elif self.encoding == Port.NRZB:
                return 'NRZB'
            elif self.encoding == Port.NRZI_MARK:
                return 'NRZI_MARK'
            elif self.encoding == Port.NRZI:
                return 'NRZI'
            elif self.encoding == Port.FM1:
                return 'FM1'
            elif self.encoding == Port.FM0:
                return 'FM0'
            elif self.encoding == Port.MANCHESTER:
                return 'MANCHESTER'
            elif self.encoding == Port.DIFF_BIPHASE_LEVEL:
                return 'DIFF_BIPHASE_LEVEL'
            else:
                return 'unknown ' + hex(self.encoding)

        def clock_str(self, clock):
            if clock == Port.TXC_INPUT:
                return 'TXC_INPUT'
            elif clock == Port.RXC_INPUT:
                return 'RXC_INPUT'
            elif clock == Port.INTERNAL:
                return 'INTERNAL'
            elif clock == Port.RECOVERED:
                return 'RECOVERED'
            else:
                return 'unknown ' + str(clock)

        def crc_str(self):
            if self.crc == Port.OFF:
                return 'OFF'
            elif self.crc == Port.CRC16:
                return 'CRC16'
            elif self.crc == Port.CRC32:
                return 'CRC32'
            else:
                return 'unknown ' + hex(self.crc)

        def parity_str(self):
            if self.async_parity == Port.OFF:
                return 'OFF'
            elif self.async_parity == Port.EVEN:
                return 'EVEN'
            elif self.async_parity == Port.ODD:
                return 'ODD'
            else:
                return 'unknown ' + hex(self.async_parity)

        def __init__(self):
            self.protocol = Port.HDLC
            self.encoding = Port.NRZ
            self.msb_first = False
            self.internal_loopback = False

            self.crc = Port.CRC16
            self.discard_data_with_error = True
            self.discard_received_crc = True

            self.hdlc_address_filter = 0xff

            self.transmit_preamble_pattern = 0x7e
            self.transmit_preamble_bits = 0

            self.recovered_clock_divisor = 16
            self.internal_clock_rate = 0

            self.transmit_clock = Port.TXC_INPUT
            self.transmit_clock_invert = False
            self.receive_clock = Port.RXC_INPUT
            self.receive_clock_invert = False

            self.auto_cts = False
            self.auto_dcd = False
            self.auto_rts = False

            self.async_data_rate = 9600
            self.async_data_bits = 8
            self.async_stop_bits = 1
            self.async_parity = Port.OFF

            self.tdm_sync_delay = 0
            self.tdm_sync_frame = False
            self.tdm_sync_short = False
            self.tdm_sync_invert = False
            self.tdm_frame_count = 1
            self.tdm_slot_count = 2
            self.tdm_slot_bits = 8

            self.sync_pattern = 0

        def __repr__(self):
            return 'Settings object at ' + hex(id(self)) + '\n' + \
                'protocol = ' + self.protocol_str() + '\n' + \
                'encoding = ' + self.encoding_str() + '\n' + \
                'msb_first = ' + str(self.msb_first) + '\n' + \
                'crc = ' + self.crc_str() + '\n' + \
                'discard_data_with_error = ' + str(self.discard_data_with_error) + '\n' + \
                'discard_received_crc = ' + str(self.discard_received_crc) + '\n' + \
                'hdlc_address_filter = ' + hex(self.hdlc_address_filter) + '\n' + \
                'auto_rts = ' + str(self.auto_rts) + '\n' + \
                'auto_cts = ' + str(self.auto_cts) + '\n' + \
                'auto_dcd = ' + str(self.auto_dcd) + '\n' + \
                'internal_clock_rate = ' + str(self.internal_clock_rate) + '\n' + \
                'transmit_clock = ' + self.clock_str(self.transmit_clock) + '\n' + \
                'transmit_clock_invert = ' + str(self.transmit_clock_invert) + '\n' + \
                'receive_clock = ' + self.clock_str(self.receive_clock) + '\n' + \
                'receive_clock_invert = ' + str(self.receive_clock_invert) + '\n' + \
                'transmit_preamble_pattern = ' + hex(self.transmit_preamble_pattern) + '\n' + \
                'transmit_preamble_bits = ' + str(self.transmit_preamble_bits) + '\n' + \
                'async_data_rate = ' + str(self.async_data_rate) + '\n' + \
                'async_data_bits = ' + str(self.async_data_bits) + '\n' + \
                'async_stop_bits = ' + str(self.async_stop_bits) + '\n' + \
                'async_parity = ' + self.parity_str() + '\n' + \
                'sync_pattern = ' + hex(self.sync_pattern) + '\n' + \
                'tdm_sync_frame = ' + str(self.tdm_sync_frame) + '\n' + \
                'tdm_sync_delay = ' + str(self.tdm_sync_delay) + '\n' + \
                'tdm_sync_short = ' + str(self.tdm_sync_short) + '\n' + \
                'tdm_sync_invert = ' + str(self.tdm_sync_invert) + '\n' + \
                'tdm_frame_count = ' + str(self.tdm_frame_count) + '\n' + \
                'tdm_slot_count = ' + str(self.tdm_slot_count) + '\n' + \
                'tdm_slot_bits = ' + str(self.tdm_slot_bits) + '\n' + \
                'internal_loopback = ' + str(self.internal_loopback) + '\n'

        def __str__(self):
            return self.__repr__()


    class GPIO():

        def __init__(self, port, bit):
            self._port = port
            self._bit = bit

        @property
        def state(self) -> bool:
            gpio = self._port.get_gpio()
            if gpio & (1 << self._bit):
                return True
            else:
                return False

        @state.setter
        def state(self, x:bool):
            mask = (1 << self._bit)
            if x:
                value = mask
            else:
                value = 0
            self._port.set_gpio(mask, value)

        @property
        def output(self) -> bool:
            gpio = self._port.get_gpio_direction()
            if gpio & (1 << self._bit):
                return True
            else:
                return False

        @output.setter
        def output(self, x:bool):
            mask = (1 << self._bit)
            if x:
                value = mask
            else:
                value = 0
            self._port.set_gpio_direction(mask, value)

    def is_open(self):
        """Return open state for port."""
        return self._open

    def open(self):
        """Open port."""
        if self.is_open():
            return
        error = MgslOpenByName(self.name, self._handle)
        if error:
            if error == ERROR_BAD_DEVICE:
                raise FileNotFoundError
            elif error == ERROR_ACCESS_DENIED or \
                 error == ERROR_DEVICE_IN_USE or \
                 error == ERROR_OPEN_FAILED:
                raise PermissionError
            else:
                raise OSError
        self._open = True
        self.get_defaults()
        self.get_settings()
        self.blocked_io = True
        self.ignore_read_errors = True
        self._reset_pio()

    def close(self):
        """Close port."""
        if self.is_open():
            self._reset_pio()
            MgslClose(self._handle)
            self._open = False

    def write(self, buf:bytearray) -> bool:
        """Write send data to port."""
        bytes_sent = MgslWrite(self._handle, buf, len(buf))
        if bytes_sent == len(buf):
            return True
        return False

    def flush(self) -> bool:
        """Wait for pending send data to complete."""
        error = MgslWaitAllSent(self._handle)
        if error:
            return False
        return True

    def read(self, size:int=None) -> bytearray:
        """Read received data from port."""
        if size == None or \
            self._default_read_size == self._defaults.max_data_size:
            # size not specified or protocol framing sets size
            size = self._default_read_size
        elif self._default_read_size == 1:
            assert size > 0 and size <= self._defaults.max_data_size, \
                str.format("size must be 1 to max_data_size")
        buf = bytearray(size)
        count = MgslRead(self._handle, buf, len(buf))
        if count:
            return buf[:count]
        return None

    def read_with_status(self, size:int) -> (bytearray, int):
        """Read received data from port with status."""
        buf = bytearray(size)
        status = INT()
        status.value = -1
        count = MgslReadWithStatus(self._handle, buf, len(buf), status)
        if status.value != -1:
            return (buf[:count], status.value)
        return None

    def disable_receiver(self):
        """Disable receiver."""
        MgslEnableReceiver(self._handle, 0)

    def enable_receiver(self):
        """Enable receiver."""
        MgslEnableReceiver(self._handle, 1)

    def force_idle_receiver(self):
        """Force receiver to idle state (hunt mode)."""
        MgslEnableReceiver(self._handle, 2)

    def disable_transmitter(self):
        """Disable transmitter."""
        MgslEnableTransmitter(self._handle, 0)

    def enable_transmitter(self):
        """Enable transmitter."""
        MgslEnableTransmitter(self._handle, 1)

    def wait(self, mask:int, timeout:int=INFINITE) -> int:
        """
        Wait for specified events.
        mask = bitmask of events to wait for
        timeout = optional wait timeout in milliseconds
        returns bitmask of events that occurred or 0 if timeout
        If timeout is not specified, this call waits forever.
        """
        if not mask:
            return 0
        events = INT()
        error = MgslWaitEventTimed(self._handle, mask, events, timeout)
        if error:
            return 0
        return events.value

    def cancel_read(self):
        """Cancel blocked read() call."""
        MgslCancelReceive(self._handle)

    def cancel_wait(self):
        """Cancel blocked wait_event() call."""
        MgslCancelWaitEvent(self._handle)

    def cancel_write(self):
        """Cancel blocked write() call."""
        MgslCancelTransmit(self._handle)

    def set_gpio(self, mask:int, states:int):
        """
        Set GPIO outputs to specified state.
        mask = bit mask of outputs to alter
        states = bit mask of output states
        """
        gpio = GPIO_DESC()
        gpio.state = states
        gpio.smask = mask
        gpio.dmask = 0  # unused
        gpio.dir = 0  # unused
        MgslSetGpio(self._handle, gpio)

    def get_gpio(self) -> int:
        """Return bitmap of GPIO states."""
        gpio = GPIO_DESC()
        MgslGetGpio(self._handle, gpio)
        return gpio.state

    def set_gpio_direction(self, mask:int, dir:int):
        """
        Set GPIO signal directions.
        mask = bit mask of GPIO directions to alter
        dir = bit mask of signal direction (0=input,1=output)
        """
        gpio = GPIO_DESC()
        gpio.state = 0 # unused
        gpio.smask = 0 # unused
        gpio.dmask = mask
        gpio.dir = dir
        MgslSetGpio(self._handle, gpio)

    def get_gpio_direction(self) -> int:
        """
        Return bitmap of GPIO signal directions.
        0 = input, 1 = output
        """
        gpio = GPIO_DESC()
        MgslGetGpio(self._handle, gpio)
        return gpio.dir

    def set_option(self, option:int, value:int):
        MgslSetOption(self._handle, option, value)

    def get_option(self, option:int) -> int:
        value = INT()
        error = MgslGetOption(self._handle, option, value)
        if error:
            return 0
        return value.value

    def _set_default_read_size(self):
        if self._settings.protocol == self.HDLC or \
            self._settings.protocol == self.TDM:
            # protocol framing determines returned read size
            self._default_read_size = self._defaults.max_data_size
        else:
            self._default_read_size = 1

    def apply_settings(self, settings):
        """Apply settings in Port.Settings object to port."""
        self._reset_pio()
        self._settings = deepcopy(settings)
        self._set_default_read_size()

        self._msb_first = settings.msb_first

        # convert tdm settings to 32 bit tdm_options value

        if settings.tdm_sync_delay == 1:
            tdm_options = TDM_SYNC_DELAY_1BIT
        elif settings.tdm_sync_delay == 2:
            tdm_options = TDM_SYNC_DELAY_2BITS
        else:
            tdm_options = 0

        if settings.tdm_sync_frame:
            tdm_options |= TDM_SYNC_FRAME_ON

        if settings.tdm_sync_short:
            tdm_options |= TDM_TX_SYNC_WIDTH_BIT

        if settings.tdm_sync_invert:
            tdm_options |= TDM_SYNC_POLARITY_INVERT

        # tdm_options[15:8] 8 bit frame count
        # valid tdm_frame_count: 1 to 256
        if settings.tdm_frame_count and (settings.tdm_frame_count < 257):
            tdm_options |= (settings.tdm_frame_count - 1) << 8

        # tdm_options[7:3] 0=384 slots, 1-31 = 2-32 slots
        # valid tdm_slot_count: 384 and 2-32
        if (settings.tdm_slot_count > 1) and (settings.tdm_slot_count < 33):
            tdm_options |= (settings.tdm_slot_count - 1) << 3

        if settings.tdm_slot_bits == 8:
            tdm_options |= TDM_SLOT_SIZE_8BITS
        elif settings.tdm_slot_bits == 12:
            tdm_options |= TDM_SLOT_SIZE_12BITS
        elif settings.tdm_slot_bits == 16:
            tdm_options |= TDM_SLOT_SIZE_16BITS
        elif settings.tdm_slot_bits == 20:
            tdm_options |= TDM_SLOT_SIZE_20BITS
        elif settings.tdm_slot_bits == 24:
            tdm_options |= TDM_SLOT_SIZE_24BITS
        elif settings.tdm_slot_bits == 28:
            tdm_options |= TDM_SLOT_SIZE_28BITS
        else:
            tdm_options |= TDM_SLOT_SIZE_32BITS

        self._tdm_options = tdm_options

        # translate Settings object into base API calls

        params = MGSL_PARAMS()
        params.Mode = settings.protocol
        params.Loopback = settings.internal_loopback

        params.Flags = 0

        if settings.transmit_clock == Port.RXC_INPUT:
            params.Flags |= HDLC_FLAG_TXC_RXCPIN
        elif settings.transmit_clock == Port.INTERNAL:
            params.Flags |= HDLC_FLAG_TXC_BRG
        elif settings.transmit_clock == Port.RECOVERED:
            params.Flags |= HDLC_FLAG_TXC_DPLL
        if settings.transmit_clock_invert:
            params.Flags |= HDLC_FLAG_TXC_INV

        if settings.receive_clock == Port.TXC_INPUT:
            params.Flags |= HDLC_FLAG_RXC_TXCPIN
        elif settings.receive_clock == Port.INTERNAL:
            params.Flags |= HDLC_FLAG_RXC_BRG
        elif settings.receive_clock == Port.RECOVERED:
            params.Flags |= HDLC_FLAG_RXC_DPLL
        if settings.receive_clock_invert:
            params.Flags |= HDLC_FLAG_RXC_INV

        if settings.auto_rts:
            params.Flags |= HDLC_FLAG_AUTO_RTS
        if settings.auto_cts:
            params.Flags |= HDLC_FLAG_AUTO_CTS
        if settings.auto_dcd:
            params.Flags |= HDLC_FLAG_AUTO_DCD

        params.Encoding = settings.encoding
        params.ClockSpeed = settings.internal_clock_rate

        params.CrcType = settings.crc
        if not settings.discard_data_with_error:
            params.CrcType |= HDLC_CRC_RETURN_CRCERR_FRAME
        if not settings.discard_received_crc:
            params.CrcType |= HDLC_CRC_RETURN_CRC

        params.Addr = settings.hdlc_address_filter

        if settings.transmit_preamble_bits == 8:
            params.PreambleLength = HDLC_PREAMBLE_LENGTH_8BITS
        elif settings.transmit_preamble_bits == 16:
            params.PreambleLength = HDLC_PREAMBLE_LENGTH_16BITS
        elif settings.transmit_preamble_bits == 32:
            params.PreambleLength = HDLC_PREAMBLE_LENGTH_32BITS
        elif settings.transmit_preamble_bits == 64:
            params.PreambleLength = HDLC_PREAMBLE_LENGTH_64BITS
        else:
            params.PreambleLength = HDLC_PREAMBLE_LENGTH_8BITS
            params.PreamblePattern = HDLC_PREAMBLE_PATTERN_NONE

        if settings.transmit_preamble_bits == 0:
            params.PreamblePattern = HDLC_PREAMBLE_PATTERN_NONE
        elif settings.transmit_preamble_pattern == 0:
            params.PreamblePattern = HDLC_PREAMBLE_PATTERN_ZEROS
        elif settings.transmit_preamble_pattern == 0xff:
            params.PreamblePattern = HDLC_PREAMBLE_PATTERN_ONES
        elif settings.transmit_preamble_pattern == 0x55:
            params.PreamblePattern = HDLC_PREAMBLE_PATTERN_10
        elif settings.transmit_preamble_pattern == 0xaa:
            params.PreamblePattern = HDLC_PREAMBLE_PATTERN_01
        elif settings.transmit_preamble_pattern == 0x7e:
            params.PreamblePattern = HDLC_PREAMBLE_PATTERN_FLAGS
        else:
            params.PreamblePattern = HDLC_PREAMBLE_PATTERN_NONE

        params.DataRate = settings.async_data_rate
        params.DataBits = settings.async_data_bits
        params.StopBits = settings.async_stop_bits
        params.Parity = settings.async_parity

        if settings.protocol == self.BISYNC:
            self.transmit_idle_pattern = settings.sync_pattern
        elif settings.protocol == self.MONOSYNC:
            self.transmit_idle_pattern = settings.sync_pattern

        if settings.internal_clock_rate and \
            self.base_clock_rate % (settings.internal_clock_rate * 16):
            # x16 reference clock is not divisor of base clock
            # fall back to x8 reference clock
            params.Flags |= HDLC_FLAG_DPLL_DIV8

        MgslSetParams(self._handle, params)


    def get_settings(self):
        """Return Port.Settings object containing current settings."""

        params = MGSL_PARAMS()
        error = MgslGetParams(self._handle, params)
        if error:
            return None

        settings = Port.Settings()
        settings.protocol = params.Mode
        settings.internal_loopback = bool(params.Loopback)

        rxc_flags = params.Flags & 0x8300
        if rxc_flags & HDLC_FLAG_RXC_BRG:
            settings.receive_clock = Port.INTERNAL
        elif rxc_flags & HDLC_FLAG_RXC_DPLL:
            settings.receive_clock = Port.RECOVERED
        elif rxc_flags & HDLC_FLAG_RXC_TXCPIN:
            settings.receive_clock = Port.TXC_INPUT
        else:
            settings.receive_clock = Port.RXC_INPUT

        if params.Flags & HDLC_FLAG_RXC_INV:
            settings.receive_clock_invert = True
        else:
            settings.receive_clock_invert = False

        txc_flags = params.Flags & 0x0c08
        if txc_flags & HDLC_FLAG_TXC_BRG:
            settings.transmit_clock = Port.INTERNAL
        elif txc_flags & HDLC_FLAG_TXC_DPLL:
            settings.transmit_clock = Port.RECOVERED
        elif txc_flags & HDLC_FLAG_TXC_RXCPIN:
            settings.transmit_clock = Port.RXC_INPUT
        else:
            settings.transmit_clock = Port.TXC_INPUT

        if params.Flags & HDLC_FLAG_TXC_INV:
            settings.transmit_clock_invert = True
        else:
            settings.transmit_clock_invert = False

        if params.Flags & HDLC_FLAG_AUTO_RTS:
            settings.auto_rts = True
        else:
            settings.auto_rts = False
        if params.Flags & HDLC_FLAG_AUTO_CTS:
            settings.auto_cts = True
        else:
            settings.auto_cts = False
        if params.Flags & HDLC_FLAG_AUTO_DCD:
            settings.auto_dcd = True
        else:
            settings.auto_dcd = False

        settings.encoding = params.Encoding
        settings.internal_clock_rate = params.ClockSpeed

        settings.crc = params.CrcType & HDLC_CRC_MODE
        if params.CrcType & HDLC_CRC_RETURN_CRCERR_FRAME:
            settings.discard_data_with_error = False
        else:
            settings.discard_data_with_error = True
            
        if params.CrcType & HDLC_CRC_RETURN_CRC:
            settings.discard_received_crc = False
        else:
            settings.discard_received_crc = True

        settings.hdlc_address_filter = params.Addr

        if params.PreambleLength == HDLC_PREAMBLE_LENGTH_8BITS:
            settings.transmit_preamble_bits = 8
        elif params.PreambleLength == HDLC_PREAMBLE_LENGTH_16BITS:
            settings.transmit_preamble_bits = 16
        elif params.PreambleLength == HDLC_PREAMBLE_LENGTH_32BITS:
            settings.transmit_preamble_bits = 32
        elif params.PreambleLength == HDLC_PREAMBLE_LENGTH_64BITS:
            settings.transmit_preamble_bits = 64
        else:
            settings.transmit_preamble_bits = 0

        if params.PreamblePattern == HDLC_PREAMBLE_PATTERN_ZEROS:
            settings.transmit_preamble_pattern = 0
        elif params.PreamblePattern == HDLC_PREAMBLE_PATTERN_ONES:
            settings.transmit_preamble_pattern = 0xff
        elif params.PreamblePattern == HDLC_PREAMBLE_PATTERN_10:
            settings.transmit_preamble_pattern = 0x55
        elif params.PreamblePattern == HDLC_PREAMBLE_PATTERN_01:
            settings.transmit_preamble_pattern = 0xaa
        elif params.PreamblePattern == HDLC_PREAMBLE_PATTERN_FLAGS:
            settings.transmit_preamble_pattern = 0x7e
        else:
            settings.transmit_preamble_pattern = 0
            settings.transmit_preamble_bits = 0

        settings.async_data_rate = params.DataRate
        settings.async_data_bits = params.DataBits
        settings.async_stop_bits = params.StopBits
        settings.async_parity = params.Parity

        # convert tdm settings to 32 tdm_options value
        tdm_options = self._tdm_options

        sync_delay = (tdm_options >> 18) & 3
        if sync_delay == TDM_SYNC_DELAY_1BIT:
            settings.tdm_sync_delay = 1
        elif sync_delay == TDM_SYNC_DELAY_2BITS:
            settings.tdm_sync_delay = 2
        else:
            settings.tdm_sync_delay = 0

        if tdm_options & TDM_TX_SYNC_WIDTH_BIT:
            settings.tdm_sync_short = True
        else:
            settings.tdm_sync_short = False

        if tdm_options & TDM_SYNC_POLARITY_INVERT:
            settings.tdm_sync_invert = True
        else:
            settings.tdm_sync_invert = False

        settings.tdm_frame_count = ((tdm_options >> 8) & 0xff) + 1

        slot_count = (tdm_options >> 3) & 0x1f
        if slot_count == 0:
            settings.tdm_slot_count = 384
        else:
            settings.tdm_slot_count = slot_count + 1

        settings.tdm_slot_bits = 4 + ((tdm_options & 0x7) * 4)

        settings.msb_first = self._msb_first

        if settings.protocol == self.BISYNC:
            settings.sync_pattern = self.transmit_idle_pattern
        elif settings.protocol == self.MONOSYNC:
            settings.sync_pattern = self.transmit_idle_pattern

        self._settings = deepcopy(settings)
        self._set_default_read_size()

        return settings

    @property
    def transmit_idle_pattern(self):
        return self._tx_idle & 0xffff

    @transmit_idle_pattern.setter
    def transmit_idle_pattern(self, idle):
        if idle == 0x7e:
            self._tx_idle = HDLC_TXIDLE_FLAGS
        elif idle == 0xaa:
            self._tx_idle = HDLC_TXIDLE_ALT_ZEROS_ONES
        elif idle == 0:
            self._tx_idle = HDLC_TXIDLE_ZEROS
        elif idle == 0xff:
            self._tx_idle = HDLC_TXIDLE_ONES
        elif idle < 0x100:
            self._tx_idle = HDLC_TXIDLE_CUSTOM_8 + idle
        else:
            self._tx_idle = HDLC_TXIDLE_CUSTOM_16 + idle
        MgslSetIdleMode(self._handle, self._tx_idle)

    @property
    def signals(self) -> int:
        signals = INT(0)
        MgslGetSerialSignals(self._handle, signals)
        return signals.value

    @signals.setter
    def signals(self, signals:int):
        MgslSetSerialSignals(self._handle, signals)

    @property
    def dtr(self) -> bool:
        return bool(self.signals & Port.DTR)

    @dtr.setter
    def dtr(self, x:bool):
        if x:
            self.signals |= Port.DTR
        else:
            self.signals &= ~Port.DTR

    @property
    def rts(self) -> bool:
        return bool(self.signals & Port.RTS)

    @rts.setter
    def rts(self, x:bool):
        if x:
            self.signals |= Port.RTS
        else:
            self.signals &= ~Port.RTS

    @property
    def dsr(self) -> bool:
        return bool(self.signals & Port.DSR)

    @property
    def cts(self) -> bool:
        return bool(self.signals & Port.CTS)

    @property
    def dcd(self) -> bool:
        return bool(self.signals & Port.DCD)

    @property
    def ri(self) -> bool:
        return bool(self.signals & Port.RI)

    @property
    def txd(self) -> bool:
        return bool(self.signals & Port.TXD)

    @property
    def rxd(self) -> bool:
        return bool(self.signals & Port.RXD)

    @property
    def rx_discard_too_large(self):
        return not self.get_option(MGSL_OPT_RX_DISCARD_TOO_LARGE)

    @rx_discard_too_large.setter
    def rx_discard_too_large(self, x):
        self.set_option(MGSL_OPT_RX_DISCARD_TOO_LARGE, x)

    @property
    def underrun_retry_limit(self):
        return self.get_option(MGSL_OPT_UNDERRUN_RETRY_LIMIT)

    @underrun_retry_limit.setter
    def underrun_retry_limit(self, x):
        self.set_option(MGSL_OPT_UNDERRUN_RETRY_LIMIT, x)

    @property
    def ll(self) -> bool:
        return not self.get_option(MGSL_OPT_ENABLE_LOCALLOOPBACK)

    @ll.setter
    def ll(self, x:bool):
        self.set_option(MGSL_OPT_ENABLE_LOCALLOOPBACK, x)

    @property
    def rl(self) -> bool:
        return not self.get_option(MGSL_OPT_ENABLE_REMOTELOOPBACK)

    @rl.setter
    def rl(self, x:bool):
        self.set_option(MGSL_OPT_ENABLE_REMOTELOOPBACK, x)

    @property
    def jcr(self):
        return not self.get_option(MGSL_OPT_JCR)

    @jcr.setter
    def jcr(self, x):
        self.set_option(MGSL_OPT_JCR, x)

    @property
    def interface(self) -> int:
        return self.get_option(MGSL_OPT_INTERFACE)

    @interface.setter
    def interface(self, x:int):
        self.set_option(MGSL_OPT_INTERFACE, x)

    @property
    def rts_output_enable(self) -> bool:
        return self.get_option(MGSL_OPT_RTS_DRIVER_CONTROL)

    @rts_output_enable.setter
    def rts_output_enable(self, value:bool):
        self.set_option(MGSL_OPT_RTS_DRIVER_CONTROL, value)

    @property
    def ignore_read_errors(self):
        return self.get_option(MGSL_OPT_RX_ERROR_MASK)

    @ignore_read_errors.setter
    def ignore_read_errors(self, x):
        self.set_option(MGSL_OPT_RX_ERROR_MASK, x)

    @property
    def base_clock_rate(self) -> int:
        return self.get_option(MGSL_OPT_CLOCK_BASE_FREQ)

    @base_clock_rate.setter
    def base_clock_rate(self, x:int):
        self.set_option(MGSL_OPT_CLOCK_BASE_FREQ, x)

    @property
    def half_duplex(self) -> bool:
        return bool(self.get_option(MGSL_OPT_HALF_DUPLEX))

    @half_duplex.setter
    def half_duplex(self, x:bool):
        self.set_option(MGSL_OPT_HALF_DUPLEX, x)

    @property
    def _msb_first(self) -> bool:
        return bool(self.get_option(MGSL_OPT_MSB_FIRST))

    @_msb_first.setter
    def _msb_first(self, x:bool):
        self.set_option(MGSL_OPT_MSB_FIRST, x)

    def receive_count(self) -> int:
        return self.get_option(MGSL_OPT_RX_COUNT)

    def transmit_count(self) -> int:
        return self.get_option(MGSL_OPT_TX_COUNT)

    @property
    def blocked_io(self) -> bool:
        return self._blocked_io

    @blocked_io.setter
    def blocked_io(self, x):
        self._blocked_io = x
        self.set_option(MGSL_OPT_RX_POLL, not x)
        self.set_option(MGSL_OPT_TX_POLL, not x)

    @property
    def termination(self) -> bool:
        return not self.get_option(MGSL_OPT_NO_TERMINATION)

    @termination.setter
    def termination(self, x):
        self.set_option(MGSL_OPT_NO_TERMINATION, not x)

    @property
    def _tdm_options(self):
        return self.get_option(MGSL_OPT_TDM)

    @_tdm_options.setter
    def _tdm_options(self, x):
        self.set_option(MGSL_OPT_TDM, x)

    @property
    def enable_clock_output(self):
        return self.get_option(MGSL_OPT_AUXCLK_ENABLE)

    @enable_clock_output.setter
    def enable_clock_output(self, x):
        self.set_option(MGSL_OPT_AUXCLK_ENABLE, x)

    @property
    def underrun_count(self):
        return self.get_option(MGSL_OPT_UNDERRUN_COUNT)

    @underrun_count.setter
    def underrun_count(self, x):
        self.set_option(MGSL_OPT_UNDERRUN_COUNT, x)

    @property
    def transmit_idle_count(self):
        return self.get_option(MGSL_OPT_TX_IDLE_COUNT)

    @transmit_idle_count.setter
    def transmit_idle_count(self, x):
        self.set_option(MGSL_OPT_TX_IDLE_COUNT, x)

    @property
    def output_control(self):
        return self.get_option(MGSL_OPT_RS422_OE)

    @output_control.setter
    def output_control(self, x):
        self.set_option(MGSL_OPT_RS422_OE, x)

    @property
    def name(self) -> int:
        """Return port name."""
        return self._name

    def set_defaults(self, defaults):
        if not self.is_open() or not self._port_id:
            return
        self._defaults = deepcopy(defaults)
        self._set_default_read_size()

        cfg = MGSL_PORT_CONFIG_EX()
        error = MgslGetPortConfigEx(self._port_id, cfg)
        if error:
            return
        cfg.MaxFrameSize = defaults.max_data_size
        cfg.Flags = defaults.interface
        if defaults.rts_output_enable:
            cfg.Flags |= MGSL_RTS_DRIVER_CONTROL
        if not defaults.termination:
            cfg.Flags |= MGSL_NO_TERMINATION
        MgslSetPortConfigEx(self._port_id, cfg)

    def get_defaults(self):
        if not self.is_open() or not self._port_id:
            return None
        cfg = MGSL_PORT_CONFIG_EX()
        error = MgslGetPortConfigEx(self._port_id, cfg)
        if error:
            return None
        defaults = self.Defaults()
        defaults.max_data_size = cfg.MaxFrameSize
        defaults.interface = cfg.Flags & MGSL_INTERFACE_MASK
        defaults.rts_output_enable = bool(cfg.Flags & MGSL_RTS_DRIVER_CONTROL)
        defaults.termination = not bool(cfg.Flags & MGSL_NO_TERMINATION)
        self._defaults = deepcopy(defaults)
        self._set_default_read_size()
        return defaults

    def _reset_pio(self):
        # work around Windows driver bug where PIO mode is not cleared
        # when switching to protocol that does not support PIO mode.
        if not self.is_open():
            return
        old_params = MGSL_PARAMS()
        MgslGetParams(self._handle, old_params)
        old_blocked_io = self.blocked_io

        params = MGSL_PARAMS()
        params.Mode = Port.RAW
        MgslSetParams(self._handle, params)
        self.blocked_io = False
        try:
            self.read(256)
        except:
            pass

        self.blocked_io = old_blocked_io
        MgslSetParams(self._handle, old_params)

    def set_fsynth_rate(self, rate: int) -> bool:
        """
        Set frequency synthesizer to specified rate.
        Return True if success (rate supported), otherwise False.
        """
        resources = MGSL_ASSIGNED_RESOURCES()
        error = MgslGetAssignedResources(self._handle, resources)
        if error:
            return False

        # select table and GPIO bit positions for device type
        if resources.DeviceId == SYNCLINK_USB_DEVICE_ID:
            freq_table = usb_table
            mux = self.gpio[23]
            clk = self.gpio[22]
            sel = self.gpio[21]
            dat = self.gpio[20]
        else:
            freq_table = gt4e_table
            mux = self.gpio[15]
            clk = self.gpio[14]
            sel = self.gpio[13]
            dat = self.gpio[12]

        data = 0

        # search for entry for requested output frequency
        for entry in freq_table:
            if entry.freq == rate:
                data = entry.data
                break

        if data == 0:
            return False

        clk.state = False

        # write 132 bit clock program word one bit at a time
        for i in range(0, 132):
            if (i % 32) == 0:
                dword_val = data[int(i/32)]
            if dword_val & (1 << 31):
                dat.state = True
            else:
                dat.state = False
            # pulse clock signal to load next bit
            clk.state = True
            clk.state = False
            dword_val <<= 1

        # pulse select signal to accept new word
        sel.state = True
        sel.state = False

        # set base clock input multiplexer
        # False = fixed frequency oscillator (default 14.7456MHz)
        # True  = frequency syntheziser output
        mux.state = True

        # tell port the new rate
        self.base_clock_rate = rate
        return True

    def __init__(self, name:str):
        self._handle = HANDLE()
        self._open = False
        self._tx_idle = HDLC_TXIDLE_FLAGS
        self._name = name
        self._port_id = self.name_to_id(self._name)
        self._blocked_io = True
        self._defaults = self.Defaults()
        self._settings = self.Settings()
        self.gpio = []
        for bit in range(0,32):
            gpio = self.GPIO(self, bit)
            self.gpio.append(gpio)

    def __del__(self):
        if self.is_open():
            self.close()

    def __repr__(self):
        return 'Port object at ' + hex(id(self)) + '\n' + \
            'name = ' + self.name

    def __str__(self):
        return self.__repr__()


# This code programs the frequency synthesizer on the SyncLink GT2e/GT4e
# PCI express serial adapters and SyncLink USB device to a specified frequency
# and selects the synthesizer output as the adapter base clock. ONLY the GT2e/GT4e
# cards and SyncLink USB device have this feature. Copy and paste this code into
# applications that require a non-standard base clock frequency.
#
# SyncLink GT family serial adapters have a fixed 14.7456MHz base clock.
# The serial controller generates data clocks by dividing the base clock
# by an integer. Only discrete data clock values can be generated
# exactly from a given base clock frequency. When an exact data clock
# value is required that cannot be derived by dividing 14.7456MHz by
# and integer, a different base clock value must be used. One way to
# do this is special ordering a different fixed base clock which is
# installed at the factory.
#
# The SyncLink GT2e, GT4e and USB serial devices have both
# a 14.7456MHz fixed base clock and a variable frequency synthesizer.
# The serial controller can use either as the base clock.
#
# The frequency synthesizer is an Integrated Device Technologies (IDT)
# ICS307-3 device. The reference clock input to the synthesizer is
# the fixed 14.7456MHz clock.
# GT2E/GT4E uses synthesizer CLK1 output
# USB uses synthesizer CLK3 output
# Refer to the appropriate hardware user's manual for more details.
#
# The synthesizer SPI programming interface is connected to the serial
# controller general purpose I/O signals. The GPIO portion of the serial
# API is used to program the synthesizer with a 132 bit word. This word
# is calculated using the IDT Versaclock software available at www.idt.com
#
# Contact Microgate for help in producing a programming word for a specific
# frequency output. Several common frequencies are included in this code.
# Maximum supported base clock is 66MHz
#
# Note:
# After programming the frequency synthesizer and selecting it
# as the base clock, each individual port of a card must be configured with
# MgslSetOption(fd, MGSL_OPT_CLOCK_BASE_FREQ, freq_value);
#
# This allows the device driver to correctly calculate divisors
# for a specified data clock rate. All ports on a card share
# a common base clock.

# Each frequency table entry contains an output frequency
# and the associated 132 bit synthesizer programming word
# to produce the frequency.

# The programming word comes from the Versaclock 2 software
# parsed into 5 32-bit integers. The final 4 bits are placed
# in the most significant 4 bits of the final 32-bit integer.
class FREQ_TABLE_ENTRY:
    def __init__(self, freq, data):
        self.freq = freq  # frequency
        self.data = data  # synth programming data


# GT2e/GT4e
#
# Base Clock = dedicated 14.7456MHz oscillator
#
# ICS307-3 (clock):
# - reference clock = 14.7456MHz oscillator
# - VDD = 3.3V
# - CLK1 (pin 8) output drives FPGA fsynth input
gt4e_table = [
    FREQ_TABLE_ENTRY(
        1228800,  [0x1800155E, 0x29A00000, 0x00000000, 0x0000DFFF, 0x60000000]),
    FREQ_TABLE_ENTRY(
        2875000,  [0x08001494, 0x28A00000, 0x00000000, 0x000211FE, 0x20000000]),
    FREQ_TABLE_ENTRY(
        12288000, [0x29BFDC00, 0x61200000, 0x00000000, 0x0000A5FF, 0xA0000000]),
    FREQ_TABLE_ENTRY(
        14745600, [0x38003C05, 0x24200000, 0x00000000, 0x000057FF, 0xA0000000]),
    FREQ_TABLE_ENTRY(
        16000000, [0x280CFC02, 0x64A00000, 0x00000000, 0x000307FD, 0x20000000]),
    FREQ_TABLE_ENTRY(
        16384000, [0x08001402, 0xA1200000, 0x00000000, 0x0000A5FF, 0xA0000000]),
    FREQ_TABLE_ENTRY(
        19660800, [0x08001403, 0xE1200000, 0x00000000, 0x0000A1FF, 0xA0000000]),
    FREQ_TABLE_ENTRY(
        20000000, [0x00001403, 0xE0C00000, 0x00000000, 0x00045E02, 0xF0000000]),
    FREQ_TABLE_ENTRY(
        23040000, [0x08001404, 0xA0A00000, 0x00000000, 0x0003A7FC, 0x60000000]),
    FREQ_TABLE_ENTRY(
        24000000, [0x00001404, 0xE1400000, 0x00000000, 0x0003D5FC, 0x20000000]),
    FREQ_TABLE_ENTRY(
        27000000, [0x00001405, 0x60C00000, 0x00000000, 0x00061E04, 0xF0000000]),
    FREQ_TABLE_ENTRY(
        28219200, [0x00001405, 0xA1400000, 0x00000000, 0x0003C1FC, 0x20000000]),
    FREQ_TABLE_ENTRY(
        28800000, [0x18001405, 0x61A00000, 0x00000000, 0x0000EBFF, 0x60000000]),
    FREQ_TABLE_ENTRY(
        30000000, [0x20267C05, 0x64C00000, 0x00000000, 0x00050603, 0x30000000]),
    FREQ_TABLE_ENTRY(
        32000000, [0x21BFDC00, 0x5A400000, 0x00000000, 0x0004D206, 0x30000000]),
    FREQ_TABLE_ENTRY(
        33200000, [0x00001400, 0xD8C00000, 0x00000000, 0x0005E204, 0xB0000000]),
    FREQ_TABLE_ENTRY(
        33320000, [0x08001400, 0xD8A00000, 0x00000000, 0x0001C7FE, 0x60000000]),
    FREQ_TABLE_ENTRY(
        38400000, [0x00001406, 0xE1800000, 0x00000000, 0x00098009, 0xF0000000]),
    FREQ_TABLE_ENTRY(
        40000000, [0x00001406, 0xE1800000, 0x00000000, 0x0009E609, 0xF0000000]),
    FREQ_TABLE_ENTRY(
        45056000, [0x08001406, 0xE0200000, 0x00000000, 0x000217FE, 0x20000000]),
    FREQ_TABLE_ENTRY(
        50000000, [0x00001400, 0x58C00000, 0x00000000, 0x0005E604, 0x70000000]),
    FREQ_TABLE_ENTRY(
        64000000, [0x21BFDC00, 0x12000000, 0x00000000, 0x000F5E14, 0xF0000000])
]


# SyncLink USB
#
# Base Clock = ICS307-3 CLK1 (pin 8) output (power up default = 14.7456MHz)
#
# ICS307-3 (xtal):
# - reference clock = 14.7456MHz xtal
# - VDD = 3.3V
# - CLK3 (pin 14) output drives FPGA fsynth input
# - CLK1 (pin 8)  output drives FPGA base clock input
#
# Note: CLK1 and CLK3 outputs must always be driven to prevent floating
# clock inputs to the FPGA. When calculating programming word with Versaclock,
# select same output on CLK1 and CLK3 or select CLK1 as multiple of CLK3.
usb_table = [
    FREQ_TABLE_ENTRY(
        1228800,  [0x296C1402, 0x25200000, 0x00000000, 0x00009FFF, 0xA0000000]),
    FREQ_TABLE_ENTRY(
        2875000,  [0x317C1400, 0x21A00000, 0x00000000, 0x0000BBFE, 0xA0000000]),
    FREQ_TABLE_ENTRY(
        12288000, [0x28401400, 0xE5200000, 0x00000000, 0x00009BFF, 0xA0000000]),
    FREQ_TABLE_ENTRY(
        14745600, [0x28481401, 0xE5200000, 0x00000000, 0x0000A5FF, 0xA0000000]),
    FREQ_TABLE_ENTRY(
        16000000, [0x284C1402, 0x64A00000, 0x00000000, 0x000307FD, 0x20000000]),
    FREQ_TABLE_ENTRY(
        16384000, [0x28501402, 0xE4A00000, 0x00000000, 0x0001F9FE, 0x20000000]),
    FREQ_TABLE_ENTRY(
        19660800, [0x38541403, 0x65A00000, 0x00000000, 0x0000B1FF, 0xA0000000]),
    FREQ_TABLE_ENTRY(
        20000000, [0x205C1404, 0x65400000, 0x00000000, 0x00068205, 0xF0000000]),
    FREQ_TABLE_ENTRY(
        23040000, [0x38601404, 0xE5A00000, 0x00000000, 0x0001B3FE, 0x60000000]),
    FREQ_TABLE_ENTRY(
        24000000, [0x20601404, 0xE5400000, 0x00000000, 0x0003D5FC, 0x20000000]),
    FREQ_TABLE_ENTRY(
        27000000, [0x20641405, 0x64C00000, 0x00000000, 0x00061E04, 0xF0000000]),
    FREQ_TABLE_ENTRY(
        28219200, [0x20641405, 0x64C00000, 0x00000000, 0x0004F603, 0x70000000]),
    FREQ_TABLE_ENTRY(
        28800000, [0x38641405, 0x65A00000, 0x00000000, 0x0000EBFF, 0x60000000]),
    FREQ_TABLE_ENTRY(
        30000000, [0x20641405, 0x64C00000, 0x00000000, 0x00050603, 0x30000000]),
    FREQ_TABLE_ENTRY(
        32000000, [0x206C1406, 0x65400000, 0x00000000, 0x00049E03, 0xF0000000]),
    FREQ_TABLE_ENTRY(
        33200000, [0x20681405, 0xE4C00000, 0x00000000, 0x00061804, 0x70000000]),
    FREQ_TABLE_ENTRY(
        33320000, [0x21FBB800, 0x05400000, 0x00000000, 0x00038BFC, 0x20000000]),
    FREQ_TABLE_ENTRY(
        38400000, [0x20701406, 0xE5800000, 0x00000000, 0x00098009, 0xF0000000]),
    FREQ_TABLE_ENTRY(
        40000000, [0x20701406, 0xE5800000, 0x00000000, 0x0009E609, 0xF0000000]),
    FREQ_TABLE_ENTRY(
        45056000, [0x28701406, 0xE4200000, 0x00000000, 0x000217FE, 0x20000000]),
    FREQ_TABLE_ENTRY(
        50000000, [0x20741407, 0x65400000, 0x00000000, 0x00068205, 0xF0000000]),
    FREQ_TABLE_ENTRY(
        64000000, [0x20781400, 0x4D400000, 0x00000000, 0x00049E03, 0xF0000000])
]
