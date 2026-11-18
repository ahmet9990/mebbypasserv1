#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mebbypass Windows arayüzü (tkinter — Python ile birlikte gelir).

GTK bu pakette Pardus/Linux için durur. Windows'ta `--gui` bu dosyayı
açar. Pencere kapanınca Linux sürümündeki gibi sorar: arka planda
sürsün mü, yoksa proxy durup sistem ayarı geri mi alınsın.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

from .core import (DEFAULT_PORT, LOG_FILE, AlreadyRunning, Server, log,
                   pid_alive, set_system, set_windows_autostart,
                   spawn_background, windows_autostart_path)


def _gui_lock_path() -> str:
    return os.path.join(os.path.expanduser("~"), ".mebbypass", "gui.pid")


def _acquire_gui_lock() -> bool:
    path = _gui_lock_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except OSError:
        return True
    try:
        with open(path, encoding="utf-8") as f:
            other = int(f.read().strip() or 0)
    except (OSError, ValueError):
        other = 0
    if other and other != os.getpid() and pid_alive(other):
        return False
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(os.getpid()))
    except OSError:
        return True
    return True


def _release_gui_lock() -> None:
    path = _gui_lock_path()
    try:
        with open(path, encoding="utf-8") as f:
            if int(f.read().strip() or 0) != os.getpid():
                return
        os.remove(path)
    except (OSError, ValueError):
        pass


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("mebbypass")
        self.geometry("640x560")
        self.minsize(520, 420)
        self.configure(bg="#10151c")
        self.server = None
        self._log_offset = 0
        self._quitting = False
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._font = ("Segoe UI", 10)
        self._font_b = ("Segoe UI", 10, "bold")
        self._mono = ("Consolas", 9)

        head = tk.Frame(self, bg="#10151c")
        head.pack(fill="x", padx=16, pady=(14, 6))
        tk.Label(head, text="mebbypass", fg="#f2f5f8", bg="#10151c",
                 font=("Segoe UI", 18, "bold")).pack(anchor="w")
        tk.Label(head, text="MEB/f@tih bypass  ·  Windows",
                 fg="#8aa0b4", bg="#10151c",
                 font=self._font).pack(anchor="w")

        card = tk.Frame(self, bg="#18222d", highlightthickness=1,
                        highlightbackground="#2a3a4a")
        card.pack(fill="x", padx=16, pady=8)
        self.pill = tk.Label(card, text="  KAPALI  ", fg="#ffffff",
                             bg="#3a4553", font=self._font_b, padx=8, pady=3)
        self.pill.pack(anchor="w", padx=12, pady=(12, 4))
        self.status_big = tk.Label(card, text="Durduruldu", fg="#f2f5f8",
                                   bg="#18222d", font=("Segoe UI", 20, "bold"))
        self.status_big.pack(anchor="w", padx=12)
        self.status_sub = tk.Label(
            card, text="Başlat'a basın — 8080 doluysa yedek port seçilir",
            fg="#8aa0b4", bg="#18222d", font=self._font, wraplength=560,
            justify="left")
        self.status_sub.pack(anchor="w", padx=12, pady=(0, 12))

        settings = tk.Frame(self, bg="#18222d", highlightthickness=1,
                            highlightbackground="#2a3a4a")
        settings.pack(fill="x", padx=16, pady=4)
        inner = tk.Frame(settings, bg="#18222d")
        inner.pack(fill="x", padx=12, pady=10)

        tk.Label(inner, text="Port", fg="#d5dee6", bg="#18222d",
                 font=self._font).grid(row=0, column=0, sticky="w", pady=3)
        self.port = tk.Spinbox(inner, from_=1024, to=65535, width=8,
                               font=self._font, justify="right")
        self.port.delete(0, "end")
        self.port.insert(0, str(DEFAULT_PORT))
        self.port.grid(row=0, column=1, sticky="w", padx=(8, 18))

        tk.Label(inner, text="Parça boyu (0=kapalı)", fg="#d5dee6",
                 bg="#18222d", font=self._font).grid(row=0, column=2, sticky="w")
        self.chunk = tk.Spinbox(inner, from_=0, to=64, width=6,
                                font=self._font, justify="right")
        self.chunk.delete(0, "end")
        self.chunk.insert(0, "8")
        self.chunk.grid(row=0, column=3, sticky="w", padx=(8, 0))

        self.var_sistem = tk.BooleanVar(value=True)
        tk.Checkbutton(
            inner, text="Sistem proxy'sini ayarla (Windows + Firefox)",
            variable=self.var_sistem, fg="#d5dee6", bg="#18222d",
            selectcolor="#10151c", activebackground="#18222d",
            activeforeground="#ffffff", font=self._font,
        ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(6, 0))

        self.var_auto = tk.BooleanVar(
            value=os.path.isfile(windows_autostart_path()))
        tk.Checkbutton(
            inner, text="Açılışta otomatik başlat",
            variable=self.var_auto, command=self._on_autostart,
            fg="#d5dee6", bg="#18222d", selectcolor="#10151c",
            activebackground="#18222d", activeforeground="#ffffff",
            font=self._font,
        ).grid(row=2, column=0, columnspan=4, sticky="w")

        bar = tk.Frame(self, bg="#10151c")
        bar.pack(fill="x", padx=16, pady=8)
        self.btn_start = tk.Button(
            bar, text="Başlat", command=self.on_start, font=self._font_b,
            bg="#26a269", fg="#ffffff", activebackground="#1e8a58",
            relief="flat", padx=14, pady=6)
        self.btn_start.pack(side="left")
        self.btn_stop = tk.Button(
            bar, text="Durdur", command=self.on_stop, font=self._font_b,
            bg="#3a4553", fg="#ffffff", activebackground="#4a5563",
            relief="flat", padx=14, pady=6, state="disabled")
        self.btn_stop.pack(side="left", padx=8)
        self.btn_tani = tk.Button(
            bar, text="Teşhis", command=self.on_tani, font=self._font_b,
            bg="#1f3a5f", fg="#ffffff", activebackground="#2d5c8a",
            relief="flat", padx=14, pady=6)
        self.btn_tani.pack(side="left")

        logcard = tk.Frame(self, bg="#10151c")
        logcard.pack(fill="both", expand=True, padx=16, pady=(0, 14))
        log_head = tk.Frame(logcard, bg="#10151c")
        log_head.pack(fill="x")
        tk.Label(log_head, text="Canlı log", fg="#f2f5f8", bg="#10151c",
                 font=self._font_b).pack(side="left")
        tk.Button(log_head, text="Temizle", command=self._on_clear,
                  font=self._font, bg="#18222d", fg="#d5dee6",
                  relief="flat").pack(side="right")
        self.log = scrolledtext.ScrolledText(
            logcard, height=12, font=self._mono, bg="#0c1116", fg="#d5dee6",
            insertbackground="#d5dee6", relief="flat", wrap="word")
        self.log.pack(fill="both", expand=True, pady=(6, 0))
        self._append("mebbypass hazır. Başlat'a basın.\n")
        self.after(1500, self._poll_log)

    def _append(self, text: str) -> None:
        self.log.insert("end", text)
        self.log.see("end")

    def _set_running(self, port: int, sistem: bool) -> None:
        self.pill.configure(text="  ÇALIŞIYOR  ", bg="#26a269")
        self.status_big.configure(text="Çalışıyor")
        self.status_sub.configure(
            text="http://127.0.0.1:%d  ·  sistem proxy %s"
            % (port, "AÇIK" if sistem else "KAPALI"))
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.port.configure(state="disabled")
        self.chunk.configure(state="disabled")

    def _set_stopped(self, note: str = "") -> None:
        self.pill.configure(text="  KAPALI  ", bg="#3a4553")
        self.status_big.configure(text="Durduruldu")
        self.status_sub.configure(
            text=note or "Başlat'a basın — 8080 doluysa yedek port seçilir")
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.port.configure(state="normal")
        self.chunk.configure(state="normal")

    def _read_ints(self):
        port = int(self.port.get())
        chunk = int(self.chunk.get())
        if not 1024 <= port <= 65535:
            raise ValueError("port")
        if not 0 <= chunk <= 64:
            raise ValueError("chunk")
        return port, chunk

    def on_start(self) -> None:
        try:
            port, chunk = self._read_ints()
        except ValueError:
            messagebox.showerror("Hata", "Port veya parça boyu geçersiz.")
            return
        sistem = bool(self.var_sistem.get())
        self.btn_start.configure(state="disabled")
        threading.Thread(target=self._worker_start,
                         args=(port, chunk, sistem), daemon=True).start()

    def _worker_start(self, port: int, chunk: int, sistem: bool) -> None:
        try:
            srv = Server(port=port, chunk=chunk, auto=True)
            srv.start()
        except AlreadyRunning as e:
            self.after(0, lambda: messagebox.showerror(
                "Hata",
                "mebbypass zaten çalışıyor (PID %d).\n"
                "DURDUR.bat ile kapatıp yeniden deneyin." % e.pid))
            self.after(0, lambda: self._set_stopped("Başlatılamadı"))
            return
        except OSError as e:
            self.after(0, lambda: messagebox.showerror(
                "Hata", "Başlatılamadı:\n%s" % e))
            self.after(0, lambda: self._set_stopped("Başlatılamadı"))
            return
        if sistem:
            set_system(srv.port, on=True)
        self.server = srv
        self.after(0, lambda: self._after_start(srv.port, sistem, srv.port != port))

    def _after_start(self, port: int, sistem: bool, fell_back: bool) -> None:
        self._set_running(port, sistem)
        self.port.configure(state="normal")
        self.port.delete(0, "end")
        self.port.insert(0, str(port))
        self.port.configure(state="disabled")
        if fell_back:
            self._append("[gui] seçilen port dolu; yedek port: %d\n" % port)
        self._append("[gui] proxy başlatıldı (port %d)\n" % port)

    def on_stop(self) -> None:
        self.btn_stop.configure(state="disabled")
        threading.Thread(target=self._worker_stop, daemon=True).start()

    def _worker_stop(self) -> None:
        srv = self.server
        if srv is None:
            self.after(0, lambda: self._set_stopped())
            return
        self.server = None
        set_system(srv.port, on=False)
        srv.stop()
        self.after(0, self._after_stop)

    def _after_stop(self) -> None:
        self._set_stopped("Durduruldu — Windows proxy ayarları geri alındı")
        self._append("[gui] proxy durduruldu, sistem ayarları geri alındı\n")

    def on_tani(self) -> None:
        self.btn_tani.configure(state="disabled")
        self._append("[gui] teşhis başlıyor (birkaç dakika sürebilir)…\n")
        threading.Thread(target=self._worker_tani, daemon=True).start()

    def _worker_tani(self) -> None:
        try:
            from .diagnosis import run_diagnosis
            path = run_diagnosis(
                progress=lambda s: self.after(
                    0, lambda msg=s: self._append("[teşhis] %s\n" % msg)))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror(
                "Hata", "Teşhis çalıştırılamadı:\n%s" % e))
            self.after(0, lambda: self.btn_tani.configure(state="normal"))
            return
        self.after(0, lambda: self._after_tani(path))

    def _after_tani(self, path: str) -> None:
        self.btn_tani.configure(state="normal")
        self._append("[teşhis] rapor: %s\n" % path)
        messagebox.showinfo(
            "Teşhis raporu hazır",
            "Rapor masaüstüne yazıldı:\n%s" % path)

    def _on_autostart(self) -> None:
        enable = bool(self.var_auto.get())
        set_windows_autostart(enable)
        self._append("[gui] açılışta otomatik başlat: %s\n"
                     % ("AÇIK" if enable else "KAPALI"))

    def _poll_log(self) -> None:
        try:
            with open(LOG_FILE, encoding="utf-8", errors="replace") as f:
                f.seek(0, os.SEEK_END)
                if f.tell() < self._log_offset:
                    self._log_offset = 0
                f.seek(self._log_offset)
                data = f.read()
                self._log_offset = f.tell()
        except OSError:
            data = ""
        if data:
            self._append(data)
        if not self._quitting:
            self.after(1500, self._poll_log)

    def _on_clear(self) -> None:
        self.log.delete("1.0", "end")
        try:
            with open(LOG_FILE, "rb") as f:
                f.seek(0, 2)
                self._log_offset = f.tell()
        except OSError:
            pass

    def on_close(self) -> None:
        srv = self.server
        if srv is not None:
            dlg = tk.Toplevel(self)
            dlg.title("mebbypass")
            dlg.configure(bg="#18222d")
            dlg.transient(self)
            dlg.grab_set()
            tk.Label(dlg, text="Proxy arka planda çalışmaya devam etsin mi?",
                     fg="#f2f5f8", bg="#18222d", font=self._font_b,
                     wraplength=360).pack(padx=16, pady=(14, 6))
            tk.Label(dlg, text="Durdur seçerseniz Windows proxy ayarı geri alınır.",
                     fg="#8aa0b4", bg="#18222d", font=self._font,
                     wraplength=360).pack(padx=16)
            choice = {"v": 0}

            def pick(v: int) -> None:
                choice["v"] = v
                dlg.destroy()

            row = tk.Frame(dlg, bg="#18222d")
            row.pack(pady=14)
            tk.Button(row, text="Devam etsin", command=lambda: pick(1),
                      bg="#26a269", fg="#ffffff", relief="flat",
                      font=self._font).pack(side="left", padx=4)
            tk.Button(row, text="Durdur ve çık", command=lambda: pick(2),
                      bg="#8a3a3a", fg="#ffffff", relief="flat",
                      font=self._font).pack(side="left", padx=4)
            tk.Button(row, text="İptal", command=lambda: pick(3),
                      bg="#3a4553", fg="#ffffff", relief="flat",
                      font=self._font).pack(side="left", padx=4)
            dlg.update_idletasks()
            x = self.winfo_rootx() + 40
            y = self.winfo_rooty() + 80
            dlg.geometry("+%d+%d" % (x, y))
            self.wait_window(dlg)
            if choice["v"] == 3 or choice["v"] == 0:
                return
            port = srv.port
            try:
                chunk = int(self.chunk.get())
            except ValueError:
                chunk = 8
            sistem = bool(self.var_sistem.get())
            if choice["v"] == 1:
                srv.stop()
                self.server = None
                try:
                    pid = spawn_background(port, chunk=chunk, sistem=sistem)
                    log("Proxy arka planda sürüyor (PID %d, port %d)"
                        % (pid, port))
                except OSError as e:
                    messagebox.showerror(
                        "Hata",
                        "Proxy arka planda başlatılamadı:\n%s" % e)
                    return
            else:
                self.server = None
                try:
                    set_system(port, on=False)
                except OSError:
                    pass
                srv.stop()
        self._quitting = True
        self.destroy()


def run() -> None:
    if not _acquire_gui_lock():
        print("mebbypass arayüzü zaten açık.", file=sys.stderr)
        return
    try:
        app = App()
        app.mainloop()
    finally:
        _release_gui_lock()
