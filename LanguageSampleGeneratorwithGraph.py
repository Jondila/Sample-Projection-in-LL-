import tkinter as tk
from tkinter import messagebox, LabelFrame, font, filedialog
from itertools import combinations
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Global variables to hold state
set_sizes = []
current_fig = None

# Generate a random hex color
def random_color():
    return f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"

# Generate sets and populate output
def generate_sets():
    global set_sizes
    langs = entry_languages.get().strip()

    if not langs:
        messagebox.showwarning("Input Missing", "Please enter the languages.")
        return

    if langs.replace(",", "").replace(" ", "").isnumeric():
        messagebox.showerror("Wrong Input", "Only numbers detected. Please enter language names.")
        return

    if " " in langs and "," not in langs:
        messagebox.showerror("Missing Commas", "Please separate languages using commas (e.g., English, French).")
        return

    if "  " in langs:
        messagebox.showwarning("Multiple Spaces Detected", "Multiple spaces found. Did you forget a comma between languages?")
        return

    if ",," in langs:
        messagebox.showerror("Multiple Commas Detected", "Multiple commas found. Please remove extra commas.")
        return

    items = [lang.strip() for lang in langs.split(',') if lang.strip()]
    for item in items:
        if len(item.split()) > 1:
            messagebox.showerror(
                "Possible Missing Comma",
                f"Detected multiple words in one entry: '{item}'.\n"
                "You may have forgotten a comma. Please check your input."
            )
            return

    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    set_sizes = []

    all_sets = []
    for r in range(1, len(items) + 1):
        for combo in combinations(items, r):
            joined = ", ".join(combo)
            all_sets.append(joined)
            set_sizes.append(len(combo))

    for i, s in enumerate(all_sets, 1):
        color = random_color()
        tag_name = f"color{i}"
        output_box.insert(tk.END, f"Set {i}: {{ {s} }}\n", tag_name)
        output_box.tag_config(tag_name, foreground=color)

    output_box.config(state=tk.DISABLED)

# Clear output and graph
def clear_results():
    global set_sizes, current_fig
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.config(state=tk.DISABLED)
    for widget in graph_frame.winfo_children():
        widget.destroy()
    set_sizes = []
    current_fig = None

# Plot bar + line graph
def plot_graph():
    global current_fig
    if not set_sizes:
        messagebox.showinfo("No Data", "Please generate sets first.")
        return

    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5, 3.2), dpi=100)
    x = list(range(1, len(set_sizes) + 1))
    y = set_sizes

    ax.bar(x, y, label='Set Size', color='skyblue')
    ax.plot(x, y, color='darkblue', marker='o', label='Trend Line')

    ax.set_title("Set Sizes")
    ax.set_xlabel("Set Number")
    ax.set_ylabel("Number of Languages")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    current_fig = fig

# Save current graph as image
def save_graph():
    global current_fig
    if not current_fig:
        messagebox.showinfo("No Graph", "Please generate or plot a graph first.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpeg"), ("PDF Document", "*.pdf"), ("All Files", "*.*")]
    )

    if file_path:
        try:
            current_fig.savefig(file_path)
            messagebox.showinfo("Success", f"Graph saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph.\n{e}")

# ---------------- GUI SETUP ---------------- #
root = tk.Tk()
root.title("SPLG with Graph")
root.geometry("1100x520")

# Define font
main_font = font.Font(family="Times New Roman", size=10)

# Label and Entry
label_languages = tk.Label(root, text="Languages (comma-separated):", font=main_font)
label_languages.grid(row=0, column=0, sticky="w", padx=10, pady=10)

entry_languages = tk.Entry(root, width=45, font=main_font)
entry_languages.insert(0, "English, French, German, Italian")
entry_languages.grid(row=1, column=0, padx=10, pady=5)

# Buttons
btn_generate = tk.Button(root, text="Generate Sets", command=generate_sets, font=main_font)
btn_generate.grid(row=2, column=0, padx=10, pady=5, sticky="w")

btn_clear = tk.Button(root, text="Clear Results", command=clear_results, font=main_font)
btn_clear.grid(row=3, column=0, padx=10, pady=5, sticky="w")

btn_plot = tk.Button(root, text="Plot Graph", command=plot_graph, font=main_font)
btn_plot.grid(row=4, column=0, padx=10, pady=5, sticky="w")

btn_save = tk.Button(root, text="Save Graph", command=save_graph, font=main_font)
btn_save.grid(row=5, column=0, padx=10, pady=5, sticky="w")

# Output section
output_frame = LabelFrame(root, text="Output Results", padx=5, pady=5, font=main_font)
output_frame.grid(row=0, column=1, rowspan=8, padx=10, pady=10, sticky="n")

output_box = tk.Text(output_frame, height=22, width=45, wrap=tk.WORD, font=main_font)
scrollbar = tk.Scrollbar(output_frame, orient=tk.VERTICAL, command=output_box.yview)
output_box.configure(yscrollcommand=scrollbar.set)

output_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_box.config(state=tk.DISABLED)

# Graph section with 5px left padding
graph_frame = LabelFrame(root, text="Set Size Graph", padx=5, pady=5, font=main_font)
graph_frame.grid(row=0, column=2, rowspan=8, padx=(5, 10), pady=10, sticky="nsew")

root.mainloop()