import tkinter as tk

root = tk.Tk()
root.title("Smiley")

canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# обличчя: жовте коло
canvas.create_oval(50, 50, 350, 350, fill="yellow", outline="black")

# очі: дві чорні точки
canvas.create_oval(130, 130, 150, 150, fill="black")
canvas.create_oval(250, 130, 270, 150, fill="black")

# ніс: чорна вертикальна лінія
canvas.create_line(200, 160, 200, 220, width=4, fill="black")

# посмішка: крива (нижня частина еліпса)
canvas.create_arc(120, 200, 280, 300, start=200, extent=140,
                  style=tk.ARC, width=4, outline="red")

root.mainloop()