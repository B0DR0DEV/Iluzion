# 🌀 Iluzion v35.0

**Iluzion** is a multifunctional gaming optimization and interface enhancement tool for Windows. It provides a set of utilities to improve your gaming experience, especially in Roblox.

> **Note:** This project is currently in active development. Some features may be incomplete or subject to change.

---

## ✨ Features

*   **🚀 Turbo Mode:** Increase the process priority of any selected window (High or Normal) for better performance.
*   **🖥 Stretch & Aspect Ratio:** Enable screen stretching similar to CS:GO (works via Windows Registry).
*   **🌀 Motion Blur:** Adds a dynamic blur effect based on mouse movement speed.
*   **📊 FPS & Ping Overlay:** A custom overlay that displays FPS (for Roblox) and network ping.
*   **🎯 Custom Crosshair:** A fully customizable crosshair overlay (Cross, Dot, Circle, Triangle, or Custom Image) that stays on top of all windows.
*   **⌨️🖱 Input Widget:** On-screen display for keyboard keys (WASD, Space, Shift, Ctrl) and mouse clicks (Left, Right, Middle).
*   **🌙 Screen Brightness:** Adjust your monitor's brightness directly from the app.
*   **📸 Screenshot Tool:** Take a screenshot with a 3-second countdown.
*   **🎥 Screen Recorder:** Coming...
*   **💬 Feedback Form:** Send feedback or bug reports directly to a Google Form.
*   **🌍 Multi-language Support:** English and Russian languages available. The language is selected on first launch.
*   **💾 Config System:** Save, load, and delete custom configurations.

---

## 🛠 Requirements & Installation

### Prerequisites

*   **Windows OS** (7/8/10/11)
*   **Python 3.7+** installed on your system.

### Installation

1.  **Clone the repository** (or download the `iluzion.py` file).
    ```bash
    git clone https://github.com/your-username/iluzion.git
    cd iluzion
Install the required dependencies.

bash
pip install -r requirements.txt
Dependencies:

tkinter (Usually built-in with Python)

Pillow

pywin32

pynput

keyboard

Run the application.

bash
python iluzion.py
🎮 How to Use
First Launch: A language selection window will appear. Choose English or Русский.

Select a Tab: Use the left sidebar to switch between features.

Turbo: Select a window from the list and press "Apply All".

Quality: Enable Stretch or Motion Blur.

Comfort: Adjust Brightness.

Tools: Enable the FPS Overlay or Input Widget. Take a screenshot.

Record: Start/Stop screen recording.

Crosshair: Customize and enable your crosshair.

Feedback: Send feedback.

Applying Settings: After configuring your desired settings, click the ▶️ Apply All button at the bottom of the main window.

Stopping All: Click the ⏹️ Stop All button to disable all active features.

Emergency Rollback: Press Ctrl+J to reset all settings immediately.

Configs: Use the top panel to create New, Save, or Delete configurations.

⚙️ Config System
Settings are saved as JSON files in:
Documents/Iluzion/Configs/

The default configuration is stored in default.json. You can create and switch between multiple config profiles.
