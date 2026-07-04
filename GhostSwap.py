import gradio as gr
import cv2
import time
import sys
import os
import hashlib
import getpass
import shutil
from swapper import UltraSwapper

# -----------------------------
# TERMINAL BANNER
# -----------------------------
def type_writer(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def center(text):
    width = shutil.get_terminal_size().columns
    return text.center(width)

def show_banner():
    os.system("cls" if os.name == "nt" else "clear")

    print("\033[96m")

    ghost = [
        " ██████   ██   ██   ██████   ███████ ████████ ",
        "██        ██   ██  ██    ██  ██         ██    ",
        "██   ███  ███████  ██    ██  ███████    ██    ",
        "██    ██  ██   ██  ██    ██       ██    ██    ",
        " ██████   ██   ██   ██████   ███████    ██    "
    ]

    for line in ghost:
        print(center(line))

    print("\033[91m")
    print(center("G H O S T   S W A P"))

    print("\033[96m")
    print(center("Control the identity. Control the reality.\n"))

    print("\033[92m")
    print(center("Author: D4RKKD3V1L"))

    print("\033[96m")
    print(center("=" * 60))

    print("\033[0m")

    type_writer("\n>> Initializing engine...", 0.02)
    type_writer(">> Loading AI models...", 0.02)
    type_writer(">> Syncing face embeddings...", 0.02)
    type_writer(">> System ready.\n", 0.02)

    time.sleep(1)


# -----------------------------
# AUTH SYSTEM (FINAL)
# -----------------------------
def authenticate():
    MAX_ATTEMPTS = 3
    PASS_FILE = "password.hash"

    def hash_password(pw):
        return hashlib.sha256(pw.encode()).hexdigest()

    # First time setup
    if not os.path.exists(PASS_FILE):
        print("\n=== FIRST TIME SETUP ===")

        while True:
            pw1 = getpass.getpass("Create new password: ")
            pw2 = getpass.getpass("Confirm password: ")

            if pw1 != pw2:
                print("Passwords do not match.\n")
            elif len(pw1) < 4:
                print("Password too short.\n")
            else:
                with open(PASS_FILE, "w") as f:
                    f.write(hash_password(pw1))
                print("\nPassword set successfully.\n")
                return True

    # Login
    with open(PASS_FILE, "r") as f:
        stored_hash = f.read().strip()

    print("\n=== LOGIN REQUIRED ===")

    for _ in range(MAX_ATTEMPTS):
        entered = getpass.getpass("Enter password: ")

        if hash_password(entered) == stored_hash:
            print("\nAccess Granted.\n")
            return True
        else:
            print("Incorrect password.")

    print("\nToo many failed attempts. Exiting...")
    return False


# -----------------------------
# SWAP FUNCTION (INIT LAZY)
# -----------------------------
swapper = None

def swap_function(source, target, enhance):
    global swapper

    if swapper is None:
        swapper = UltraSwapper()

    if source is None or target is None:
        return None, "Error: Upload both images"

    cv2.imwrite("temp_src.jpg", source)
    cv2.imwrite("temp_tgt.jpg", target)

    result, msg = swapper.swap("temp_src.jpg", "temp_tgt.jpg", enhance)
    return result, msg


# -----------------------------
# CYBER UI CSS
# -----------------------------
css = """
html, body, .gradio-container {
    margin: 0;
    padding: 0;
    height: 100%;
    background: #000;
    overflow-x: hidden;
    font-family: 'Orbitron', sans-serif;
}

body::before {
    content: "";
    position: fixed;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 20% 30%, rgba(0,255,255,0.15), transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(0,150,255,0.15), transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(0,255,150,0.1), transparent 60%);
    animation: bgMove 18s ease-in-out infinite alternate;
    z-index: -3;
}

@keyframes bgMove {
    0% { transform: translate(0,0); }
    100% { transform: translate(-10%, -10%); }
}

.particles {
    position: fixed;
    width: 100%;
    height: 100%;
    z-index: -2;
}

.particles span {
    position: absolute;
    width: 3px;
    height: 3px;
    background: cyan;
    box-shadow: 0 0 10px cyan;
    border-radius: 50%;
    animation: float linear infinite;
}

@keyframes float {
    from { transform: translateY(100vh); opacity: 0; }
    20% { opacity: 1; }
    to { transform: translateY(-10vh); opacity: 0; }
}

.particles span:nth-child(1){ left:10%; animation-duration:12s;}
.particles span:nth-child(2){ left:25%; animation-duration:18s;}
.particles span:nth-child(3){ left:40%; animation-duration:15s;}
.particles span:nth-child(4){ left:60%; animation-duration:20s;}
.particles span:nth-child(5){ left:75%; animation-duration:17s;}
.particles span:nth-child(6){ left:90%; animation-duration:22s;}

button {
    background: rgba(0,0,0,0.6) !important;
    color: cyan !important;
    border: 1px solid cyan !important;
    border-radius: 10px !important;
}
"""


# -----------------------------
# UI
# -----------------------------
with gr.Blocks(css=css) as demo:

    gr.HTML("""
    <div class="particles">
      <span></span><span></span><span></span>
      <span></span><span></span><span></span>
    </div>
    """)

    gr.HTML("""
    <div style="text-align:center; margin-top:20px;">
        <h1 style="font-size:48px; color:cyan;">GhostSwap</h1>
        <p style="color:#00ffff;">Control the identity. Control the reality.</p>
        <p style="color:#00ff99;">by D4RKKD3V1L</p>
    </div>
    """)

    with gr.Row():
        source = gr.Image(label="Source Face", type="numpy")
        target = gr.Image(label="Target Image", type="numpy")

    enhance = gr.Checkbox(label="Enhance Output", value=True)
    run_btn = gr.Button("START PROCESS")

    result = gr.Image(label="Result")
    status = gr.Textbox(label="System Status")

    run_btn.click(
        fn=swap_function,
        inputs=[source, target, enhance],
        outputs=[result, status]
    )


# -----------------------------
# RUN SYSTEM
# -----------------------------
if __name__ == "__main__":
    show_banner()

    if not authenticate():
        sys.exit()

    input("Press ENTER to launch GhostSwap interface...")

    print("\nLaunching interface...\n")

    demo.launch(
        share=False,
        inbrowser=True,

        quiet=True
    )