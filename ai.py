import json_functions
import json
import tkinter as tk
from tkinter import filedialog
import terminal_commands

lines_of_q_and_a = 0

def append_text(user_input):
    global knowledge_base
    global lines_of_q_and_a
    
    user_input = user_input.strip()
    conversation_label.config(text=conversation_label.cget("text") + f"\n{name}: {user_input}")
    
    if lines_of_q_and_a > 20:
        conversation_label.config(text="")
    
    if user_input == "help":
        lines_of_q_and_a += 7
        terminal_commands.help(conversation_label)
    elif user_input == "render3d":
        lines_of_q_and_a += 1
        terminal_commands.render()
    elif user_input == "video":
        lines_of_q_and_a += 1
        terminal_commands.video()
    elif user_input == "math":
        lines_of_q_and_a += 2
        terminal_commands.math_command(root)
        conversation_label.config(text=conversation_label.cget("text") + f"\nPandaAI: Doing math.")
    elif user_input == "uwu" or user_input == "UwU":
        leave_program()
    elif user_input == "date":
        lines_of_q_and_a += 2
        conversation_label.config(text=conversation_label.cget("text") + f"\nPandaAI: {terminal_commands.date()}")
    elif user_input == "time":
        lines_of_q_and_a += 2
        conversation_label.config(text=conversation_label.cget("text") + f"\nPandaAI: {terminal_commands.time()}")
    elif user_input == "gif":
        lines_of_q_and_a += 1
        terminal_commands.show_gif(filedialog, root)
    else:
        lines_of_q_and_a += 2
        best_match_question = json_functions.best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        if best_match_question:
            answer = json_functions.get_answer(best_match_question, knowledge_base)
            if answer:
                conversation_label.config(text=conversation_label.cget("text") + f"\nPandaAI: {answer}")
            else:
                conversation_label.config(text=conversation_label.cget("text") + f"\nPandaAI: None of my bamboo books say anything about that. Maybe you could teach me.")
        else:
            conversation_label.config(text=conversation_label.cget("text") + f"\nPandaAI: None of my bamboo books say anything about that. Maybe you could teach me.")

def delete_question(index):
    global knowledge_base
    global question_entries, answer_entries
    
    del knowledge_base["questions"][index]
    
    question_entries[index].destroy()
    answer_entries[index].destroy()
    
    del question_entries[index]
    del answer_entries[index]
    
    json_functions.save('knowledge_base.json', knowledge_base)

def save_question():
    global knowledge_base
    try:
        for i, (question, answer) in enumerate(zip(question_entries, answer_entries)):
            if i < len(knowledge_base["questions"]):
                knowledge_base["questions"][i]["question"] = question.get()
                knowledge_base["questions"][i]["answer"] = answer.get()
            else:
                knowledge_base["questions"].append({"question": question.get(), "answer": answer.get()})
        json_functions.save('knowledge_base.json', knowledge_base)
        hide_questions_menu()
    except IndexError:
        print("Error: Index out of range while saving questions.")

