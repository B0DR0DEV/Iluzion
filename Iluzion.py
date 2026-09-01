import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os
import time
import threading
import subprocess
import winreg
import re
import random
import webbrowser
import urllib.parse
from PIL import Image, ImageTk, ImageDraw, ImageGrab
import win32gui
import win32process
import win32api
import win32con
from pynput.keyboard import Key, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener, Button
import keyboard
import cv2
import pyautogui
import numpy as np
import pyaudio
import wave
import sys

# ---------- КОНФИГ ----------
CONFIG_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Iluzion", "Configs")
SCREENSHOTS_DIR = os.path.join(os.path.expanduser("~"), "Pictures", "Iluzion")
RECORDINGS_DIR = os.path.join(os.path.expanduser("~"), "Videos", "Iluzion")
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(RECORDINGS_DIR, exist_ok=True)

DEFAULT_CONFIG = {
    "turbo_mode": False,
    "turbo_process": "",
    "turbo_priority": "high",
    "fps_overlay": False,
    "stretch_image": False,
    "motion_blur": False,
    "motion_blur_strength": 50,
    "input_widget": False,
    "overlay_show_fps": True,
    "overlay_show_ping": True,
    "language": "en",
    "record_folder": RECORDINGS_DIR,
    "record_microphone": False,
    "crosshair_enabled": False,
    "crosshair_type": "cross",
    "crosshair_color": "#00FF00",
    "crosshair_size": 20,
    "crosshair_opacity": 100,
    "crosshair_image": "",
    "crosshair_aspect": "square",
    "crosshair_draggable": True,
    "crosshair_pos_x": None,
    "crosshair_pos_y": None,
    "crosshair_visible": True,
}

# ---------- ПЕРЕВОДЫ ----------
TEXTS = {
    "en": {
        "app_title": "🌀 Iluzion v30.0",
        "config": "Config:",
        "save": "Save",
        "new": "New",
        "delete": "Delete",
        "fps_status_off": "FPS: off",
        "fps_status_on": "FPS: on",
        "tab_turbo": "Turbo",
        "tab_quality": "Quality",
        "tab_tools": "Tools",
        "tab_record": "Record",
        "tab_crosshair": "Crosshair",
        "tab_feedback": "Feedback",
        "tab_language": "Language",
        "turbo": "Turbo Mode",
        "turbo_desc": "Increase priority of selected window",
        "turbo_select": "Select window:",
        "refresh": "Refresh",
        "priority": "Priority:",
        "priority_high": "High",
        "priority_normal": "Normal",
        "stretch": "Stretch Image",
        "stretch_desc": "Like in CS:GO",
        "motion_blur": "Motion Blur",
        "motion_blur_desc": "Blur on fast movement",
        "motion_blur_strength": "Strength:",
        "overlay": "Overlay (FPS + Ping)",
        "overlay_desc": "Show FPS and ping",
        "overlay_settings": "Overlay settings:",
        "input_widget": "Input Widget",
        "input_widget_desc": "Show keys and mouse clicks",
        "screenshot": "Screenshot (3s)",
        "screenshot_desc": "Click → countdown → screenshot",
        "record": "Record Screen",
        "record_desc": "Record screen with audio",
        "record_start": "▶️ Start Recording",
        "record_stop": "⏹️ Stop Recording",
        "record_folder": "Save folder:",
        "record_browse": "Browse",
        "record_microphone": "🎤 Record Microphone",
        "crosshair": "Crosshair Overlay",
        "crosshair_desc": "Custom crosshair on top of all windows",
        "crosshair_type": "Type:",
        "crosshair_type_cross": "Cross",
        "crosshair_type_dot": "Dot",
        "crosshair_type_circle": "Circle",
        "crosshair_type_triangle": "Triangle",
        "crosshair_type_custom": "Custom Image/Video",
        "crosshair_color": "Color:",
        "crosshair_size": "Size:",
        "crosshair_opacity": "Opacity:",
        "crosshair_image": "Image/Video:",
        "crosshair_browse": "Browse",
        "crosshair_aspect": "Aspect Ratio:",
        "crosshair_aspect_square": "Square",
        "crosshair_aspect_16_9": "16:9",
        "crosshair_aspect_4_3": "4:3",
        "crosshair_draggable": "Draggable",
        "crosshair_reset_pos": "Reset Position",
        "crosshair_hide_hotkey": "Alt+Q - Hide/Show",
        "apply": "▶️ Apply All",
        "stop": "⏹️ Stop All",
        "rollback": "🔴 Emergency Rollback",
        "rollback_hotkey": "Ctrl+J",
        "status_ready": "Ready. Ctrl+J — rollback",
        "status_hotkey_error": "Ctrl+J not registered",
        "history": "Last used:",
        "no_history": "No history",
        "turbo_history": "Turbo Mode",
        "overlay_history": "FPS Overlay",
        "stretch_history": "Stretch",
        "motion_history": "Motion Blur",
        "input_history": "Input Widget",
        "crosshair_history": "Crosshair",
        "screenshot_ready": "3... 2... 1...",
        "screenshot_saved": "Screenshot saved:",
        "screenshot_error": "Screenshot error",
        "screenshot_success": "Success",
        "screenshot_saved_msg": "Screenshot saved in:",
        "rollback_confirm": "Emergency rollback",
        "rollback_confirm_msg": "Revert all settings?",
        "rollback_done": "Rollback done!",
        "rollback_result": "All settings reverted!\n",
        "apply_done": "Done!",
        "stop_done": "All functions stopped!",
        "record_starting": "Recording started...",
        "record_started": "🔴 Recording... Click 'Stop' to save",
        "record_stopped": "✅ Recording saved:",
        "record_error": "❌ Recording error",
        "record_success": "Success",
        "record_saved_msg": "Video saved in:",
        "record_folder_changed": "Folder changed:",
        "feedback_title": "📩 Send Feedback",
        "feedback_desc": "Write your ideas, suggestions or bug reports:",
        "feedback_send": "📤 Send",
        "feedback_clear": "🗑 Clear",
        "feedback_success": "Thank you! Form opened in your browser.",
        "feedback_error": "Could not open form.",
        "feedback_placeholder": "Write your feedback here...",
        "under_development": "🚧 Under Development\nScreen recording will be available in future updates",
        "start": "🚀 Start",
        "video_error": "Video error",
        "crosshair_hidden": "Crosshair hidden",
        "crosshair_shown": "Crosshair shown",
    },
    "ru": {
        "app_title": "🌀 Iluzion v30.0",
        "config": "Конфиг:",
        "save": "Сохранить",
        "new": "Новый",
        "delete": "Удалить",
        "fps_status_off": "FPS: выкл",
        "fps_status_on": "FPS: вкл",
        "tab_turbo": "Турбо",
        "tab_quality": "Качество",
        "tab_tools": "Инструменты",
        "tab_record": "Запись",
        "tab_crosshair": "Прицел",
        "tab_feedback": "Обратная связь",
        "tab_language": "Язык",
        "turbo": "Турбо-режим",
        "turbo_desc": "Повысить приоритет окна",
        "turbo_select": "Выберите окно:",
        "refresh": "Обновить",
        "priority": "Приоритет:",
        "priority_high": "Высокий",
        "priority_normal": "Обычный",
        "stretch": "Растяжение",
        "stretch_desc": "Как в CS:GO",
        "motion_blur": "Размытие",
        "motion_blur_desc": "При быстром движении",
        "motion_blur_strength": "Сила:",
        "overlay": "Оверлей (FPS + Пинг)",
        "overlay_desc": "Показывать поверх окон",
        "overlay_settings": "Настройки оверлея:",
        "input_widget": "Виджет ввода",
        "input_widget_desc": "Клавиши и мышь",
        "screenshot": "Скриншот (3с)",
        "screenshot_desc": "Нажми → отсчёт → скриншот",
        "record": "Запись экрана",
        "record_desc": "Запись с аудио",
        "record_start": "▶️ Начать запись",
        "record_stop": "⏹️ Остановить",
        "record_folder": "Папка:",
        "record_browse": "Обзор",
        "record_microphone": "🎤 Запись микрофона",
        "crosshair": "Прицел поверх всех окон",
        "crosshair_desc": "Настраиваемый прицел поверх игры",
        "crosshair_type": "Тип:",
        "crosshair_type_cross": "Крестик",
        "crosshair_type_dot": "Точка",
        "crosshair_type_circle": "Круг",
        "crosshair_type_triangle": "Треугольник",
        "crosshair_type_custom": "Изображение/Видео",
        "crosshair_color": "Цвет:",
        "crosshair_size": "Размер:",
        "crosshair_opacity": "Прозрачность:",
        "crosshair_image": "Изображение/Видео:",
        "crosshair_browse": "Обзор",
        "crosshair_aspect": "Соотношение:",
        "crosshair_aspect_square": "Квадрат",
        "crosshair_aspect_16_9": "16:9",
        "crosshair_aspect_4_3": "4:3",
        "crosshair_draggable": "Перемещаемый",
        "crosshair_reset_pos": "Сброс позиции",
        "crosshair_hide_hotkey": "Alt+Q - Скрыть/Показать",
        "apply": "▶️ Запустить",
        "stop": "⏹️ Остановить",
        "rollback": "🔴 Аварийный откат",
        "rollback_hotkey": "Ctrl+J",
        "status_ready": "Готов. Ctrl+J — откат",
        "status_hotkey_error": "Ctrl+J не зарегистрирован",
        "history": "Последние использованные:",
        "no_history": "Нет истории",
        "turbo_history": "Турбо-режим",
        "overlay_history": "FPS-оверлей",
        "stretch_history": "Растяжение",
        "motion_history": "Motion Blur",
        "input_history": "Виджет ввода",
        "crosshair_history": "Прицел",
        "screenshot_ready": "3... 2... 1...",
        "screenshot_saved": "Скриншот сохранён:",
        "screenshot_error": "Ошибка скриншота",
        "screenshot_success": "Успех",
        "screenshot_saved_msg": "Скриншот сохранён в:",
        "rollback_confirm": "Аварийный откат",
        "rollback_confirm_msg": "Вернуть все настройки?",
        "rollback_done": "Откат выполнен!",
        "rollback_result": "Все настройки возвращены!\n",
        "apply_done": "Готово!",
        "stop_done": "Все функции остановлены!",
        "record_starting": "Запись запущена...",
        "record_started": "🔴 Идёт запись... Нажми 'Остановить'",
        "record_stopped": "✅ Запись сохранена:",
        "record_error": "❌ Ошибка записи",
        "record_success": "Успех",
        "record_saved_msg": "Видео сохранено в:",
        "record_folder_changed": "Папка изменена:",
        "feedback_title": "📩 Обратная связь",
        "feedback_desc": "Напишите идеи, предложения или сообщите о багах:",
        "feedback_send": "📤 Отправить",
        "feedback_clear": "🗑 Очистить",
        "feedback_success": "Спасибо! Форма открыта в браузере.",
        "feedback_error": "Не удалось открыть форму.",
        "feedback_placeholder": "Напишите здесь...",
        "under_development": "🚧 В разработке\nФункция записи экрана появится в следующих обновлениях",
        "start": "🚀 Начать",
        "video_error": "Ошибка видео",
        "crosshair_hidden": "Прицел скрыт",
        "crosshair_shown": "Прицел показан",
    }
}

