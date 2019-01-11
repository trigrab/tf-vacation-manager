from jinja2 import Template, FileSystemLoader, Environment
from tkinter import Tk, Frame, Label, StringVar
from pyDatePicker import Datepicker
import sys
import tkinter.ttk as ttk

templateLoader = FileSystemLoader(searchpath="./")
templateEnv = Environment(loader=templateLoader)
template_file = "vacation_template.txt"
template = templateEnv.get_template(template_file)


root = Tk()
root.geometry("500x600")

start_date = StringVar()
end_date = StringVar()


def get_template():
    output_text = template.render(start_date=start_date.get(), end_date=end_date.get(), username="ntw")
    print(output_text)

main = Frame(root, pady=15, padx=15)
main.pack(expand=True, fill="both")

Label(main, justify="left", text="Urlaub vom").pack(anchor="w", pady=(15, 0))

start = Datepicker(main, datevar=start_date).pack(anchor="w", )

Label(main, justify="left", text="Urlaub bis").pack(anchor="w", pady=(15, 0))

Datepicker(main, datevar=end_date).pack(anchor="w")

b = ttk.Button(main, text="set", width=10, command=get_template).pack(anchor="w")

if 'win' not in sys.platform:
    style = ttk.Style()
    style.theme_use('clam')

root.mainloop()