def show_questions_menu():
    global question_menu_frame, question_entries, answer_entries
    
    def add_question():
        question_entry = tk.Entry(question_menu_frame, width=50)
        question_entry.grid(row=len(question_entries) + 1, column=1)
        
        answer_entry = tk.Entry(question_menu_frame, width=50)
        answer_entry.grid(row=len(answer_entries) + 1, column=3)
        
        delete_button = tk.Button(question_menu_frame, text="Delete", command=lambda i=len(question_entries): delete_question(i))
        delete_button.grid(row=len(question_entries) + 1, column=4)
        
        question_entries.append(question_entry)
        answer_entries.append(answer_entry)
        
        add_button.grid(row=len(question_entries) + 2, column=1, columnspan=2)
        save_button.grid(row=len(question_entries) + 2, column=3, columnspan=2)
    
    question_menu_frame = tk.Frame(root)
    question_menu_frame.pack(pady=10)
    question_label = tk.Label(question_menu_frame, text="Questions Menu", font=('Helvetica', 14, 'bold'))
    question_label.grid(row=0, column=0, columnspan=4)
    question_entries = []
    answer_entries = []
    
    for i, q in enumerate(knowledge_base.get("questions", [])):
        question_label = tk.Label(question_menu_frame, text="Question:")
        question_label.grid(row=i+1, column=0)
        question_entry = tk.Entry(question_menu_frame, width=50)
        question_entry.insert(tk.END, q["question"])
        question_entry.grid(row=i+1, column=1)
        question_entries.append(question_entry)

        answer_label = tk.Label(question_menu_frame, text="Answer:")
        answer_label.grid(row=i+1, column=2)
        answer_entry = tk.Entry(question_menu_frame, width=50)
        answer_entry.insert(tk.END, q["answer"])
        answer_entry.grid(row=i+1, column=3)
        answer_entries.append(answer_entry)
        
        delete_button = tk.Button(question_menu_frame, text="Delete", command=lambda i=i: delete_question(i))
        delete_button.grid(row=i+1, column=4)
    
    add_button = tk.Button(question_menu_frame, text="Add Question", command=add_question)
    add_button.grid(row=len(question_entries) + 1, column=1, columnspan=2)

    save_button = tk.Button(question_menu_frame, text="Save Changes", command=save_question)
    save_button.grid(row=len(question_entries) + 1, column=3, columnspan=2)

def hide_questions_menu():
    global question_menu_frame
    question_menu_frame.destroy()

def show_new_question_form():
    global question_entry, answer_entry
    new_question_frame = tk.Frame(root)
    new_question_frame.pack(pady=10)
    question_label = tk.Label(new_question_frame, text="New Question:")
    question_label.pack()
    question_entry = tk.Entry(new_question_frame, width=50)
    question_entry.pack(pady=5)
    answer_label = tk.Label(new_question_frame, text="Answer:")
    answer_label.pack()
    answer_entry = tk.Entry(new_question_frame, width=50)
    answer_entry.pack(pady=5)
    save_button = tk.Button(new_question_frame, text="Save", command=save_question)
    save_button.pack(pady=5)

def leave_program():
    root.destroy()

def show_name_window():
    global name_window, name_entry
    name_window = tk.Frame(root)
    name_window.pack(pady=10)
    name_label = tk.Label(name_window, text="Enter your name:")
    name_label.pack(pady=5)
    name_entry = tk.Entry(name_window, width=30)
    name_entry.pack(pady=5)
    save_button = tk.Button(name_window, text="Save", command=lambda: save_name('settings.json'))
    save_button.pack(pady=5)

def hide_name_window():
    name_window.destroy()

def save_name(settings_file):
    global name_entry
    global name
    name = name_entry.get()
    name_entry.delete(0, tk.END)
    
    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {}

    settings['name'] = name

    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)
    
    hide_name_window()

settings_file = 'settings.json'
name = json_functions.load_name(settings_file)

root = tk.Tk()
root.title("PandaAI")

icon_file = tk.PhotoImage(file='pandaaiicon.ico')
root.iconphoto(False, icon_file)

knowledge_base = json_functions.load('knowledge_base.json')
question_menu_frame = None

conversation_label = tk.Label(root, text="")
conversation_label.pack(pady=10)

input_field = tk.Entry(root)
input_field.pack(pady=5)

say_button = tk.Button(root, text="Say", command=lambda: append_text(input_field.get()))
say_button.pack(pady=5)

change_name_button = tk.Button(root, text="Change Name", command=show_name_window)
change_name_button.pack(pady=5)

leave_button = tk.Button(root, text="Leave", command=leave_program)
leave_button.pack(side="bottom", pady=10)

json_editor_button = tk.Button(root, text="Open Questions Menu", command=show_questions_menu)
json_editor_button.pack(side="bottom", pady=10)

root.attributes('-fullscreen', True)

root.mainloop()