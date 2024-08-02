import datetime
import tdmain
import tkinter as tk
import video_player

def date():
    now = datetime.datetime.now()
    return f"Current date is: {now.strftime('%m-%d-%y')}"

def time():
    now = datetime.datetime.now()
    return f"Current time is: {now.strftime('%H:%M:%S')}"

def show_gif(filedialog, root):
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])

    if file_path:
        gif_window = tk.Toplevel(root)
        gif_window.title("GIF Viewer")
        gif_label = tk.Label(gif_window)
        gif_label.pack()

        icon_file = tk.PhotoImage(file='pandaaiicon.ico')
        gif_window.iconphoto(False, icon_file)
        
        gif_image = tk.PhotoImage(file=file_path)
        gif_label.config(image=gif_image)
        gif_label.image = gif_image

def help(conversation_label):
    conversation_label.config(text=conversation_label.cget("text") + "\n" + f"PandaAI: \"math\" = Use it to make a math equation\nPandaAI: \"date\" = For the current date\nPandaAI: \"time\" = For the current time\nPandaAI: \"gif\" = To show a GIF image\nPandaAI: \"video\" = To play a video\nPandaAI: \"render3d\" = Render a 3d object")

def math_command(root):
    math_window = tk.Toplevel(root)
    math_window.title("Math Command")

    icon_file = tk.PhotoImage(file='pandaaiicon.ico')
    math_window.iconphoto(False, icon_file)

    equation_label = tk.Label(math_window, text="Enter the equation:")
    equation_label.pack(pady=5)

    equation_entry = tk.Entry(math_window, width=30)
    equation_entry.pack(pady=5)

    def calculate():
        equation = equation_entry.get()
        try:
            result = eval(equation)
            result_label.config(text=f"Result: {result}")
        except Exception as e:
            result_label.config(text=f"Error: {e}")

    calculate_button = tk.Button(math_window, text="Calculate", command=calculate)
    calculate_button.pack(pady=5)

    result_label = tk.Label(math_window, text="")
    result_label.pack(pady=5)

def render():
    tdmain.choose_file_and_render()

def video():
    video_player.VideoPlayer()