# ---------- ЗАКРУГЛЁННАЯ КНОПКА ----------
class RoundedButton(tk.Canvas):
    def __init__(self, master=None, text="", command=None, bg="#E94560", fg="white",
                 font=('Segoe UI', 10, 'bold'), padx=15, pady=8, radius=12, **kwargs):
        self.command = command
        self.text = text
        self.bg = bg
        self.fg = fg
        self.font = font
        self.padx = padx
        self.pady = pady
        self.radius = radius
        self.hover = False
        self._disabled = False
        
        temp_label = tk.Label(master, text=text, font=font)
        temp_label.update_idletasks()
        self.text_width = temp_label.winfo_reqwidth()
        self.text_height = temp_label.winfo_reqheight()
        temp_label.destroy()
        
        width = self.text_width + padx * 2
        height = self.text_height + pady * 2
        
        super().__init__(master, width=width, height=height, highlightthickness=0, bd=0, bg='#1A1A2E')
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Configure>", self._draw)
        self._draw()
    
    def _draw(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        r = self.radius
        
        color = self.bg
        if self._disabled:
            color = '#555'
        elif self.hover:
            color = self._lighten_color(self.bg, 30)
        
        self.create_arc((0, 0, r*2, r*2), start=90, extent=90, fill=color, outline=color)
        self.create_arc((w-r*2, 0, w, r*2), start=0, extent=90, fill=color, outline=color)
        self.create_arc((0, h-r*2, r*2, h), start=180, extent=90, fill=color, outline=color)
        self.create_arc((w-r*2, h-r*2, w, h), start=270, extent=90, fill=color, outline=color)
        
        self.create_rectangle((r, 0, w-r, h), fill=color, outline=color)
        self.create_rectangle((0, r, w, h-r), fill=color, outline=color)
        
        text_color = '#888' if self._disabled else self.fg
        self.create_text(w/2, h/2, text=self.text, fill=text_color, font=self.font)
    
    def _lighten_color(self, color, amount):
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = min(255, r + amount)
            g = min(255, g + amount)
            b = min(255, b + amount)
            return f'#{r:02x}{g:02x}{b:02x}'
        return color
    
    def _on_click(self, event):
        if not self._disabled and self.command:
            self.command()
    
    def _on_enter(self, event):
        self.hover = True
        self._draw()
    
    def _on_leave(self, event):
        self.hover = False
        self._draw()
    
    def config(self, **kwargs):
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'bg' in kwargs:
            self.bg = kwargs['bg']
        if 'fg' in kwargs:
            self.fg = kwargs['fg']
        if 'state' in kwargs:
            self._disabled = (kwargs['state'] == 'disabled')
            if self._disabled:
                self['cursor'] = 'arrow'
            else:
                self['cursor'] = 'hand2'
        self._draw()
    
    def configure(self, **kwargs):
        self.config(**kwargs)

# ---------- КЛАСС ЗАПИСИ ЭКРАНА ----------
class ScreenRecorder:
    def __init__(self, fps=30, quality="medium", record_mic=False, save_folder=None):
        self.fps = fps
        self.quality = quality
        self.record_mic = record_mic
        self.save_folder = save_folder or RECORDINGS_DIR
        self.recording = False
        self.audio_frames = []
        self.thread = None
        self.video_writer = None
        self.temp_file = None
        self.start_time = None
        self.frame_count = 0
        self.audio_stream = None
        self.audio = None
        
    def start_recording(self):
        self.recording = True
        self.frame_count = 0
        self.audio_frames = []
        self.start_time = time.time()
        
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.temp_file = os.path.join(self.save_folder, f"temp_{timestamp}.mp4")
        
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(
            self.temp_file, 
            fourcc, 
            self.fps, 
            (screen_size.width, screen_size.height)
        )
        
        self.thread = threading.Thread(target=self._record, daemon=True)
        self.thread.start()
        
        if self.record_mic:
            self._start_audio()
    
    def _start_audio(self):
        try:
            self.audio = pyaudio.PyAudio()
            self.audio_stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024
            )
            self.audio_recording = True
            audio_thread = threading.Thread(target=self._record_audio, daemon=True)
            audio_thread.start()
        except:
            pass
    
    def _record_audio(self):
        while self.recording and hasattr(self, 'audio_recording') and self.audio_recording:
            try:
                data = self.audio_stream.read(1024, exception_on_overflow=False)
                self.audio_frames.append(data)
            except:
                pass
    
    def _record(self):
        while self.recording:
            try:
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                self.video_writer.write(frame)
                self.frame_count += 1
                
                expected_time = self.frame_count / self.fps
                actual_time = time.time() - self.start_time
                if actual_time < expected_time:
                    time.sleep(expected_time - actual_time)
            except:
                pass
        
        if self.video_writer:
            self.video_writer.release()
    
    def stop_recording(self):
        self.recording = False
        if hasattr(self, 'audio_recording'):
            self.audio_recording = False
            if hasattr(self, 'audio_stream') and self.audio_stream:
                try:
                    self.audio_stream.stop_stream()
                    self.audio_stream.close()
                except:
                    pass
            if hasattr(self, 'audio') and self.audio:
                try:
                    self.audio.terminate()
                except:
                    pass
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        
        return self._post_process()
    
    def _post_process(self):
        if self.record_mic and self.audio_frames:
            return self._merge_audio_video()
        else:
            final_file = self.temp_file.replace("temp_", "recording_")
            if os.path.exists(self.temp_file):
                os.rename(self.temp_file, final_file)
                return final_file
            return None
    
    def _merge_audio_video(self):
        audio_file = self.temp_file.replace(".mp4", "_audio.wav")
        try:
            wf = wave.open(audio_file, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.audio_frames))
            wf.close()
        except:
            pass
        
        try:
            final_file = self.temp_file.replace("temp_", "recording_")
            subprocess.run([
                'ffmpeg', '-i', self.temp_file, '-i', audio_file,
                '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0',
                '-shortest', final_file, '-y'
            ], capture_output=True, check=False, creationflags=subprocess.CREATE_NO_WINDOW)
            
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
            if os.path.exists(audio_file):
                os.remove(audio_file)
                
            if os.path.exists(final_file):
                return final_file
        except:
            pass
        
        final_file = self.temp_file.replace("temp_", "recording_")
        if os.path.exists(self.temp_file):
            os.rename(self.temp_file, final_file)
            return final_file
        return None

# ---------- КЛАСС ПРИЦЕЛА ----------
class CrosshairOverlay:
    def __init__(self, crosshair_type="cross", color="#00FF00", size=20, opacity=100, 
                 image_path="", aspect="square", draggable=True):
        self.opacity = opacity / 100.0
        self.aspect = aspect
        self.draggable = draggable
        self.visible = True
        self.type = crosshair_type
        self.color = color
        self.size = size
        self.image_path = image_path
        self.custom_image = None
        self.video_cap = None
        self.video_thread = None
        self.video_running = False
        
        self.window = tk.Toplevel()
        self.window.title("Iluzion Crosshair")
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)
        self.window.wm_attributes("-transparentcolor", "black")
        self.window.configure(bg='black')
        
        self.update_window_size()
        self.window.attributes("-alpha", self.opacity)
        
        if not self.draggable:
            self.window.attributes("-disabled", True)
        
        self.canvas = tk.Canvas(self.window, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        if self.draggable:
            self.canvas.bind("<Button-1>", self.start_move)
            self.canvas.bind("<B1-Motion>", self.on_move)
        
        self.draw_crosshair()
        self.center_window()
        self.window.update()
        self.running = True
    
    def update_window_size(self):
        base = self.size * 3
        if self.aspect == "16_9":
            w = int(base * 1.78)
            h = base
        elif self.aspect == "4_3":
            w = int(base * 1.33)
            h = base
        else:
            w = base
            h = base
        self.window.geometry(f"{w}x{h}")
    
    def center_window(self):
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        w = self.window.winfo_width()
        h = self.window.winfo_height()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.window.geometry(f"+{x}+{y}")
    
    def draw_crosshair(self):
        self.canvas.delete("all")
        
        w = self.window.winfo_width()
        h = self.window.winfo_height()
        cx = w // 2
        cy = h // 2
        
        if self.type == "custom" and self.image_path and os.path.exists(self.image_path):
            ext = os.path.splitext(self.image_path)[1].lower()
            if ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.gif']:
                self._load_video()
                return
            elif ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                try:
                    img = Image.open(self.image_path)
                    img = img.resize((w, h), Image.Resampling.LANCZOS)
                    self.custom_image = ImageTk.PhotoImage(img)
                    self.canvas.create_image(cx, cy, image=self.custom_image)
                    return
                except:
                    pass
        
        size = self.size
        if self.type == "cross":
            self.canvas.create_line(cx - size, cy, cx + size, cy, fill=self.color, width=2)
            self.canvas.create_line(cx, cy - size, cx, cy + size, fill=self.color, width=2)
        elif self.type == "dot":
            self.canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill=self.color, outline=self.color)
        elif self.type == "circle":
            r = size // 2
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=self.color, width=2)
        elif self.type == "triangle":
            self.canvas.create_polygon(cx, cy - size, cx - size, cy + size, cx + size, cy + size, 
                                      outline=self.color, fill='', width=2)
    
    def _load_video(self):
        try:
            self._stop_video()
            self.video_cap = cv2.VideoCapture(self.image_path)
            if not self.video_cap.isOpened():
                return
            self.video_running = True
            self.video_thread = threading.Thread(target=self._play_video, daemon=True)
            self.video_thread.start()
        except:
            pass
    
    def _play_video(self):
        while self.video_running and self.video_cap is not None:
            try:
                ret, frame = self.video_cap.read()
                if not ret:
                    self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                w = self.window.winfo_width()
                h = self.window.winfo_height()
                img = img.resize((w, h), Image.Resampling.LANCZOS)
                self.custom_image = ImageTk.PhotoImage(img)
                self.window.after(0, self._update_video_frame)
                time.sleep(1/30)
            except:
                break
    
    def _update_video_frame(self):
        try:
            w = self.window.winfo_width()
            h = self.window.winfo_height()
            cx = w // 2
            cy = h // 2
            self.canvas.delete("all")
            if self.custom_image:
                self.canvas.create_image(cx, cy, image=self.custom_image)
        except:
            pass
    
    def _stop_video(self):
        self.video_running = False
        if self.video_thread and self.video_thread.is_alive():
            self.video_thread.join(timeout=1)
        if self.video_cap:
            self.video_cap.release()
            self.video_cap = None
        self.custom_image = None
        self.canvas.delete("all")
    
    def update_settings(self, crosshair_type=None, color=None, size=None, opacity=None, 
                        image_path=None, aspect=None, draggable=None):
        if crosshair_type is not None:
            self.type = crosshair_type
            if self.type != "custom":
                self._stop_video()
        if color is not None:
            self.color = color
        if size is not None:
            self.size = size
            self.update_window_size()
        if opacity is not None:
            self.opacity = opacity / 100.0
            self.window.attributes("-alpha", self.opacity)
        if image_path is not None:
            self._stop_video()
            self.image_path = image_path
        if aspect is not None:
            self.aspect = aspect
            self.update_window_size()
        if draggable is not None:
            self.draggable = draggable
            if not draggable:
                self.window.attributes("-disabled", True)
            else:
                self.window.attributes("-disabled", False)
        self.draw_crosshair()
        self.center_window()
        self.window.update()
    
    def toggle_visibility(self):
        self.visible = not self.visible
        if self.visible:
            self.window.deiconify()
        else:
            self.window.withdraw()
        return self.visible
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        if not self.draggable:
            return
        x = self.window.winfo_x() + (event.x - self.x)
        y = self.window.winfo_y() + (event.y - self.y)
        self.window.geometry(f"+{x}+{y}")
    
    def reset_position(self):
        self.center_window()
    
    def close(self):
        self.running = False
        self._stop_video()
        try:
            self.window.destroy()
        except:
            pass
    
    def is_running(self):
        return self.running

# ---------- ВИДЖЕТ МЫШИ ----------
class MouseWidget:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Iluzion Mouse")
        self.window.geometry("100x130")
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)
        self.window.wm_attributes("-transparentcolor", "black")
        self.window.configure(bg='black')
        self.window.attributes("-alpha", 0.85)
        
        screen_width = self.window.winfo_screenwidth()
        self.window.geometry(f"100x130+{screen_width-120}+400")
        
        self.canvas = tk.Canvas(self.window, width=90, height=120, bg='black', highlightthickness=0)
        self.canvas.pack(pady=5)
        
        self.canvas.create_oval(20, 35, 70, 85, fill='#555', outline='#888', width=2)
        self.canvas.create_rectangle(25, 35, 65, 75, fill='#555', outline='#888', width=1)
        
        self.left_btn = self.canvas.create_rectangle(26, 40, 48, 60, fill='#444', outline='#888', width=1)
        self.right_btn = self.canvas.create_rectangle(52, 40, 74, 60, fill='#444', outline='#888', width=1)
        self.middle_btn = self.canvas.create_rectangle(39, 30, 51, 38, fill='#444', outline='#888', width=1)
        
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.on_move)
        
        self.running = True
        self.mouse_listener = MouseListener(on_click=self.on_click)
        self.mouse_listener.start()
        
        close_btn = tk.Label(self.window, text="✕", font=('Segoe UI', 10, 'bold'),
                             fg='#888', bg='black', cursor='hand2')
        close_btn.place(x=80, y=5)
        close_btn.bind("<Button-1>", lambda e: self.close())
        
        self.window.protocol("WM_DELETE_WINDOW", self.close)
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry(f"+{x}+{y}")
    
    def on_click(self, x, y, button, pressed):
        if not self.running:
            return
        try:
            if pressed:
                if button == Button.left:
                    self.canvas.itemconfig(self.left_btn, fill='#FF6B6B')
                    self.canvas.itemconfig(self.right_btn, fill='#444')
                    self.canvas.itemconfig(self.middle_btn, fill='#444')
                elif button == Button.right:
                    self.canvas.itemconfig(self.right_btn, fill='#FF6B6B')
                    self.canvas.itemconfig(self.left_btn, fill='#444')
                    self.canvas.itemconfig(self.middle_btn, fill='#444')
                elif button == Button.middle:
                    self.canvas.itemconfig(self.middle_btn, fill='#FF6B6B')
                    self.canvas.itemconfig(self.left_btn, fill='#444')
                    self.canvas.itemconfig(self.right_btn, fill='#444')
            else:
                self.canvas.itemconfig(self.left_btn, fill='#444')
                self.canvas.itemconfig(self.right_btn, fill='#444')
                self.canvas.itemconfig(self.middle_btn, fill='#444')
        except:
            pass
    
    def close(self):
        self.running = False
        try:
            self.mouse_listener.stop()
        except:
            pass
        try:
            self.window.destroy()
        except:
            pass
    
    def is_running(self):
        return self.running

