from tkinter import *
from tkinter import filedialog
from audit_parser import parse_audit_file


class CsLab1(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(side=BOTTOM)
        self.parent = parent
        self.parent.configure(background='white')

        self.openBt = Button(self, text="Open file", command=self.openFile,

                                 width=15, height=1, bg="#F5DD9F", fg="#000000", font=("Arial", "15"))
        self.openBt.pack(side=LEFT)

        self.saveBt = Button(self, text="Save file", command=self.saveFile,
                                 width=15, height=1, bg="#A0F6A5", fg="#000000", font=("Arial", "15"))
        self.saveBt.pack(side=RIGHT)

        self.textField = Text(bg="#AFD1FA", fg="black", font=("Arial", "15"))
        self.textField.pack(fill=BOTH, expand=1)

    def openFile(self):
        file = filedialog.askopenfile(mode="r", defaultextension=".audit")

        if not file:
            return

        f = open(file.name, "r")

        structure = parse_audit_file(f.read())

        form = '{}{}'

        self.textField.config(state=NORMAL)

        for (line, depth, text) in structure:
            self.textField.insert(END, form.format('.  ' * depth, text))
            self.textField.insert(END, '\n')

        self.textField.config(state=DISABLED)

    def saveFile(self):
        file = filedialog.asksaveasfile(mode="w", defaultextension=".audit")
        f = open(file.name, "w")
        f.write(self.textField.get("1.0", END))
        f.close()


def main():
    root = Tk()
    app = CsLab1(root)
    root.title("Tolici Constantin. CSLAB-1. FAF-193")
    root.geometry("1200x860")
    root.mainloop()


if __name__ == '__main__':
    main()
