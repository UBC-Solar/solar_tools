#!/usr/bin/env python3
"""PCAN-View style CAN monitor (minimal, SocketCAN via python-can + PySide6)

Features: interface selection, live monitor, basic filtering, send panel, logging.
"""
import sys
import csv
import time
from datetime import datetime
from pathlib import Path

from PySide6 import QtCore, QtWidgets, QtGui

try:
    import can
except Exception:
    can = None


class CanReaderThread(QtCore.QThread):
    msg_received = QtCore.Signal(object)

    def __init__(self, bus):
        super().__init__()
        self.bus = bus
        self._running = True

    def run(self):
        while self._running:
            try:
                msg = self.bus.recv(timeout=1)
            except Exception:
                msg = None
            if msg is not None:
                self.msg_received.emit(msg)

    def stop(self):
        self._running = False
        self.wait(2000)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PCAN-View (Py)')
        self.resize(1000, 600)

        self.bus = None
        self.reader = None
        self.logging = False
        self.logfile = None

        self._setup_ui()

    def _setup_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)

        # Left panel: interface/config
        left = QtWidgets.QVBoxLayout()
        self.iface_combo = QtWidgets.QComboBox()
        self.refresh_ifaces()
        left.addWidget(QtWidgets.QLabel('Interface'))
        left.addWidget(self.iface_combo)
        self.connect_btn = QtWidgets.QPushButton('Connect')
        self.connect_btn.clicked.connect(self.toggle_connect)
        left.addWidget(self.connect_btn)

        left.addWidget(QtWidgets.QLabel('Filter (ID or hex)'))
        self.filter_edit = QtWidgets.QLineEdit()
        left.addWidget(self.filter_edit)

        self.pause_btn = QtWidgets.QPushButton('Pause')
        self.pause_btn.setCheckable(True)
        self.pause_btn.clicked.connect(lambda: None)
        left.addWidget(self.pause_btn)

        self.clear_btn = QtWidgets.QPushButton('Clear')
        self.clear_btn.clicked.connect(self.clear_table)
        left.addWidget(self.clear_btn)

        self.log_btn = QtWidgets.QPushButton('Start Logging')
        self.log_btn.clicked.connect(self.toggle_logging)
        left.addWidget(self.log_btn)

        left.addStretch()
        layout.addLayout(left, 1)

        # Center: message table
        self.table = QtWidgets.QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(['Timestamp', 'Interface', 'Dir', 'ID', 'DLC', 'Data', 'Freq(Hz)', 'Notes'])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table, 6)

        # Right: send panel
        right = QtWidgets.QVBoxLayout()
        right.addWidget(QtWidgets.QLabel('Send CAN Frame'))
        self.id_edit = QtWidgets.QLineEdit('580')
        right.addWidget(self.id_edit)
        self.ext_check = QtWidgets.QCheckBox('Extended ID')
        right.addWidget(self.ext_check)
        self.dlc_spin = QtWidgets.QSpinBox(); self.dlc_spin.setRange(0,8); self.dlc_spin.setValue(8)
        right.addWidget(QtWidgets.QLabel('DLC'))
        right.addWidget(self.dlc_spin)
        self.data_edit = QtWidgets.QLineEdit('11 22 33 44 55 66 77 88')
        right.addWidget(QtWidgets.QLabel('Data (hex bytes separated)'))
        right.addWidget(self.data_edit)
        self.send_btn = QtWidgets.QPushButton('Send')
        self.send_btn.clicked.connect(self.send_frame)
        right.addWidget(self.send_btn)

        self.periodic_check = QtWidgets.QCheckBox('Periodic')
        right.addWidget(self.periodic_check)
        self.interval_spin = QtWidgets.QSpinBox(); self.interval_spin.setRange(10, 3600000); self.interval_spin.setValue(1000)
        right.addWidget(QtWidgets.QLabel('Interval ms'))
        right.addWidget(self.interval_spin)

        right.addStretch()
        layout.addLayout(right, 2)

        # Timer for periodic send
        self.periodic_timer = QtCore.QTimer(self)
        self.periodic_timer.timeout.connect(self.send_frame)

    def refresh_ifaces(self):
        self.iface_combo.clear()
        # Detect can interfaces from /sys/class/net or ip
        ifaces = []
        try:
            for p in Path('/sys/class/net').iterdir():
                if p.name.startswith('can') or p.name.startswith('vcan'):
                    ifaces.append(p.name)
        except Exception:
            pass
        if not ifaces:
            # fallback to can0
            ifaces = ['can0']
        self.iface_combo.addItems(ifaces)

    def toggle_connect(self):
        if self.bus is None:
            iface = self.iface_combo.currentText()
            if can is None:
                QtWidgets.QMessageBox.critical(self, 'Missing dependency', 'python-can not installed')
                return
            try:
                self.bus = can.interface.Bus(channel=iface, bustype='socketcan')
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Failed to open', str(e))
                self.bus = None
                return
            self.reader = CanReaderThread(self.bus)
            self.reader.msg_received.connect(self.on_message)
            self.reader.start()
            self.connect_btn.setText('Disconnect')
        else:
            # disconnect
            if self.reader:
                self.reader.stop()
                self.reader = None
            try:
                self.bus.shutdown()
            except Exception:
                pass
            self.bus = None
            self.connect_btn.setText('Connect')

    def on_message(self, msg):
        if self.pause_btn.isChecked():
            return
        # filter
        filt = self.filter_edit.text().strip()
        if filt:
            try:
                if filt.lower().startswith('0x'):
                    filt_val = int(filt, 16)
                else:
                    filt_val = int(filt, 0)
            except Exception:
                filt_val = None
            if filt_val is not None and msg.arbitration_id != filt_val:
                return

        timestamp = datetime.fromtimestamp(msg.timestamp).isoformat(sep=' ')
        iface = getattr(msg, 'channel', '') or ''
        direction = 'Rx' if not msg.is_remote_frame and not msg.is_error_frame else 'Tx'
        msg_id = hex(msg.arbitration_id)
        dlc = msg.dlc
        data = ' '.join(f"{b:02X}" for b in msg.data)

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(timestamp))
        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(iface))
        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(direction))
        self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(msg_id))
        self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(dlc)))
        self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(data))
        self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(''))
        self.table.setItem(row, 7, QtWidgets.QTableWidgetItem(''))

        if self.logging and self.logfile:
            try:
                self.logfile.writerow([timestamp, iface, direction, msg.arbitration_id, dlc, data])
            except Exception:
                pass

        # auto-scroll
        self.table.scrollToBottom()

    def send_frame(self):
        if self.bus is None:
            QtWidgets.QMessageBox.warning(self, 'Not connected', 'Open an interface first')
            return
        try:
            ident = int(self.id_edit.text(), 0)
        except Exception:
            QtWidgets.QMessageBox.warning(self, 'Bad ID', 'Invalid CAN ID')
            return
        data_bytes = []
        for part in self.data_edit.text().split():
            try:
                data_bytes.append(int(part, 16))
            except Exception:
                pass
        msg = can.Message(arbitration_id=ident, data=bytes(data_bytes), is_extended_id=self.ext_check.isChecked())
        try:
            self.bus.send(msg)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Send failed', str(e))
            return

        if self.periodic_check.isChecked():
            self.periodic_timer.start(self.interval_spin.value())
        else:
            self.periodic_timer.stop()

    def toggle_logging(self):
        if not self.logging:
            fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save log', 'can_log.csv', 'CSV files (*.csv)')
            if not fname:
                return
            try:
                f = open(fname, 'w', newline='')
                self._csvfile = f
                self.logfile = csv.writer(f)
                self.logfile.writerow(['timestamp', 'interface', 'dir', 'id', 'dlc', 'data'])
                self.logging = True
                self.log_btn.setText('Stop Logging')
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Log failed', str(e))
        else:
            try:
                self._csvfile.close()
            except Exception:
                pass
            self.logging = False
            self.log_btn.setText('Start Logging')

    def clear_table(self):
        self.table.setRowCount(0)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