# ---------- ВИДЖЕТ КЛАВИШ ----------
class KeyWidget:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Iluzion Keys")
        self.window.geometry("220x140")
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)
        self.window.wm_attributes("-transparentcolor", "black")
        self.window.configure(bg='black')
        self.window.attributes("-alpha", 0.85)
        
        screen_width = self.window.winfo_screenwidth()
        self.window.geometry(f"220x140+{screen_width-240}+300")
        
        self.canvas = tk.Canvas(self.window, width=200, height=120, bg='black', highlightthickness=0)
        self.canvas.pack(pady=5)
        
        # WASD
        self.w_rect = self.canvas.create_rectangle(85, 10, 115, 38, fill='#333', outline='#555', width=1)
        self.w_text = self.canvas.create_text(100, 24, text="W", fill='#888', font=('Segoe UI', 10, 'bold'))
        
        self.a_rect = self.canvas.create_rectangle(50, 40, 80, 68, fill='#333', outline='#555', width=1)
        self.a_text = self.canvas.create_text(65, 54, text="A", fill='#888', font=('Segoe UI', 10, 'bold'))
        
        self.s_rect = self.canvas.create_rectangle(85, 40, 115, 68, fill='#333', outline='#555', width=1)
        self.s_text = self.canvas.create_text(100, 54, text="S", fill='#888', font=('Segoe UI', 10, 'bold'))
        
        self.d_rect = self.canvas.create_rectangle(120, 40, 150, 68, fill='#333', outline='#555', width=1)
        self.d_text = self.canvas.create_text(135, 54, text="D", fill='#888', font=('Segoe UI', 10, 'bold'))
        
        # Ctrl
        self.ctrl_rect = self.canvas.create_rectangle(10, 70, 65, 98, fill='#333', outline='#555', width=1)
        self.ctrl_text = self.canvas.create_text(37, 84, text="CTRL", fill='#888', font=('Segoe UI', 8, 'bold'))
        
        # Shift
        self.shift_rect = self.canvas.create_rectangle(135, 70, 190, 98, fill='#333', outline='#555', width=1)
        self.shift_text = self.canvas.create_text(162, 84, text="SHIFT", fill='#888', font=('Segoe UI', 8, 'bold'))
        
        # Space
        self.space_rect = self.canvas.create_rectangle(65, 100, 135, 118, fill='#333', outline='#555', width=1)
        self.space_text = self.canvas.create_text(100, 109, text="SPACE", fill='#888', font=('Segoe UI', 7, 'bold'))
        
        # Русская раскладка
        self.ru_to_en = {
            'ц': 'w', 'W': 'w',
            'ф': 'a', 'F': 'a',
            'ы': 's', 'Y': 's',
            'в': 'd', 'V': 'd',
        }
        
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.on_move)
        
        self.running = True
        self.keyboard_listener = KeyboardListener(on_press=self.on_press, on_release=self.on_release)
        self.keyboard_listener.start()
        
        close_btn = tk.Label(self.window, text="✕", font=('Segoe UI', 10, 'bold'),
                             fg='#888', bg='black', cursor='hand2')
        close_btn.place(x=195, y=5)
        close_btn.bind("<Button-1>", lambda e: self.close())
        
        self.window.protocol("WM_DELETE_WINDOW", self.close)
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry(f"+{x}+{y}")
    
    def on_press(self, key):
        try:
            if key == Key.space:
                self.highlight_key('space', True)
            elif key == Key.shift:
                self.highlight_key('shift', True)
            elif key == Key.ctrl:
                self.highlight_key('ctrl', True)
            elif hasattr(key, 'char') and key.char:
                char = key.char
                if char.lower() in ['w', 'a', 's', 'd']:
                    self.highlight_key(char.lower(), True)
                elif char in self.ru_to_en:
                    self.highlight_key(self.ru_to_en[char], True)
        except:
            pass
    
    def on_release(self, key):
        try:
            if key == Key.space:
                self.highlight_key('space', False)
            elif key == Key.shift:
                self.highlight_key('shift', False)
            elif key == Key.ctrl:
                self.highlight_key('ctrl', False)
            elif hasattr(key, 'char') and key.char:
                char = key.char
                if char.lower() in ['w', 'a', 's', 'd']:
                    self.highlight_key(char.lower(), False)
                elif char in self.ru_to_en:
                    self.highlight_key(self.ru_to_en[char], False)
        except:
            pass
    
    def highlight_key(self, key, pressed):
        color = '#4CAF50' if pressed else '#333'
        text_color = '#FFF' if pressed else '#888'
        
        if key == 'w':
            self.canvas.itemconfig(self.w_rect, fill=color)
            self.canvas.itemconfig(self.w_text, fill=text_color)
        elif key == 'a':
            self.canvas.itemconfig(self.a_rect, fill=color)
            self.canvas.itemconfig(self.a_text, fill=text_color)
        elif key == 's':
            self.canvas.itemconfig(self.s_rect, fill=color)
            self.canvas.itemconfig(self.s_text, fill=text_color)
        elif key == 'd':
            self.canvas.itemconfig(self.d_rect, fill=color)
            self.canvas.itemconfig(self.d_text, fill=text_color)
        elif key == 'ctrl':
            self.canvas.itemconfig(self.ctrl_rect, fill=color)
            self.canvas.itemconfig(self.ctrl_text, fill=text_color)
        elif key == 'shift':
            self.canvas.itemconfig(self.shift_rect, fill=color)
            self.canvas.itemconfig(self.shift_text, fill=text_color)
        elif key == 'space':
            self.canvas.itemconfig(self.space_rect, fill=color)
            self.canvas.itemconfig(self.space_text, fill=text_color)
    
    def close(self):
        self.running = False
        try:
            self.keyboard_listener.stop()
        except:
            pass
        try:
            self.window.destroy()
        except:
            pass
    
    def is_running(self):
        return self.running

# ---------- FPS ОВЕРЛЕЙ ----------
class FPSOverlay:
    def __init__(self, show_fps=True, show_ping=True):
        self.window = tk.Toplevel()
        self.window.title("Iluzion FPS")
        self.window.geometry("200x80")
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)
        self.window.wm_attributes("-transparentcolor", "black")
        self.window.configure(bg='black')
        self.window.attributes("-alpha", 0.85)

        screen_width = self.window.winfo_screenwidth()
        self.window.geometry(f"210x90+{screen_width-230}+30")

        self.line_fps = tk.Frame(self.window, bg='black')
        self.line_fps.pack(anchor='w', padx=10, pady=(5,0))

        self.fps_label = tk.Label(
            self.line_fps,
            text="FPS: 0",
            font=('Segoe UI', 14, 'bold'),
            fg='#00FF00',
            bg='black'
        )
        self.fps_label.pack(side='left')

        self.line_ping = tk.Frame(self.window, bg='black')
        self.line_ping.pack(anchor='w', padx=10)

        self.ping_label = tk.Label(
            self.line_ping,
            text="Пинг: 0 мс",
            font=('Segoe UI', 12),
            fg='#FFD700',
            bg='black'
        )
        self.ping_label.pack(side='left')

        self.settings_visible = False
        self.settings_menu = None

        settings_btn = tk.Label(
            self.window,
            text="▼",
            font=('Segoe UI', 10, 'bold'),
            fg='#888',
            bg='black',
            cursor='hand2'
        )
        settings_btn.place(x=180, y=5)
        settings_btn.bind("<Button-1>", self.toggle_settings)

        close_btn = tk.Label(
            self.window,
            text="✕",
            font=('Segoe UI', 10, 'bold'),
            fg='#888',
            bg='black',
            cursor='hand2'
        )
        close_btn.place(x=195, y=5)
        close_btn.bind("<Button-1>", lambda e: self.close())

        self.show_fps = show_fps
        self.show_ping = show_ping

        self.fps_label.bind("<Button-1>", self.start_move)
        self.fps_label.bind("<B1-Motion>", self.on_move)
        self.window.bind("<Button-1>", self.start_move)
        self.window.bind("<B1-Motion>", self.on_move)

        self.running = True
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

        self.apply_visibility()

    def toggle_settings(self, event):
        if self.settings_visible:
            if self.settings_menu:
                self.settings_menu.destroy()
            self.settings_visible = False
            return

        self.settings_menu = tk.Toplevel(self.window)
        self.settings_menu.title("Настройки оверлея")
        self.settings_menu.geometry("150x120")
        self.settings_menu.configure(bg='#1A1A2E')
        self.settings_menu.overrideredirect(True)
        self.settings_menu.wm_attributes("-topmost", True)
        self.settings_menu.resizable(False, False)

        x = self.window.winfo_x() + 170
        y = self.window.winfo_y() + 25
        self.settings_menu.geometry(f"150x120+{x}+{y}")

        tk.Label(self.settings_menu, text="Показывать:", bg='#1A1A2E', fg='#E94560', 
                 font=('Segoe UI', 10, 'bold')).pack(pady=(10, 5))

        self.check_vars = {}
        for text, var, cmd in [
            ("FPS", self.show_fps, self.toggle_show_fps),
            ("Пинг", self.show_ping, self.toggle_show_ping),
        ]:
            var_obj = tk.BooleanVar(value=var)
            self.check_vars[text] = var_obj
            cb = tk.Checkbutton(self.settings_menu, text=text, variable=var_obj,
                                bg='#1A1A2E', fg='white', selectcolor='#1A1A2E',
                                font=('Segoe UI', 9), command=cmd)
            cb.pack(anchor='w', padx=20, pady=2)

        self.settings_visible = True

    def toggle_show_fps(self):
        self.show_fps = not self.show_fps
        self.apply_visibility()

    def toggle_show_ping(self):
        self.show_ping = not self.show_ping
        self.apply_visibility()

    def apply_visibility(self):
        if self.show_fps:
            self.line_fps.pack(anchor='w', padx=10, pady=(5,0))
        else:
            self.line_fps.pack_forget()

        if self.show_ping:
            self.line_ping.pack(anchor='w', padx=10)
        else:
            self.line_ping.pack_forget()

        self.window.update()
        self.window.geometry("")

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry(f"+{x}+{y}")

    def get_ping_safe(self):
        try:
            result = subprocess.run(
                ['ping', '-n', '1', '8.8.8.8'],
                capture_output=True,
                text=True,
                timeout=2,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                match = re.search(r'<(\d+)ms', result.stdout)
                if match:
                    return int(match.group(1))
            return 0
        except:
            return 0

    def update(self):
        last_time = time.time()
        frame_count = 0
        last_fps = 0
        hwnd = None
        
        while self.running:
            try:
                if hwnd is None or not win32gui.IsWindow(hwnd):
                    hwnd = win32gui.FindWindow(None, "Roblox")
                    if not hwnd:
                        hwnd = win32gui.FindWindow(None, "RobloxPlayerBeta")
                
                if hwnd and win32gui.IsWindowVisible(hwnd):
                    rect = win32gui.GetWindowRect(hwnd)
                    if rect is not None:
                        frame_count += 1
                        current_time = time.time()
                        if current_time - last_time >= 1.0:
                            last_fps = frame_count
                            frame_count = 0
                            last_time = current_time
                            self.fps_label.config(text=f"FPS: {last_fps}", fg='#00FF00')
                else:
                    self.fps_label.config(text="Roblox не найден", fg='#888')
                    last_time = time.time()
                    frame_count = 0
                
                ping = self.get_ping_safe()
                if ping > 0:
                    self.ping_label.config(text=f"Пинг: {ping} мс", fg='#FFD700' if ping < 50 else '#FF4444')
                else:
                    self.ping_label.config(text="Пинг: ---", fg='#888')
                
                time.sleep(0.1)
            except:
                time.sleep(0.1)

    def get_settings(self):
        return {
            'show_fps': self.show_fps,
            'show_ping': self.show_ping,
        }

    def close(self):
        self.running = False
        if self.settings_menu:
            self.settings_menu.destroy()
        try:
            self.window.destroy()
        except:
            pass

    def is_running(self):
        return self.running

# ---------- РАЗМЫТИЕ ПРИ ДВИЖЕНИИ ----------
class MotionBlurOverlay:
    def __init__(self, strength=50):
        self.strength = strength
        self.window = tk.Toplevel()
        self.window.title("Iluzion Motion Blur")
        self.window.geometry(f"{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()}+0+0")
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)
        self.window.wm_attributes("-transparentcolor", "black")
        self.window.configure(bg='black')
        self.window.attributes("-alpha", 0.0)
        
        try:
            hwnd = win32gui.FindWindow(None, "Iluzion Motion Blur")
            if hwnd:
                ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_TRANSPARENT)
        except:
            pass
        
        self.running = True
        self.blur_intensity = 0.0
        self.max_blur = strength / 100.0 * 0.5
        
        self.last_x = None
        self.last_y = None
        self.speed = 0
        
        self.window.bind("<Motion>", self.on_mouse_move)
        
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()
    
    def on_mouse_move(self, event):
        if self.last_x is None:
            self.last_x = event.x_root
            self.last_y = event.y_root
            return
        
        dx = event.x_root - self.last_x
        dy = event.y_root - self.last_y
        self.speed = (dx**2 + dy**2) ** 0.5
        
        self.last_x = event.x_root
        self.last_y = event.y_root
    
    def update(self):
        while self.running:
            try:
                if self.speed > 30:
                    self.blur_intensity = min(self.max_blur, self.blur_intensity + 0.02)
                else:
                    self.blur_intensity = max(0.0, self.blur_intensity - 0.02)
                
                self.window.attributes("-alpha", self.blur_intensity)
                self.speed = max(0, self.speed - 5)
                time.sleep(0.02)
            except:
                time.sleep(0.02)
    
    def set_strength(self, strength):
        self.max_blur = strength / 100.0 * 0.5
    
    def close(self):
        self.running = False
        try:
            self.window.destroy()
        except:
            pass
    
    def is_running(self):
        return self.running

