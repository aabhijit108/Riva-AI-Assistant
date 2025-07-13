import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import riva_assistant  # Your assistant must return (logs, code)

class RivaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Riva - AI Female Assistant")
        self.root.geometry("780x680")
        self.root.configure(bg="#121212")

        # Header
        tk.Label(
            root,
            text="💫 Riva - Female AI Desktop Assistant",
            font=("Segoe UI", 20, "bold"),
            bg="#121212",
            fg="#00ffe7"
        ).pack(pady=20)

        # Status Label
        self.status_label = tk.Label(
            root,
            text="Status: 💤 Idle",
            font=("Segoe UI", 12),
            bg="#121212",
            fg="#32cd32"
        )
        self.status_label.pack()

        # Unified Output + Code Box
        self.output_box = scrolledtext.ScrolledText(
            root,
            width=85,
            height=24,
            font=("Consolas", 11),
            bg="#1e1e1e",
            fg="#00ffcc",
            insertbackground="white",
            bd=0,
            relief="flat"
        )
        self.output_box.pack(padx=15, pady=10)
        self.output_box.configure(state='disabled')

        # Copy Button
        self.copy_button = tk.Button(
            root,
            text="📋 Copy All to Clipboard",
            font=("Segoe UI", 11),
            bg="#3949ab",
            fg="white",
            activebackground="#5c6bc0",
            relief="flat",
            padx=10,
            pady=5,
            command=self.copy_output_to_clipboard
        )
        self.copy_button.pack(pady=(0, 10))

        # Button Frame
        button_frame = tk.Frame(root, bg="#121212")
        button_frame.pack(pady=10)

        self.listen_button = tk.Button(
            button_frame,
            text="🎤 Talk to Riva",
            font=("Segoe UI", 12),
            bg="#00c853",
            fg="white",
            activebackground="#00e676",
            relief="flat",
            padx=20,
            pady=5,
            command=self.start_listening_thread
        )
        self.listen_button.grid(row=0, column=0, padx=10)

        self.quit_button = tk.Button(
            button_frame,
            text="❌ Shut Down",
            font=("Segoe UI", 12),
            bg="#d50000",
            fg="white",
            activebackground="#ff1744",
            relief="flat",
            padx=20,
            pady=5,
            command=root.quit
        )
        self.quit_button.grid(row=0, column=1, padx=10)

    def log(self, text, emoji="🤖"):
        self.output_box.configure(state='normal')
        self.output_box.insert("end", f"{emoji} {text}\n")
        self.output_box.see("end")
        self.output_box.configure(state='disabled')

    def log_code(self, code):
        self.output_box.configure(state='normal')
        self.output_box.insert("end", "\n📄 Code Output:\n", "bold")
        self.output_box.insert("end", f"{code}\n")
        self.output_box.see("end")
        self.output_box.configure(state='disabled')

    def copy_output_to_clipboard(self):
        text = self.output_box.get("1.0", tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
            messagebox.showinfo("Copied", "✅ Output copied to clipboard!")
        else:
            messagebox.showwarning("No Output", "⚠️ There's nothing to copy!")

    def start_listening_thread(self):
        self.status_label.config(text="Status: 🎧 Listening...", fg="yellow")
        threading.Thread(target=self.run_riva, daemon=True).start()

    def run_riva(self):
        try:
            logs, code = riva_assistant.run_riva()
            for log in logs:
                self.log(log)
            if code:
                self.log_code(code)
        except Exception as e:
            self.log(f"Error: {e}")
        finally:
            self.status_label.config(text="Status: 💤 Idle", fg="#32cd32")


if __name__ == "__main__":
    root = tk.Tk()
    app = RivaApp(root)
    root.mainloop()
