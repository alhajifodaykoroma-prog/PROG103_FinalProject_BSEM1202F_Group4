import os
import sqlite3
import sys
from tkinter import *
from tkinter import messagebox

# ===================== CLINICAL THEME =====================
NAVY      = "#0B1F3A"
TEAL      = "#0E7C7B"
TEAL_DK   = "#0A5C5B"
ACCENT    = "#14B8A6"
APP_BG    = "#EEF3F8"
CARD_BG   = "#FFFFFF"
BORDER    = "#D7E0EC"
TEXT_DARK = "#0F2440"
TEXT_MUTE = "#64748B"
DANGER    = "#D7443E"
FONT      = "Lato"


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def draw_vertical_gradient(canvas, width, height, color_top, color_bottom):
    r1, g1, b1 = _hex_to_rgb(color_top)
    r2, g2, b2 = _hex_to_rgb(color_bottom)
    steps = max(height, 1)
    for i in range(steps):
        ratio = i / steps
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        canvas.create_line(0, i, width, i, fill=f"#{r:02x}{g:02x}{b:02x}")


# Main Login Window
root = Tk()
root.title("Clinic Management Login")
root.geometry("940x580")
root.config(bg=APP_BG)
root.resizable(False, False)

# Variables
username_var = StringVar()
password_var = StringVar()


# Login Function
def login():
    username = username_var.get().strip()
    password = password_var.get().strip()

    # Validation
    if not username or not password:
        messagebox.showerror(
            "Error",
            "Please enter username and password"
        )
        return

    # Database Connection
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    # Check User
    cursor.execute('''
    SELECT * FROM users
    WHERE username=? AND password=?
    ''', (username, password))

    user = cursor.fetchone()
    conn.close()

    # If user exists
    if user:
        messagebox.showinfo(
            "Login Success",
            f"Welcome {username}"
        )
        root.destroy()

        # Secure System Execution Pathing
        os.system(f'"{sys.executable}" main.py')
    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password"
        )


# ---- Hover helper ----
def _hover(btn, normal, hover):
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=normal))


# ============ LAYOUT: brand panel + form card ============
container = Frame(root, bg=APP_BG)
container.pack(fill=BOTH, expand=True)

# ---- LEFT BRAND PANEL (navy -> teal gradient) ----
left = Frame(container, width=420, height=580)
left.pack(side=LEFT, fill=Y)
left.pack_propagate(False)

brand_canvas = Canvas(left, width=420, height=580, highlightthickness=0, bd=0)
brand_canvas.pack(fill=BOTH, expand=True)
draw_vertical_gradient(brand_canvas, 420, 580, NAVY, TEAL)
brand_canvas.create_text(210, 215, text="\u271a", font=(FONT, 70, "bold"), fill="white")
brand_canvas.create_text(
    210, 305,
    text="COMMUNITY HEALTH SYSTEM",
    font=(FONT, 19, "bold"),
    fill="white",
    width=340,
    justify="center"
)
brand_canvas.create_line(150, 350, 270, 350, fill=ACCENT, width=3)


# ---- RIGHT FORM CARD ----
right = Frame(container, bg=APP_BG)
right.pack(side=LEFT, fill=BOTH, expand=True)

card = Frame(right, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)

Label(
    card,
    text="System Login",
    font=(FONT, 23, "bold"),
    bg=CARD_BG,
    fg=TEXT_DARK
).pack(pady=(46, 6))

Frame(card, bg=ACCENT, height=3, width=48).pack(pady=(0, 30))

# Username Layout Elements
Label(
    card,
    text="Username",
    font=(FONT, 10, "bold"),
    bg=CARD_BG,
    fg=TEXT_MUTE,
    anchor="w"
).pack(fill=X, padx=46)

u_wrap = Frame(card, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
u_wrap.pack(padx=46, pady=(6, 18), fill=X)
Entry(
    u_wrap,
    textvariable=username_var,
    font=(FONT, 12),
    bd=0,
    bg=CARD_BG,
    fg=TEXT_DARK,
    insertbackground=TEAL
).pack(fill=X, ipady=9, padx=12)

# Password Layout Elements
Label(
    card,
    text="Password",
    font=(FONT, 10, "bold"),
    bg=CARD_BG,
    fg=TEXT_MUTE,
    anchor="w"
).pack(fill=X, padx=46)

p_wrap = Frame(card, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
p_wrap.pack(padx=46, pady=(6, 28), fill=X)
Entry(
    p_wrap,
    textvariable=password_var,
    show="*",
    font=(FONT, 12),
    bd=0,
    bg=CARD_BG,
    fg=TEXT_DARK,
    insertbackground=TEAL
).pack(fill=X, ipady=9, padx=12)


# Interactive Process Trigger Keys Buttons
login_btn = Button(
    card,
    text="LOGIN",
    font=(FONT, 12, "bold"),
    bg=TEAL,
    fg="white",
    activebackground=TEAL_DK,
    activeforeground="white",
    bd=0,
    cursor="hand2",
    command=login
)
login_btn.pack(padx=46, fill=X, ipady=11)
_hover(login_btn, TEAL, TEAL_DK)

exit_btn = Button(
    card,
    text="EXIT",
    font=(FONT, 10, "bold"),
    bg=CARD_BG,
    fg=TEXT_MUTE,
    activebackground=CARD_BG,
    activeforeground=DANGER,
    bd=0,
    cursor="hand2",
    command=root.destroy
)
exit_btn.pack(pady=(18, 0))
exit_btn.bind("<Enter>", lambda e: exit_btn.config(fg=DANGER))
exit_btn.bind("<Leave>", lambda e: exit_btn.config(fg=TEXT_MUTE))

root.mainloop()