# ---------- БЕЗОПАСНЫЕ ФУНКЦИИ ----------
def get_open_windows():
    windows = []
    def enum_windows_callback(hwnd, windows_list):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows_list.append((hwnd, title))
        return True
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def set_process_priority_by_window(hwnd, priority="high"):
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
        if priority == "high":
            win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)
        elif priority == "normal":
            win32process.SetPriorityClass(handle, win32process.NORMAL_PRIORITY_CLASS)
        win32api.CloseHandle(handle)
        return True
    except:
        return False

def reset_process_priority_by_window(hwnd):
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
        win32process.SetPriorityClass(handle, win32process.NORMAL_PRIORITY_CLASS)
        win32api.CloseHandle(handle)
        return True
    except:
        return False

def stretch_image():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                             r"Software\Roblox\RobloxStudioBrowser\roblox.com", 
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "StretchImage", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "AspectRatio", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        return True
    except:
        return False

def reset_stretch():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                             r"Software\Roblox\RobloxStudioBrowser\roblox.com", 
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "StretchImage", 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(key, "AspectRatio", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        return True
    except:
        return False

def take_delayed_screenshot(delay=3):
    countdown_window = tk.Toplevel()
    countdown_window.title("Скриншот")
    countdown_window.geometry("200x100")
    countdown_window.resizable(False, False)
    countdown_window.configure(bg='#1A1A2E')
    countdown_window.overrideredirect(True)
    countdown_window.wm_attributes("-topmost", True)
    
    screen_width = countdown_window.winfo_screenwidth()
    screen_height = countdown_window.winfo_screenheight()
    x = (screen_width - 200) // 2
    y = (screen_height - 100) // 2
    countdown_window.geometry(f"200x100+{x}+{y}")
    
    label = tk.Label(
        countdown_window,
        text="Скриншот через:",
        font=('Segoe UI', 12, 'bold'),
        fg='#E94560',
        bg='#1A1A2E'
    )
    label.pack(pady=5)
    
    timer_label = tk.Label(
        countdown_window,
        text="3",
        font=('Segoe UI', 36, 'bold'),
        fg='white',
        bg='#1A1A2E'
    )
    timer_label.pack(pady=5)
    
    countdown_window.update()
    
    for i in range(delay, 0, -1):
        timer_label.config(text=str(i))
        countdown_window.update()
        time.sleep(1)
    
    countdown_window.destroy()
    
    try:
        screenshot = ImageGrab.grab()
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(SCREENSHOTS_DIR, f"iluzion_{timestamp}.png")
        screenshot.save(filename, "PNG")
        return filename
    except:
        return None

def is_roblox_running():
    try:
        hwnd = win32gui.FindWindow(None, "Roblox")
        if not hwnd:
            hwnd = win32gui.FindWindow(None, "RobloxPlayerBeta")
        return hwnd is not None and win32gui.IsWindowVisible(hwnd)
    except:
        return False

# ---------- ОКНО ЗАГРУЗКИ ----------
class SplashScreen:
    def __init__(self, lang="en"):
        self.lang = lang
        self.window = tk.Tk()
        self.window.title("Загрузка Iluzion")
        self.window.geometry("500x350")
        self.window.resizable(False, False)
        self.window.configure(bg='#1A1A2E')
        self.window.overrideredirect(True)

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 350) // 2
        self.window.geometry(f"500x350+{x}+{y}")

        self.canvas = tk.Canvas(self.window, width=500, height=350, highlightthickness=0, bg='#1A1A2E')
        self.canvas.pack(fill="both", expand=True)
        self.draw_gradient()

        try:
            img = Image.open("icon.ico")
            img = img.resize((80, 80), Image.Resampling.LANCZOS)
            self.icon_photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(250, 80, image=self.icon_photo)
        except:
            self.canvas.create_text(250, 80, text="🌀", font=('Segoe UI', 48, 'bold'), fill='#E94560')

        self.canvas.create_text(250, 165, text="Iluzion", font=('Segoe UI', 28, 'bold'), fill='#E94560')

        self.status_id = self.canvas.create_text(250, 205, text="Инициализация...", 
                                                  font=('Segoe UI', 10), fill='#AAAAAA')

        self.progress = ttk.Progressbar(self.window, length=300, mode='determinate', maximum=100)
        self.progress.place(x=100, y=235)

        self.detail_id = self.canvas.create_text(250, 270, text="Подготовка модулей...", 
                                                  font=('Segoe UI', 8), fill='#666666')

        self.window.update()

    def draw_gradient(self):
        gradient = Image.new("RGB", (500, 350), color=(26, 26, 46))
        draw = ImageDraw.Draw(gradient)
        for i in range(350):
            r = 26 + int(i * 0.06)
            g = 26 + int(i * 0.04)
            b = 46 + int(i * 0.12)
            draw.line([(0, i), (500, i)], fill=(r, g, b))
        self.gradient_image = ImageTk.PhotoImage(gradient)
        self.canvas.create_image(0, 0, anchor="nw", image=self.gradient_image)

    def update_status(self, text, value, detail=""):
        self.canvas.itemconfig(self.status_id, text=text)
        self.progress['value'] = value
        self.canvas.itemconfig(self.detail_id, text=detail)
        self.window.update()
        time.sleep(0.3)

    def close(self):
        try:
            self.window.destroy()
        except:
            pass

# ---------- ОСНОВНОЕ ПРИЛОЖЕНИЕ ----------
class IluzionApp:
    def __init__(self, root, lang="en"):
        self.lang = lang
        self.text = TEXTS[lang]
        self.root = root
        self.root.title(self.text["app_title"])
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#1A1A2E')
        
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

        self.canvas = tk.Canvas(self.root, width=1000, height=700, highlightthickness=0, bg='#1A1A2E')
        self.canvas.pack(fill="both", expand=True)
        self.draw_gradient()

        self.main_frame = tk.Frame(self.canvas, bg='#1A1A2E', bd=0)
        self.main_frame.place(x=10, y=10, width=980, height=680)
        self.canvas.create_rectangle(10, 10, 990, 690, fill='#1A1A2E', outline='#E94560', width=1)

        # ---------- ЛЕВАЯ ПАНЕЛЬ ----------
        self.sidebar = tk.Frame(self.main_frame, bg='#0F1A2E', width=110, height=680)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)

        self.tab_buttons = []
        tab_names = [
            ("⚡", self.text["tab_turbo"]),
            ("🎨", self.text["tab_quality"]),
            ("🛠", self.text["tab_tools"]),
            ("🎥", self.text["tab_record"]),
            ("🎯", self.text["tab_crosshair"]),
            ("💬", self.text["tab_feedback"]),
            ("🌍", self.text["tab_language"]),
        ]
        
        for i, (icon, name) in enumerate(tab_names):
            btn = RoundedButton(
                self.sidebar,
                text=f"{icon} {name}",
                bg='#0F1A2E' if i != 0 else '#1A2A4E',
                fg='white' if i != 0 else '#E94560',
                font=('Segoe UI', 10, 'bold'),
                padx=10,
                pady=8,
                radius=8,
                command=lambda idx=i: self.switch_tab(idx)
            )
            btn.pack(pady=3, padx=5, fill='x')
            self.tab_buttons.append(btn)

        # ---------- ОСНОВНАЯ ОБЛАСТЬ ----------
        self.content_frame = tk.Frame(self.main_frame, bg='#1A1A2E')
        self.content_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        self.tabs = []
        self.create_tabs()

        self.current_tab = 0
        self.show_tab(0)

        # ---------- ВЕРХНЯЯ ПАНЕЛЬ ----------
        top_frame = tk.Frame(self.content_frame, bg='#1A1A2E', pady=5)
        top_frame.pack(fill='x', padx=5)

        tk.Label(top_frame, text=self.text["config"], bg='#1A1A2E', fg='#E94560', 
                 font=('Segoe UI', 10, 'bold')).pack(side='left', padx=5)
        self.config_combo = ttk.Combobox(top_frame, width=20, state='readonly', font=('Segoe UI', 9))
        self.config_combo.pack(side='left', padx=5)
        self.config_combo.bind('<<ComboboxSelected>>', self.on_config_selected)

        for text, cmd, color in [
            (self.text["save"], self.save_config, '#E94560'),
            (self.text["new"], self.new_config, '#533483'),
            (self.text["delete"], self.delete_config, '#C82F3D')
        ]:
            btn = RoundedButton(top_frame, text=text, bg=color, fg='white', 
                               font=('Segoe UI', 8, 'bold'), command=cmd, padx=8, pady=3)
            btn.pack(side='left', padx=3)

        self.fps_status = tk.Label(top_frame, text=self.text["fps_status_off"], bg='#1A1A2E', fg='#888', 
                                    font=('Segoe UI', 9, 'bold'))
        self.fps_status.pack(side='right', padx=10)

        # ---------- ИСТОРИЯ ----------
        self.history_frame = tk.Frame(self.content_frame, bg='#1A1A2E', pady=3)
        self.history_frame.pack(fill='x', padx=5, pady=(0,5))
        self.last_used = {k: False for k in DEFAULT_CONFIG.keys() if not k.startswith('overlay_')}
        self.update_history_labels()

        # ---------- КНОПКИ ВНИЗУ ----------
        bottom_frame = tk.Frame(self.content_frame, bg='#1A1A2E', pady=5)
        bottom_frame.pack(fill='x', padx=5)

        self.apply_button = RoundedButton(
            bottom_frame,
            text=self.text["apply"],
            bg='#28B463',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.apply_all,
            padx=20,
            pady=8
        )
        self.apply_button.pack(side='left', padx=5)

        self.stop_button = RoundedButton(
            bottom_frame,
            text=self.text["stop"],
            bg='#FF9800',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.stop_all,
            padx=20,
            pady=8
        )
        self.stop_button.pack(side='left', padx=5)

        self.rollback_button = RoundedButton(
            bottom_frame,
            text=self.text["rollback"],
            bg='#C82F3D',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.rollback_all,
            padx=20,
            pady=8
        )
        self.rollback_button.pack(side='right', padx=5)

        hotkey_label = tk.Label(
            bottom_frame,
            text=self.text["rollback_hotkey"],
            bg='#1A1A2E',
            fg='#FFD700',
            font=('Segoe UI', 9, 'bold')
        )
        hotkey_label.pack(side='right', padx=5)

        self.status_label = tk.Label(self.content_frame, text="✨ Готов к работе", bg='#1A1A2E', fg='#888', 
                                      font=('Segoe UI', 9, 'italic'))
        self.status_label.pack(pady=3)

        self.current_config_name = "default"
        self.config_data = self.load_config("default")
        self.load_config_list()
        self.apply_config_to_ui()
        self.update_window_list()

        try:
            keyboard.add_hotkey('ctrl+j', self.rollback_all)
            keyboard.add_hotkey('alt+q', self.toggle_crosshair_visibility)
            self.status_label.config(text=self.text["status_ready"], fg='#888')
        except:
            self.status_label.config(text=self.text["status_hotkey_error"], fg='#FFD700')

        self.fps_overlay = None
        self.motion_blur = None
        self.key_widget = None
        self.mouse_widget = None
        self.crosshair = None
        self.recorder = None

    def draw_gradient(self):
        gradient = Image.new("RGB", (1000, 700), color=(26, 26, 46))
        draw = ImageDraw.Draw(gradient)
        for i in range(700):
            r = 26 + int(i * 0.03)
            g = 26 + int(i * 0.02)
            b = 46 + int(i * 0.06)
            draw.line([(0, i), (1000, i)], fill=(r, g, b))
        self.gradient_image = ImageTk.PhotoImage(gradient)
        self.canvas.create_image(0, 0, anchor="nw", image=self.gradient_image)

    def switch_tab(self, idx):
        self.current_tab = idx
        for i, btn in enumerate(self.tab_buttons):
            if i == idx:
                btn.config(bg='#1A2A4E', fg='#E94560')
            else:
                btn.config(bg='#0F1A2E', fg='white')
        self.show_tab(idx)

    def show_tab(self, idx):
        for i, tab in enumerate(self.tabs):
            if i == idx:
                tab.pack(fill='both', expand=True)
            else:
                tab.pack_forget()

    def toggle_crosshair_visibility(self):
        if self.crosshair and self.crosshair.is_running():
            visible = self.crosshair.toggle_visibility()
            if visible:
                self.status_label.config(text=self.text["crosshair_shown"], fg='#28B463')
            else:
                self.status_label.config(text=self.text["crosshair_hidden"], fg='#FFD700')
        else:
            self.status_label.config(text="❌ Прицел не запущен", fg='#E94560')

    def create_tabs(self):
        # ---------- Вкладка "Турбо" ----------
        tab_turbo = tk.Frame(self.content_frame, bg='#1A1A2E')
        self.tabs.append(tab_turbo)
        
        self.turbo_var = tk.BooleanVar()
        tk.Checkbutton(tab_turbo, text=self.text["turbo"], 
                       variable=self.turbo_var, bg='#1A1A2E', fg='white', 
                       selectcolor='#1A1A2E', font=('Segoe UI', 11)).grid(row=0, column=0, sticky='w', padx=20, pady=5)
        
        tk.Label(tab_turbo, text=self.text["turbo_select"], 
                 bg='#1A1A2E', fg='#888', font=('Segoe UI', 9)).grid(row=1, column=0, sticky='w', padx=20)
        
        window_frame = tk.Frame(tab_turbo, bg='#1A1A2E')
        window_frame.grid(row=2, column=0, sticky='w', padx=20, pady=5)
        
        self.window_combo = ttk.Combobox(window_frame, width=40, state='readonly', font=('Segoe UI', 9))
        self.window_combo.pack(side='left', padx=5)
        self.turbo_process_var = tk.StringVar()
        self.window_combo.config(textvariable=self.turbo_process_var)
        
        refresh_btn = RoundedButton(window_frame, text=self.text["refresh"], 
                                   bg='#3A5A8C', fg='white', font=('Segoe UI', 8),
                                   command=self.refresh_window_list, padx=8, pady=3)
        refresh_btn.pack(side='left', padx=5)

        tk.Label(tab_turbo, text=self.text["priority"], 
                 bg='#1A1A2E', fg='#888', font=('Segoe UI', 9)).grid(row=3, column=0, sticky='w', padx=20, pady=(10,5))
        
        priority_frame = tk.Frame(tab_turbo, bg='#1A1A2E')
        priority_frame.grid(row=4, column=0, sticky='w', padx=20)
        self.turbo_priority_var = tk.StringVar(value="high")
        
        for text, value in [(self.text["priority_high"], "high"), 
                           (self.text["priority_normal"], "normal")]:
            tk.Radiobutton(priority_frame, text=text, variable=self.turbo_priority_var, value=value,
                          bg='#1A1A2E', fg='white', selectcolor='#1A1A2E', font=('Segoe UI', 9)).pack(anchor='w')

        # ---------- Вкладка "Качество" ----------
        tab_quality = tk.Frame(self.content_frame, bg='#1A1A2E')
        self.tabs.append(tab_quality)

        self.stretch_var = tk.BooleanVar()
        tk.Checkbutton(tab_quality, text=self.text["stretch"], 
                       variable=self.stretch_var, bg='#1A1A2E', fg='white', 
                       selectcolor='#1A1A2E', font=('Segoe UI', 11)).grid(row=0, column=0, sticky='w', padx=20, pady=5)
        tk.Label(tab_quality, text=self.text["stretch_desc"], 
                 bg='#1A1A2E', fg='#888', font=('Segoe UI', 9, 'italic')).grid(row=1, column=0, sticky='w', padx=20)

        self.motion_var = tk.BooleanVar()
        tk.Checkbutton(tab_quality, text=self.text["motion_blur"], 
                       variable=self.motion_var, bg='#1A1A2E', fg='white', 
                       selectcolor='#1A1A2E', font=('Segoe UI', 11)).grid(row=2, column=0, sticky='w', padx=20, pady=(15,5))
        tk.Label(tab_quality, text=self.text["motion_blur_desc"], 
                 bg='#1A1A2E', fg='#888', font=('Segoe UI', 9, 'italic')).grid(row=3, column=0, sticky='w', padx=20)

        strength_frame = tk.Frame(tab_quality, bg='#1A1A2E')
        strength_frame.grid(row=4, column=0, sticky='w', padx=20, pady=5)
        
        tk.Label(strength_frame, text=self.text["motion_blur_strength"], 
                 bg='#1A1A2E', fg='white', font=('Segoe UI', 10)).pack(side='left', padx=5)
        
        self.motion_strength_var = tk.IntVar(value=50)
        strength_slider = tk.Scale(strength_frame, from_=0, to=100, orient='horizontal', 
                                   length=200, bg='#1A1A2E', fg='#E94560', highlightthickness=0,
                                   troughcolor='#0F3460', variable=self.motion_strength_var)
        strength_slider.pack(side='left', padx=10)
        
        self.strength_label = tk.Label(strength_frame, text="50%", bg='#1A1A2E', fg='#E94560', font=('Segoe UI', 10))
        self.strength_label.pack(side='left', padx=5)
        strength_slider.config(command=lambda v: self.strength_label.config(text=f"{int(float(v))}%"))

        # ---------- Вкладка "Инструменты" ----------
        tab_tools = tk.Frame(self.content_frame, bg='#1A1A2E')
        self.tabs.append(tab_tools)

        self.fps_var = tk.BooleanVar()
        tk.Checkbutton(tab_tools, text=self.text["overlay"], 
                       variable=self.fps_var, bg='#1A1A2E', fg='white', 
                       selectcolor='#1A1A2E', font=('Segoe UI', 11)).grid(row=0, column=0, sticky='w', padx=20, pady=5)
        tk.Label(tab_tools, text=self.text["overlay_desc"], 
                 bg='#1A1A2E', fg='#888', font=('Segoe UI', 9, 'italic')).grid(row=1, column=0, sticky='w', padx=20)

        overlay_settings_frame = tk.Frame(tab_tools, bg='#1A1A2E')
        overlay_settings_frame.grid(row=2, column=0, sticky='w', padx=20, pady=5)
        
        tk.Label(overlay_settings_frame, text=self.text["overlay_settings"], 
                 bg='#1A1A2E', fg='#E94560', font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        
        self.overlay_show_fps_var = tk.BooleanVar(value=True)
        self.overlay_show_ping_var = tk.BooleanVar(value=True)
        
        for text, var in [("FPS", self.overlay_show_fps_var), ("Пинг", self.overlay_show_ping_var)]:
            tk.Checkbutton(overlay_settings_frame, text=text, variable=var,
                           bg='#1A1A2E', fg='white', selectcolor='#1A1A2E',
                           font=('Segoe UI', 9)).pack(anchor='w', padx=10)

        self.input_var = tk.BooleanVar()
        tk.Checkbutton(tab_tools, text=self.text["input_widget"], 
                       variable=self.input_var, bg='#1A1A2E', fg='white', 
                       selectcolor='#1A1A2E', font=('Segoe UI', 11)).grid(row=3, column=0, sticky='w', padx=20, pady=5)
        tk.Label(tab_tools, text=self.text["input_widget_desc"], 
                 bg='#1A1A2E', fg='#888', font=('Segoe UI', 9, 'italic')).grid(row=4, column=0, sticky='w', padx=20)

        screenshot_frame = tk.Frame(tab_tools, bg='#1A1A2E')
        screenshot_frame.grid(row=5, column=0, sticky='w', padx=20, pady=10)
        
        screenshot_btn = RoundedButton(
            screenshot_frame,
            text=self.text["screenshot"],
            bg='#533483',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            command=self.take_screenshot_delayed,
            padx=15,
            pady=5
        )
        screenshot_btn.pack(side='left', padx=5)
        
        tk.Label(screenshot_frame, text=self.text["screenshot_desc"], 
                 bg='#1A1A2E', fg='#888', font=('Segoe UI', 9, 'italic')).pack(side='left', padx=5)

        # ---------- Вкладка "Запись" ----------
        tab_record = tk.Frame(self.content_frame, bg='#1A1A2E')
        self.tabs.append(tab_record)

        tk.Label(tab_record, text="🎥 Запись экрана", font=('Segoe UI', 16, 'bold'),
                 bg='#1A1A2E', fg='#E94560').pack(pady=10)

        dev_label = tk.Label(
            tab_record,
            text=self.text["under_development"],
            font=('Segoe UI', 14, 'bold'),
            bg='#1A1A2E',
            fg='#FFD700',
            justify='center'
        )
        dev_label.pack(pady=20)

        settings_frame = tk.Frame(tab_record, bg='#1A1A2E')
        settings_frame.pack(pady=5)

        self.record_mic_var = tk.BooleanVar(value=False)
        mic_check = tk.Checkbutton(
            settings_frame,
            text=self.text["record_microphone"],
            variable=self.record_mic_var,
            bg='#1A1A2E',
            fg='#888',
            selectcolor='#1A1A2E',
            font=('Segoe UI', 10),
            state='disabled'
        )
        mic_check.pack(side='left', padx=10)

        folder_frame = tk.Frame(tab_record, bg='#1A1A2E')
        folder_frame.pack(pady=5)
        
        tk.Label(folder_frame, text=self.text["record_folder"], bg='#1A1A2E', fg='#888', 
                 font=('Segoe UI', 10)).pack(side='left', padx=5)
        self.record_folder_var = tk.StringVar(value=RECORDINGS_DIR)
        folder_entry = tk.Entry(folder_frame, textvariable=self.record_folder_var, width=40, 
                                bg='#0F3460', fg='#888', font=('Segoe UI', 9), state='disabled')
        folder_entry.pack(side='left', padx=5)
        folder_btn = RoundedButton(folder_frame, text=self.text["record_browse"], 
                                  bg='#555', fg='#888', font=('Segoe UI', 8),
                                  command=lambda: None, padx=8, pady=3, state='disabled')
        folder_btn.pack(side='left', padx=5)

        record_btn_frame = tk.Frame(tab_record, bg='#1A1A2E')
        record_btn_frame.pack(pady=10)

        self.record_start_btn = RoundedButton(
            record_btn_frame,
            text=self.text["record_start"],
            bg='#555',
            fg='#888',
            font=('Segoe UI', 10, 'bold'),
            padx=15,
            pady=6,
            state='disabled'
        )
        self.record_start_btn.pack(side='left', padx=10)

        self.record_stop_btn = RoundedButton(
            record_btn_frame,
            text=self.text["record_stop"],
            bg='#555',
            fg='#888',
            font=('Segoe UI', 10, 'bold'),
            padx=15,
            pady=6,
            state='disabled'
        )
        self.record_stop_btn.pack(side='left', padx=10)

        # ---------- Вкладка "Прицел" ----------
        tab_crosshair = tk.Frame(self.content_frame, bg='#1A1A2E')
        self.tabs.append(tab_crosshair)

        tk.Label(tab_crosshair, text="🎯 Прицел", font=('Segoe UI', 16, 'bold'),
                 bg='#1A1A2E', fg='#E94560').pack(pady=10)

        hotkey_label = tk.Label(
            tab_crosshair,
            text=self.text["crosshair_hide_hotkey"],
            bg='#1A1A2E',
            fg='#FFD700',
            font=('Segoe UI', 10, 'bold')
        )
        hotkey_label.pack(anchor='w', padx=20, pady=(0,5))

        self.crosshair_var = tk.BooleanVar()
        tk.Checkbutton(tab_crosshair, text=self.text["crosshair"], 
                       variable=self.crosshair_var, bg='#1A1A2E', fg='white', 
                       selectcolor='#1A1A2E', font=('Segoe UI', 11)).pack(anchor='w', padx=20, pady=5)

        settings_frame_ch = tk.Frame(tab_crosshair, bg='#1A1A2E')
        settings_frame_ch.pack(pady=5, padx=20, anchor='w')

        tk.Label(settings_frame_ch, text=self.text["crosshair_type"], bg='#1A1A2E', fg='white', 
                 font=('Segoe UI', 10)).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.crosshair_type_var = tk.StringVar(value="cross")
        
        self.color_names = {
            "#00FF00": "Green",
            "#FF0000": "Red", 
            "#0000FF": "Blue",
            "#FFFF00": "Yellow",
            "#FF00FF": "Magenta",
            "#00FFFF": "Cyan",
            "#FFFFFF": "White"
        }
        self.color_names_ru = {
            "#00FF00": "Зелёный",
            "#FF0000": "Красный",
            "#0000FF": "Синий",
            "#FFFF00": "Жёлтый",
            "#FF00FF": "Пурпурный",
            "#00FFFF": "Голубой",
            "#FFFFFF": "Белый"
        }
        
        type_combo = ttk.Combobox(settings_frame_ch, textvariable=self.crosshair_type_var, 
                                   values=["cross", "dot", "circle", "triangle", "custom"], 
                                   width=10, state='readonly', font=('Segoe UI', 9))
        type_combo.grid(row=0, column=1, padx=5, pady=2)
        type_combo.bind('<<ComboboxSelected>>', self.on_crosshair_type_changed)

        tk.Label(settings_frame_ch, text=self.text["crosshair_color"], bg='#1A1A2E', fg='white', 
                 font=('Segoe UI', 10)).grid(row=0, column=2, sticky='w', padx=5, pady=2)
        self.crosshair_color_var = tk.StringVar(value="#00FF00")
        
        color_names_list = list(self.color_names.values()) if self.lang == "en" else list(self.color_names_ru.values())
        color_combo = ttk.Combobox(settings_frame_ch, textvariable=self.crosshair_color_var, 
                                    values=color_names_list,
                                    width=10, state='readonly', font=('Segoe UI', 9))
        color_combo.grid(row=0, column=3, padx=5, pady=2)
        color_combo.set("Green" if self.lang == "en" else "Зелёный")
        color_combo.bind('<<ComboboxSelected>>', self.on_color_changed)

        tk.Label(settings_frame_ch, text=self.text["crosshair_size"], bg='#1A1A2E', fg='white', 
                 font=('Segoe UI', 10)).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.crosshair_size_var = tk.IntVar(value=20)
        size_slider = tk.Scale(settings_frame_ch, from_=5, to=50, orient='horizontal', 
                               length=150, bg='#1A1A2E', fg='#E94560', highlightthickness=0,
                               troughcolor='#0F3460', variable=self.crosshair_size_var)
        size_slider.grid(row=1, column=1, padx=5, pady=2)
        self.size_label = tk.Label(settings_frame_ch, text="20", bg='#1A1A2E', fg='#E94560', font=('Segoe UI', 10))
        self.size_label.grid(row=1, column=2, padx=5)
        size_slider.config(command=lambda v: self.size_label.config(text=f"{int(float(v))}"))

        tk.Label(settings_frame_ch, text=self.text["crosshair_opacity"], bg='#1A1A2E', fg='white', 
                 font=('Segoe UI', 10)).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.crosshair_opacity_var = tk.IntVar(value=100)
        opacity_slider = tk.Scale(settings_frame_ch, from_=10, to=100, orient='horizontal', 
                                  length=150, bg='#1A1A2E', fg='#E94560', highlightthickness=0,
                                  troughcolor='#0F3460', variable=self.crosshair_opacity_var)
        opacity_slider.grid(row=2, column=1, padx=5, pady=2)
        self.opacity_label = tk.Label(settings_frame_ch, text="100%", bg='#1A1A2E', fg='#E94560', font=('Segoe UI', 10))
        self.opacity_label.grid(row=2, column=2, padx=5)
        opacity_slider.config(command=lambda v: self.opacity_label.config(text=f"{int(float(v))}%"))

        tk.Label(settings_frame_ch, text=self.text["crosshair_aspect"], bg='#1A1A2E', fg='white', 
                 font=('Segoe UI', 10)).grid(row=3, column=0, sticky='w', padx=5, pady=2)
        self.crosshair_aspect_var = tk.StringVar(value="square")
        aspect_combo = ttk.Combobox(settings_frame_ch, textvariable=self.crosshair_aspect_var,
                                     values=["square", "16_9", "4_3"],
                                     width=8, state='readonly', font=('Segoe UI', 9))
        aspect_combo.grid(row=3, column=1, padx=5, pady=2)
        aspect_display = {
            "square": self.text["crosshair_aspect_square"],
            "16_9": self.text["crosshair_aspect_16_9"],
            "4_3": self.text["crosshair_aspect_4_3"],
        }
        aspect_combo.config(values=list(aspect_display.values()))
        self.aspect_map = {v: k for k, v in aspect_display.items()}
        self.aspect_reverse = aspect_display
        aspect_combo.set(self.aspect_reverse["square"])
        aspect_combo.bind('<<ComboboxSelected>>', self.on_aspect_changed)

        self.crosshair_draggable_var = tk.BooleanVar(value=True)
        tk.Checkbutton(settings_frame_ch, text=self.text["crosshair_draggable"],
                       variable=self.crosshair_draggable_var, bg='#1A1A2E', fg='white',
                       selectcolor='#1A1A2E', font=('Segoe UI', 10)).grid(row=3, column=2, sticky='w', padx=5, pady=2)

        reset_pos_btn = RoundedButton(
            settings_frame_ch,
            text=self.text["crosshair_reset_pos"],
            bg='#FF9800',
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            command=self.reset_crosshair_position,
            padx=10,
            pady=3
        )
        reset_pos_btn.grid(row=3, column=3, padx=5, pady=2)

        image_frame = tk.Frame(tab_crosshair, bg='#1A1A2E')
        image_frame.pack(anchor='w', padx=20, pady=5)

        tk.Label(image_frame, text=self.text["crosshair_image"], bg='#1A1A2E', fg='white', 
                 font=('Segoe UI', 10)).pack(side='left', padx=5)
        self.crosshair_image_var = tk.StringVar(value="")
        image_entry = tk.Entry(image_frame, textvariable=self.crosshair_image_var, width=30, 
                               bg='#0F3460', fg='white', font=('Segoe UI', 9))
        image_entry.pack(side='left', padx=5)
        image_btn = RoundedButton(image_frame, text=self.text["crosshair_browse"], 
                                  bg='#3A5A8C', fg='white', font=('Segoe UI', 8),
                                  command=self.browse_crosshair_image, padx=8, pady=3)
        image_btn.pack(side='left', padx=5)

        # ---------- Вкладка "Обратная связь" ----------
        tab_feedback = tk.Frame(self.content_frame, bg='#1A1A2E')
        self.tabs.append(tab_feedback)

        tk.Label(tab_feedback, text=self.text["feedback_title"], font=('Segoe UI', 16, 'bold'),
                 bg='#1A1A2E', fg='#E94560').pack(pady=10)

        tk.Label(tab_feedback, text=self.text["feedback_desc"],
                 bg='#1A1A2E', fg='#AAAAAA', font=('Segoe UI', 10)).pack(pady=5)

        text_frame = tk.Frame(tab_feedback, bg='#1A1A2E')
        text_frame.pack(pady=10, padx=20, fill='both', expand=True)

        self.feedback_text = tk.Text(text_frame, height=10, width=60, bg='#0F3460', fg='white',
                                      font=('Segoe UI', 10), wrap='word', relief='flat')
        self.feedback_text.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.feedback_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.feedback_text.config(yscrollcommand=scrollbar.set)

        self.feedback_text.insert('1.0', self.text["feedback_placeholder"])
        self.feedback_text.bind('<FocusIn>', self.on_feedback_focus)

        btn_fb_frame = tk.Frame(tab_feedback, bg='#1A1A2E')
        btn_fb_frame.pack(pady=10)

        send_btn = RoundedButton(btn_fb_frame, text=self.text["feedback_send"], bg='#28B463', fg='white',
                                 font=('Segoe UI', 11, 'bold'), command=self.open_feedback_form,
                                 padx=20, pady=8)
        send_btn.pack(side='left', padx=10)

        clear_btn = RoundedButton(btn_fb_frame, text=self.text["feedback_clear"], bg='#C82F3D', fg='white',
                                  font=('Segoe UI', 11, 'bold'), command=self.clear_feedback,
                                  padx=20, pady=8)
        clear_btn.pack(side='left', padx=10)

        # ---------- Вкладка "Язык" ----------
        tab_language = tk.Frame(self.content_frame, bg='#1A1A2E')
        self.tabs.append(tab_language)

        tk.Label(tab_language, text="🌍 Language / Язык", font=('Segoe UI', 16, 'bold'),
                 bg='#1A1A2E', fg='#E94560').pack(pady=20)

        tk.Label(tab_language, text="Select your preferred language:", 
                 bg='#1A1A2E', fg='#AAAAAA', font=('Segoe UI', 12)).pack(pady=5)
        tk.Label(tab_language, text="Выберите предпочитаемый язык:", 
                 bg='#1A1A2E', fg='#AAAAAA', font=('Segoe UI', 12)).pack(pady=5)

        btn_frame_lang = tk.Frame(tab_language, bg='#1A1A2E')
        btn_frame_lang.pack(pady=30)

        def switch_language(lang):
            self.lang = lang
            self.text = TEXTS[lang]
            self.root.title(self.text["app_title"])
            self.rebuild_ui()

        en_btn_lang = RoundedButton(
            btn_frame_lang,
            text="🇬🇧 English",
            bg='#E94560' if self.lang == "en" else '#0F3460',
            fg='white',
            font=('Segoe UI', 14, 'bold'),
            command=lambda: switch_language("en"),
            padx=25,
            pady=10
        )
        en_btn_lang.pack(side='left', padx=15)

        ru_btn_lang = RoundedButton(
            btn_frame_lang,
            text="🇷🇺 Русский",
            bg='#E94560' if self.lang == "ru" else '#0F3460',
            fg='white',
            font=('Segoe UI', 14, 'bold'),
            command=lambda: switch_language("ru"),
            padx=25,
            pady=10
        )
        ru_btn_lang.pack(side='left', padx=15)

        tk.Label(tab_language, text="✅ Language changes apply immediately",
                 bg='#1A1A2E', fg='#28B463', font=('Segoe UI', 10, 'italic')).pack(pady=10)
        tk.Label(tab_language, text="✅ Язык меняется сразу без перезапуска",
                 bg='#1A1A2E', fg='#28B463', font=('Segoe UI', 10, 'italic')).pack(pady=2)

    def on_crosshair_type_changed(self, event):
        if self.crosshair_type_var.get() != "custom":
            if self.crosshair and self.crosshair.is_running():
                self.crosshair._stop_video()
                self.crosshair.draw_crosshair()
                self.crosshair.window.update()

    def on_color_changed(self, event):
        color_name = event.widget.get()
        if self.lang == "en":
            reverse_colors = {v: k for k, v in self.color_names.items()}
        else:
            reverse_colors = {v: k for k, v in self.color_names_ru.items()}
        hex_color = reverse_colors.get(color_name, "#00FF00")
        self.crosshair_color_var.set(hex_color)

    def update_color_combo(self):
        hex_color = self.crosshair_color_var.get()
        if self.lang == "en":
            color_name = self.color_names.get(hex_color, hex_color)
        else:
            color_name = self.color_names_ru.get(hex_color, hex_color)
        for widget in self.tabs[4].winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Combobox) and child.get() in list(self.color_names.values()) + list(self.color_names_ru.values()):
                        child.set(color_name)
                        break

    def on_aspect_changed(self, event):
        display_name = event.widget.get()
        aspect = self.aspect_map.get(display_name, "square")
        self.crosshair_aspect_var.set(aspect)

    def reset_crosshair_position(self):
        if self.crosshair and self.crosshair.is_running():
            self.crosshair.reset_position()
            self.status_label.config(text="✅ Позиция прицела сброшена в центр", fg='#28B463')
        else:
            self.status_label.config(text="❌ Прицел не запущен", fg='#E94560')

    def load_config(self, name):
        path = os.path.join(CONFIG_DIR, f"{name}.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return DEFAULT_CONFIG.copy()

    def save_config_to_file(self, name, data):
        path = os.path.join(CONFIG_DIR, f"{name}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_config_list(self):
        files = [f[:-5] for f in os.listdir(CONFIG_DIR) if f.endswith('.json')]
        self.config_combo['values'] = files if files else ["default"]
        if files:
            self.config_combo.set(files[0])
            self.current_config_name = files[0]
            self.config_data = self.load_config(self.current_config_name)

    def apply_config_to_ui(self):
        self.turbo_var.set(self.config_data.get('turbo_mode', False))
        self.turbo_process_var.set(self.config_data.get('turbo_process', ''))
        self.turbo_priority_var.set(self.config_data.get('turbo_priority', 'high'))
        self.fps_var.set(self.config_data.get('fps_overlay', False))
        self.stretch_var.set(self.config_data.get('stretch_image', False))
        self.motion_var.set(self.config_data.get('motion_blur', False))
        self.motion_strength_var.set(self.config_data.get('motion_blur_strength', 50))
        self.input_var.set(self.config_data.get('input_widget', False))
        self.overlay_show_fps_var.set(self.config_data.get('overlay_show_fps', True))
        self.overlay_show_ping_var.set(self.config_data.get('overlay_show_ping', True))
        self.crosshair_var.set(self.config_data.get('crosshair_enabled', False))
        self.crosshair_type_var.set(self.config_data.get('crosshair_type', 'cross'))
        self.crosshair_color_var.set(self.config_data.get('crosshair_color', '#00FF00'))
        self.crosshair_size_var.set(self.config_data.get('crosshair_size', 20))
        self.crosshair_opacity_var.set(self.config_data.get('crosshair_opacity', 100))
        self.crosshair_image_var.set(self.config_data.get('crosshair_image', ''))
        self.crosshair_aspect_var.set(self.config_data.get('crosshair_aspect', 'square'))
        self.crosshair_draggable_var.set(self.config_data.get('crosshair_draggable', True))
        self.record_mic_var.set(self.config_data.get('record_microphone', False))
        self.record_folder_var.set(self.config_data.get('record_folder', RECORDINGS_DIR))
        
        self.update_color_combo()
        
        aspect_display = {
            "square": self.text["crosshair_aspect_square"],
            "16_9": self.text["crosshair_aspect_16_9"],
            "4_3": self.text["crosshair_aspect_4_3"],
        }
        for widget in self.tabs[4].winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Combobox):
                        if child.get() in aspect_display.values():
                            child.set(aspect_display.get(self.crosshair_aspect_var.get(), self.text["crosshair_aspect_square"]))
                            break

    def get_config_from_ui(self):
        return {
            'turbo_mode': self.turbo_var.get(),
            'turbo_process': self.turbo_process_var.get(),
            'turbo_priority': self.turbo_priority_var.get(),
            'fps_overlay': self.fps_var.get(),
            'stretch_image': self.stretch_var.get(),
            'motion_blur': self.motion_var.get(),
            'motion_blur_strength': self.motion_strength_var.get(),
            'input_widget': self.input_var.get(),
            'overlay_show_fps': self.overlay_show_fps_var.get(),
            'overlay_show_ping': self.overlay_show_ping_var.get(),
            'language': self.lang,
            'record_folder': self.record_folder_var.get(),
            'record_microphone': self.record_mic_var.get(),
            'crosshair_enabled': self.crosshair_var.get(),
            'crosshair_type': self.crosshair_type_var.get(),
            'crosshair_color': self.crosshair_color_var.get(),
            'crosshair_size': self.crosshair_size_var.get(),
            'crosshair_opacity': self.crosshair_opacity_var.get(),
            'crosshair_image': self.crosshair_image_var.get(),
            'crosshair_aspect': self.crosshair_aspect_var.get(),
            'crosshair_draggable': self.crosshair_draggable_var.get(),
            'crosshair_visible': True,
        }

    def update_window_list(self):
        windows = get_open_windows()
        window_names = [f"{title} (HWND:{hwnd})" for hwnd, title in windows if title]
        if not window_names:
            window_names = ["Нет открытых окон"]
        self.window_combo['values'] = window_names
        if window_names:
            self.window_combo.set(window_names[0])

    def refresh_window_list(self):
        self.update_window_list()
        self.status_label.config(text="🔄 Список окон обновлён", fg='#28B463')

    def browse_record_folder(self):
        folder = filedialog.askdirectory(title="Выберите папку для сохранения записей")
        if folder:
            self.record_folder_var.set(folder)
            self.status_label.config(text=f"{self.text['record_folder_changed']} {folder}", fg='#28B463')

    def browse_crosshair_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Images & Videos", "*.png *.jpg *.jpeg *.bmp *.gif *.mp4 *.avi *.mov *.mkv *.webm"),
                ("Images", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("Videos", "*.mp4 *.avi *.mov *.mkv *.webm")
            ],
            title="Выберите изображение или видео для прицела"
        )
        if file_path:
            self.crosshair_type_var.set("custom")
            self.crosshair_image_var.set(file_path)
            self.status_label.config(
                text=f"✅ Загружено: {os.path.basename(file_path)}",
                fg='#28B463'
            )
            
            if self.crosshair and self.crosshair.is_running():
                self.crosshair.update_settings(
                    crosshair_type="custom",
                    image_path=file_path,
                    opacity=self.crosshair_opacity_var.get()
                )

    def rebuild_ui(self):
        tab_names = [
            ("⚡", self.text["tab_turbo"]),
            ("🎨", self.text["tab_quality"]),
            ("🛠", self.text["tab_tools"]),
            ("🎥", self.text["tab_record"]),
            ("🎯", self.text["tab_crosshair"]),
            ("💬", self.text["tab_feedback"]),
            ("🌍", self.text["tab_language"]),
        ]
        
        for i, btn in enumerate(self.tab_buttons):
            if i < len(tab_names):
                icon, name = tab_names[i]
                btn.config(text=f"{icon} {name}")
        
        if self.fps_overlay and self.fps_overlay.is_running():
            self.fps_status.config(text=self.text["fps_status_on"])
        else:
            self.fps_status.config(text=self.text["fps_status_off"])
        
        self.apply_button.config(text=self.text["apply"])
        self.stop_button.config(text=self.text["stop"])
        self.rollback_button.config(text=self.text["rollback"])
        
        self.status_label.config(text=self.text["status_ready"])
        
        self.show_tab(self.current_tab)
        self.update_color_combo()
        
        try:
            self.save_config_to_file(self.current_config_name, self.get_config_from_ui())
        except:
            pass

    def open_feedback_form(self):
        text = self.feedback_text.get('1.0', 'end-1c').strip()
        
        feedback_file = os.path.join(CONFIG_DIR, "feedback.txt")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(feedback_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"📅 Дата: {timestamp}\n")
            f.write(f"📌 Версия: 30.0\n")
            f.write(f"💬 Сообщение:\n{text if text else '(пусто)'}\n")
            f.write(f"{'='*50}\n")
        
        try:
            if text and text != self.text["feedback_placeholder"]:
                encoded_text = urllib.parse.quote(text)
                webbrowser.open(f"https://forms.yandex.ru/u/6a95ba08eb6146ecc605cbe4/?text={encoded_text}")
            else:
                webbrowser.open("https://forms.yandex.ru/u/6a95ba08eb6146ecc605cbe4/")
            
            self.feedback_text.delete('1.0', 'end')
            self.feedback_text.insert('1.0', self.text["feedback_placeholder"])
            messagebox.showinfo("✅ Успех", self.text["feedback_success"])
            self.status_label.config(text="✅ Форма открыта в браузере", fg='#28B463')
        except:
            messagebox.showwarning("⚠️ Ошибка", self.text["feedback_error"])
            self.status_label.config(text="❌ Не удалось открыть форму", fg='#E94560')

    def on_feedback_focus(self, event):
        if self.feedback_text.get('1.0', 'end-1c') == self.text["feedback_placeholder"]:
            self.feedback_text.delete('1.0', 'end')

    def clear_feedback(self):
        if messagebox.askyesno("Подтверждение", "Очистить поле ввода?"):
            self.feedback_text.delete('1.0', 'end')
            self.feedback_text.insert('1.0', self.text["feedback_placeholder"])

    def take_screenshot_delayed(self):
        self.status_label.config(text=self.text["screenshot_ready"], fg='#FFD700')
        self.root.update()
        filename = take_delayed_screenshot(delay=3)
        if filename:
            self.status_label.config(text=f"{self.text['screenshot_saved']} {os.path.basename(filename)}", fg='#28B463')
            messagebox.showinfo(self.text["screenshot_success"], f"{self.text['screenshot_saved_msg']}\n{filename}")
        else:
            self.status_label.config(text=self.text["screenshot_error"], fg='#E94560')
            messagebox.showerror(self.text["screenshot_success"], self.text["screenshot_error"])

    def start_recording(self):
        try:
            mic = self.record_mic_var.get()
            folder = self.record_folder_var.get()
            
            self.recorder = ScreenRecorder(30, "medium", mic, folder)
            
            self.record_start_btn.config(state='disabled')
            self.record_stop_btn.config(state='normal')
            
            self.status_label.config(text=self.text["record_starting"], fg='#FFD700')
            self.root.update()
            
            self.recorder.start_recording()
            self.status_label.config(text=self.text["record_started"], fg='#FF4444')
        except Exception as e:
            self.status_label.config(text=f"{self.text['record_error']}: {str(e)}", fg='#E94560')
            self.record_start_btn.config(state='normal')
            self.record_stop_btn.config(state='disabled')

    def stop_recording(self):
        try:
            if self.recorder:
                self.status_label.config(text="⏳ Сохранение записи...", fg='#FFD700')
                self.root.update()
                
                result = self.recorder.stop_recording()
                
                folder = self.record_folder_var.get()
                files = [f for f in os.listdir(folder) if f.startswith("recording_") and f.endswith(".mp4")]
                if files:
                    latest = max(files, key=lambda f: os.path.getctime(os.path.join(folder, f)))
                    self.status_label.config(text=f"{self.text['record_stopped']} {latest}", fg='#28B463')
                    messagebox.showinfo(self.text["record_success"], 
                                       f"{self.text['record_saved_msg']}\n{os.path.join(folder, latest)}")
                else:
                    self.status_label.config(text=self.text["record_stopped"], fg='#28B463')
        except Exception as e:
            self.status_label.config(text=f"{self.text['record_error']}: {str(e)}", fg='#E94560')
        finally:
            self.record_start_btn.config(state='normal')
            self.record_stop_btn.config(state='disabled')
            self.recorder = None

    def stop_all(self):
        results = []
        
        if self.turbo_process_var.get() and "HWND:" in self.turbo_process_var.get():
            try:
                hwnd = int(self.turbo_process_var.get().split("HWND:")[1].strip(")"))
                if reset_process_priority_by_window(hwnd):
                    results.append("✅ Приоритет сброшен")
            except:
                pass
        
        if reset_stretch():
            results.append("✅ Растяжение отключено")
        
        if self.fps_overlay:
            try:
                self.fps_overlay.close()
                self.fps_overlay = None
                self.fps_status.config(text=self.text["fps_status_off"], fg='#888')
                results.append("✅ Оверлей остановлен")
            except:
                pass
        
        if self.motion_blur:
            try:
                self.motion_blur.close()
                self.motion_blur = None
                results.append("✅ Motion Blur отключен")
            except:
                pass
        
        if self.key_widget:
            try:
                self.key_widget.close()
                self.key_widget = None
                results.append("✅ Виджет клавиш закрыт")
            except:
                pass
        
        if self.mouse_widget:
            try:
                self.mouse_widget.close()
                self.mouse_widget = None
                results.append("✅ Виджет мыши закрыт")
            except:
                pass
        
        if self.crosshair:
            try:
                self.crosshair.close()
                self.crosshair = None
                results.append("✅ Прицел закрыт")
            except:
                pass
        
        self.status_label.config(text=self.text["stop_done"], fg='#28B463')
        messagebox.showinfo("Готово", "\n".join(results))

    def stop_all_functions(self):
        if self.turbo_process_var.get() and "HWND:" in self.turbo_process_var.get():
            try:
                hwnd = int(self.turbo_process_var.get().split("HWND:")[1].strip(")"))
                reset_process_priority_by_window(hwnd)
            except:
                pass
        
        reset_stretch()
        
        if self.fps_overlay:
            try:
                self.fps_overlay.close()
                self.fps_overlay = None
                self.fps_status.config(text=self.text["fps_status_off"], fg='#888')
            except:
                pass
        
        if self.motion_blur:
            try:
                self.motion_blur.close()
                self.motion_blur = None
            except:
                pass
        
        if self.key_widget:
            try:
                self.key_widget.close()
                self.key_widget = None
            except:
                pass
        
        if self.mouse_widget:
            try:
                self.mouse_widget.close()
                self.mouse_widget = None
            except:
                pass
        
        if self.crosshair:
            try:
                self.crosshair.close()
                self.crosshair = None
            except:
                pass

    def rollback_all(self):
        if not messagebox.askyesno(self.text["rollback_confirm"], self.text["rollback_confirm_msg"]):
            return

        self.status_label.config(text="⏳ Откат изменений...", fg='#FFD700')
        self.root.update()

        self.last_used = {
            "turbo_mode": self.turbo_var.get(),
            "fps_overlay": self.fps_var.get(),
            "stretch_image": self.stretch_var.get(),
            "motion_blur": self.motion_var.get(),
            "input_widget": self.input_var.get(),
            "crosshair": self.crosshair_var.get(),
        }

        self.stop_all_functions()

        self.turbo_var.set(False)
        self.fps_var.set(False)
        self.stretch_var.set(False)
        self.motion_var.set(False)
        self.input_var.set(False)
        self.crosshair_var.set(False)

        self.save_config_to_file(self.current_config_name, self.get_config_from_ui())
        self.update_history_labels()

        self.status_label.config(text=self.text["rollback_done"], fg='#28B463')
        messagebox.showinfo(self.text["rollback_done"], self.text["rollback_result"])

    def apply_all(self):
        self.status_label.config(text="⏳ Применение...", fg='#FFD700')
        self.root.update()

        results = []

        if self.turbo_var.get():
            window_name = self.turbo_process_var.get()
            if window_name and "HWND:" in window_name:
                try:
                    hwnd = int(window_name.split("HWND:")[1].strip(")"))
                    priority = self.turbo_priority_var.get()
                    if set_process_priority_by_window(hwnd, priority):
                        results.append("✅ Турбо-режим включён")
                    else:
                        results.append("❌ Турбо-режим: ошибка")
                except:
                    results.append("❌ Турбо-режим: выберите окно")
            else:
                results.append("❌ Турбо-режим: выберите окно из списка")

        if self.stretch_var.get():
            if stretch_image():
                results.append("🖥 Растяжение включено")
            else:
                results.append("❌ Растяжение: ошибка")

        if self.motion_var.get():
            strength = self.motion_strength_var.get()
            if self.motion_blur is None or not self.motion_blur.is_running():
                self.motion_blur = MotionBlurOverlay(strength)
                results.append(f"🌀 Motion Blur включен ({strength}%)")
            else:
                self.motion_blur.set_strength(strength)
                results.append(f"🌀 Motion Blur обновлён ({strength}%)")

        if self.input_var.get():
            if self.key_widget is None or not self.key_widget.is_running():
                self.key_widget = KeyWidget()
                results.append("⌨️ Виджет клавиш запущен")
            else:
                results.append("ℹ️ Виджет клавиш уже работает")
            
            if self.mouse_widget is None or not self.mouse_widget.is_running():
                self.mouse_widget = MouseWidget()
                results.append("🖱 Виджет мыши запущен")
            else:
                results.append("ℹ️ Виджет мыши уже работает")

        if self.fps_var.get():
            if self.fps_overlay is None or not self.fps_overlay.is_running():
                show_fps = self.config_data.get('overlay_show_fps', True)
                show_ping = self.config_data.get('overlay_show_ping', True)
                
                self.fps_overlay = FPSOverlay(show_fps, show_ping)
                self.fps_status.config(text=self.text["fps_status_on"], fg='#28B463')
                results.append("📊 Оверлей запущен")
            else:
                results.append("ℹ️ Оверлей уже работает")
        else:
            if self.fps_overlay:
                try:
                    self.fps_overlay.close()
                    self.fps_overlay = None
                    self.fps_status.config(text=self.text["fps_status_off"], fg='#888')
                    results.append("📊 Оверлей остановлен")
                except:
                    results.append("❌ Оверлей: ошибка")

        if self.crosshair_var.get():
            aspect = self.crosshair_aspect_var.get()
            draggable = self.crosshair_draggable_var.get()
            image_path = self.crosshair_image_var.get()
            crosshair_type = self.crosshair_type_var.get()
            
            if crosshair_type != "custom":
                image_path = ""
            
            if self.crosshair is None or not self.crosshair.is_running():
                self.crosshair = CrosshairOverlay(
                    crosshair_type=crosshair_type,
                    color=self.crosshair_color_var.get(),
                    size=self.crosshair_size_var.get(),
                    opacity=self.crosshair_opacity_var.get(),
                    image_path=image_path,
                    aspect=aspect,
                    draggable=draggable
                )
                results.append(f"🎯 Прицел запущен ({crosshair_type})")
            else:
                self.crosshair.update_settings(
                    crosshair_type=crosshair_type,
                    color=self.crosshair_color_var.get(),
                    size=self.crosshair_size_var.get(),
                    opacity=self.crosshair_opacity_var.get(),
                    image_path=image_path,
                    aspect=aspect,
                    draggable=draggable
                )
                results.append(f"🎯 Прицел обновлён ({crosshair_type})")
        else:
            if self.crosshair:
                try:
                    self.crosshair.close()
                    self.crosshair = None
                    results.append("🎯 Прицел остановлен")
                except:
                    results.append("❌ Прицел: ошибка")

        self.last_used = {
            "turbo_mode": self.turbo_var.get(),
            "fps_overlay": self.fps_var.get(),
            "stretch_image": self.stretch_var.get(),
            "motion_blur": self.motion_var.get(),
            "input_widget": self.input_var.get(),
            "crosshair": self.crosshair_var.get(),
        }
        self.update_history_labels()

        self.save_config_to_file(self.current_config_name, self.get_config_from_ui())

        self.status_label.config(text=self.text["apply_done"], fg='#28B463')
        messagebox.showinfo(self.text["apply_done"], "\n".join(results))

    def update_history_labels(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        history_texts = []
        if self.last_used.get("turbo_mode", False):
            history_texts.append(self.text["turbo_history"])
        if self.last_used.get("fps_overlay", False):
            history_texts.append(self.text["overlay_history"])
        if self.last_used.get("stretch_image", False):
            history_texts.append(self.text["stretch_history"])
        if self.last_used.get("motion_blur", False):
            history_texts.append(self.text["motion_history"])
        if self.last_used.get("input_widget", False):
            history_texts.append(self.text["input_history"])
        if self.last_used.get("crosshair", False):
            history_texts.append(self.text["crosshair_history"])
        
        if history_texts:
            tk.Label(self.history_frame, text=self.text["history"], 
                     bg='#1A1A2E', fg='#E94560', font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(0,3))
            for text in history_texts:
                tk.Label(self.history_frame, text=text, 
                         bg='#1A1A2E', fg='#FFD700', font=('Segoe UI', 8)).pack(anchor='w')
        else:
            tk.Label(self.history_frame, text=self.text["no_history"], 
                     bg='#1A1A2E', fg='#888', font=('Segoe UI', 8, 'italic')).pack(anchor='w')

    def on_config_selected(self, event):
        name = self.config_combo.get()
        if name:
            self.current_config_name = name
            self.config_data = self.load_config(name)
            self.apply_config_to_ui()

    def save_config(self):
        name = self.config_combo.get() or "default"
        data = self.get_config_from_ui()
        self.save_config_to_file(name, data)
        self.current_config_name = name
        self.load_config_list()
        messagebox.showinfo("Успех", f"Конфиг '{name}' сохранён!")

    def new_config(self):
        name = simpledialog.askstring("Новый конфиг", "Введите имя:")
        if name:
            if name in [f[:-5] for f in os.listdir(CONFIG_DIR) if f.endswith('.json')]:
                messagebox.showerror("Ошибка", "Такой конфиг уже существует")
                return
            self.save_config_to_file(name, DEFAULT_CONFIG.copy())
            self.load_config_list()
            self.config_combo.set(name)
            self.current_config_name = name
            self.config_data = DEFAULT_CONFIG.copy()
            self.apply_config_to_ui()
            self.last_used = {k: False for k in self.last_used}
            self.update_history_labels()

    def delete_config(self):
        name = self.config_combo.get()
        if name and name != "default":
            if messagebox.askyesno("Удаление", f"Удалить конфиг '{name}'?"):
                os.remove(os.path.join(CONFIG_DIR, f"{name}.json"))
                self.load_config_list()
                self.on_config_selected(None)

    def on_closing(self):
        """Полное завершение приложения"""
        try:
            # Останавливаем все функции
            self.stop_all_functions()
            
            # Закрываем окно прицела
            if self.crosshair:
                try:
                    self.crosshair.close()
                    self.crosshair = None
                except:
                    pass
            
            # Закрываем FPS оверлей
            if self.fps_overlay:
                try:
                    self.fps_overlay.close()
                    self.fps_overlay = None
                except:
                    pass
            
            # Закрываем виджеты
            if self.key_widget:
                try:
                    self.key_widget.close()
                    self.key_widget = None
                except:
                    pass
            
            if self.mouse_widget:
                try:
                    self.mouse_widget.close()
                    self.mouse_widget = None
                except:
                    pass
            
            # Закрываем Motion Blur
            if self.motion_blur:
                try:
                    self.motion_blur.close()
                    self.motion_blur = None
                except:
                    pass
            
            # Сохраняем конфиг
            try:
                self.save_config_to_file(self.current_config_name, self.get_config_from_ui())
            except:
                pass
            
            # Удаляем горячие клавиши
            try:
                keyboard.remove_hotkey('ctrl+j')
                keyboard.remove_hotkey('alt+q')
            except:
                pass
            
        except:
            pass
        
        # Закрываем главное окно
        try:
            self.root.destroy()
        except:
            pass
        
        # Принудительно завершаем процесс
        try:
            os._exit(0)
        except:
            pass

# ---------- ЗАПУСК ----------
if __name__ == "__main__":
    config_path = os.path.join(CONFIG_DIR, "default.json")
    lang = "en"
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
                if "language" in saved_config:
                    lang = saved_config["language"]
                    splash = SplashScreen(lang)
                    steps = [
                        ("🔧 Инициализация модулей...", 10, "Загрузка библиотек..."),
                        ("🎨 Создание графического движка...", 25, "Подготовка интерфейса..."),
                        ("⚙️ Настройка конфигураций...", 45, "Чтение пользовательских настроек..."),
                        ("🖼 Загрузка ресурсов...", 60, "Подготовка иконок и шрифтов..."),
                        ("🔌 Проверка системных компонентов...", 75, "Сканирование открытых окон..."),
                        ("🚀 Готово к работе!", 100, "Запуск основного окна..."),
                    ]
                    for text, value, detail in steps:
                        splash.update_status(text, value, detail)
                    splash.close()
                    
                    root = tk.Tk()
                    try:
                        root.iconbitmap('icon.ico')
                    except:
                        pass
                    app = IluzionApp(root, lang)
                    root.protocol("WM_DELETE_WINDOW", app.on_closing)
                    root.mainloop()
                    exit()
        except:
            pass
    
    # ---------- ПЕРВЫЙ ЗАПУСК (выбор языка) ----------
    welcome_window = tk.Tk()
    welcome_window.title("Добро пожаловать!")
    welcome_window.geometry("500x400")
    welcome_window.resizable(False, False)
    welcome_window.configure(bg='#1A1A2E')
    welcome_window.overrideredirect(True)
    
    screen_width = welcome_window.winfo_screenwidth()
    screen_height = welcome_window.winfo_screenheight()
    x = (screen_width - 500) // 2
    y = (screen_height - 400) // 2
    welcome_window.geometry(f"500x400+{x}+{y}")
    
    canvas = tk.Canvas(welcome_window, width=500, height=400, highlightthickness=0, bg='#1A1A2E')
    canvas.pack(fill="both", expand=True)
    
    gradient = Image.new("RGB", (500, 400), color=(26, 26, 46))
    draw = ImageDraw.Draw(gradient)
    for i in range(400):
        r = 26 + int(i * 0.06)
        g = 26 + int(i * 0.04)
        b = 46 + int(i * 0.12)
        draw.line([(0, i), (500, i)], fill=(r, g, b))
    gradient_image = ImageTk.PhotoImage(gradient)
    canvas.create_image(0, 0, anchor="nw", image=gradient_image)
    
    try:
        img = Image.open("icon.ico")
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        icon_photo = ImageTk.PhotoImage(img)
        canvas.create_image(250, 100, image=icon_photo)
    except:
        canvas.create_text(250, 100, text="🌀", font=('Segoe UI', 60, 'bold'), fill='#E94560')
    
    canvas.create_text(250, 200, text="Iluzion", font=('Segoe UI', 32, 'bold'), fill='#E94560')
    canvas.create_text(250, 240, text="Ваш визуальный помощник", font=('Segoe UI', 14), fill='#AAAAAA')
    
    welcome_window.attributes('-alpha', 0.0)
    def fade_in():
        alpha = 0.0
        while alpha < 1.0:
            alpha += 0.05
            welcome_window.attributes('-alpha', alpha)
            welcome_window.update()
            time.sleep(0.02)
    threading.Thread(target=fade_in, daemon=True).start()
    
    def run_app(lang):
        welcome_window.destroy()
        splash = SplashScreen(lang)
        steps = [
            ("🔧 Инициализация модулей...", 10, "Загрузка библиотек..."),
            ("🎨 Создание графического движка...", 25, "Подготовка интерфейса..."),
            ("⚙️ Настройка конфигураций...", 45, "Чтение пользовательских настроек..."),
            ("🖼 Загрузка ресурсов...", 60, "Подготовка иконок и шрифтов..."),
            ("🔌 Проверка системных компонентов...", 75, "Сканирование открытых окон..."),
            ("🚀 Готово к работе!", 100, "Запуск основного окна..."),
        ]
        for text, value, detail in steps:
            splash.update_status(text, value, detail)
        splash.close()
        
        root = tk.Tk()
        try:
            root.iconbitmap('icon.ico')
        except:
            pass
        app = IluzionApp(root, lang)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    
    def show_language_selector():
        lang_window = tk.Toplevel()
        lang_window.title("Выберите язык / Choose Language")
        lang_window.geometry("400x300")
        lang_window.resizable(False, False)
        lang_window.configure(bg='#1A1A2E')
        lang_window.overrideredirect(True)
        lang_window.transient(welcome_window)
        lang_window.grab_set()
        
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        lang_window.geometry(f"400x300+{x}+{y}")
        
        lang_canvas = tk.Canvas(lang_window, width=400, height=300, highlightthickness=0, bg='#1A1A2E')
        lang_canvas.pack(fill="both", expand=True)
        
        gradient_lang = Image.new("RGB", (400, 300), color=(26, 26, 46))
        draw_lang = ImageDraw.Draw(gradient_lang)
        for i in range(300):
            r = 26 + int(i * 0.08)
            g = 26 + int(i * 0.05)
            b = 46 + int(i * 0.15)
            draw_lang.line([(0, i), (400, i)], fill=(r, g, b))
        gradient_lang_image = ImageTk.PhotoImage(gradient_lang)
        lang_canvas.create_image(0, 0, anchor="nw", image=gradient_lang_image)
        
        lang_canvas.create_text(200, 50, text="🌍 Выберите язык", font=('Segoe UI', 18, 'bold'), fill='#E94560')
        lang_canvas.create_text(200, 80, text="Choose your language", font=('Segoe UI', 12), fill='#AAAAAA')
        
        def select_lang(lang):
            lang_window.destroy()
            try:
                os.makedirs(CONFIG_DIR, exist_ok=True)
                with open(os.path.join(CONFIG_DIR, "default.json"), 'w', encoding='utf-8') as f:
                    json.dump({"language": lang}, f, indent=4, ensure_ascii=False)
            except:
                pass
            run_app(lang)
        
        en_btn = RoundedButton(
            lang_window,
            text="🇬🇧 English",
            bg='#E94560',
            fg='white',
            font=('Segoe UI', 14, 'bold'),
            command=lambda: select_lang("en"),
            padx=25,
            pady=10
        )
        en_btn.place(x=50, y=150)
        
        ru_btn = RoundedButton(
            lang_window,
            text="🇷🇺 Русский",
            bg='#533483',
            fg='white',
            font=('Segoe UI', 14, 'bold'),
            command=lambda: select_lang("ru"),
            padx=25,
            pady=10
        )
        ru_btn.place(x=230, y=150)
        
        lang_window.mainloop()
    
    def on_start():
        show_language_selector()
    
    start_btn = RoundedButton(
        welcome_window,
        text=TEXTS["en"]["start"],
        bg='#E94560',
        fg='white',
        font=('Segoe UI', 14, 'bold'),
        command=on_start,
        padx=30,
        pady=10
    )
    start_btn.place(x=200, y=300)
    
    welcome_window.mainloop()
    
    # Принудительный выход после завершения
    try:
        os._exit(0)
    except:
        pass
