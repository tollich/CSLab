from tkinter import *
from tkinter import Tk, Text, BOTH, W, N, E, S, filedialog
from tkinter.ttk import Frame, Button, Label
from audit_parser import parse_audit_file
from winregistry import WinRegistry as Reg


class SBT(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.master.title("SBT")
        self.pack(fill=BOTH, expand=True)

        self.entry_value = StringVar()
        self.entry_value.trace('w', self.showSearchResults)

        self.columnconfigure((1, 3), weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(5, weight=1)

        search_label = Label(self, text="Search:")
        search_label.grid(sticky=N + E, row=0, column=0, padx=10, pady=6)

        self.searchEntry = Entry(self, textvariable=self.entry_value)
        self.searchEntry.grid(sticky=E + W + S + N, row=0, column=1, columnspan=3, pady=4)

        open_button = Button(self, text="Open .audit file", command=self.openFile)
        open_button.grid(sticky=S, row=6, column=0, pady=6, padx=70)

        save_button = Button(self, text="Save .audit file", command=self.saveFile)
        save_button.grid(sticky=S, row=6, column=4, pady=6, padx=70)

        test_button = Button(self, text="Test", command=self.openNewWindow)
        test_button.grid(sticky=S, row=6, column=2, pady=6)

        select_all_button = Button(self, text="Select all options", command=self.selectAll)
        select_all_button.grid(sticky=S, row=6, column=1, pady=6)

        deselect_all_button = Button(self, text="Deselect all options", command=self.deselectAll)
        deselect_all_button.grid(sticky=S, row=7, column=1, pady=6)

        enforce_button = Button(self, text="Enforce", command=self.enforce)
        enforce_button.grid(sticky=S, row=6, column=3, pady=6)

        rollback_button = Button(self, text="Rollback", command=self.rollback)
        rollback_button.grid(sticky=S, row=7, column=3, pady=6)

        self.list = Listbox(self, selectmode='multiple')
        self.list.grid(row=1, column=0, columnspan=5, rowspan=4, sticky=E + W + S + N)
        self.list.config(width=0, height=0)

        self.scrollbar = Scrollbar(self)
        self.list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.list.yview)
        self.scrollbar.grid(column=5, row=1, rowspan=4, sticky=N + S + W)

        self.listContent = list()

    def openNewWindow(self):

        newWindow = Toplevel(self)
        newWindow.title("Security Test")
        newWindow.geometry("800x400")

        newWindow.columnconfigure(1, weight=1)
        newWindow.rowconfigure(1, weight=1)

        a_file = open("test.txt", "w")

        reg = Reg()

        for i in self.list.curselection():
            try:
                z = (item_type[i])[1:]
                if z == 'REGISTRY_SETTING':
                    path = (reg_key[i])[2:-1]
                    y = reg.read_value(path, (reg_item[i])[2:-1])['value']
                    value_data = int((val_data[i])[2:-1])
                    info = (output[i])[2:-1]
                    x = reg.read_value(path, y)['data']

                    print(i + 1, ')', info, '\nreg_item:', y, file=a_file)

                    if x == value_data:
                        print('Success\n', file=a_file)
                        self.list.itemconfig(i, {'bg': 'green'})

                    else:
                        print('value_data is set to:', x, file=a_file)
                        print('value_data must be set to:', value_data, file=a_file)
                        print('Failure\n', file=a_file)
                        self.list.itemconfig(i, {'bg': 'red'})

                if z == 'USER_RIGHTS_POLICY':
                    info = (output[i])[2:-1]
                    print(i + 1, ')', info, file=a_file)
                    print('Not implemented yet.\n', file=a_file)

            except:
                print(i + 1, ')', 'Path not found.', file=a_file)
                print(path, '\n', file=a_file)
                self.list.itemconfig(i, {'bg': 'light gray'})
                pass  # doing nothing on exception

        a_file.close()

        newWindow.textBox = Text(newWindow)
        newWindow.textBox.grid(row=0, column=0, columnspan=5, rowspan=4, sticky=E + W + S + N)

        newWindow.scrollbar = Scrollbar(newWindow)
        newWindow.textBox.config(yscrollcommand=newWindow.scrollbar.set)
        newWindow.scrollbar.config(command=newWindow.textBox.yview)
        newWindow.scrollbar.grid(column=5, row=0, rowspan=4, sticky=N + S + W)

        with open('test.txt', "r") as f:
            data = f.readlines()
        for x in data:
            newWindow.textBox.insert(END, x)

        # self.list.selection_clear(0, END)

    def enforce(self):
        f = open("rollback.txt", "w")
        reg = Reg()

        for i in range(len(structure)):
            try:
                path = (reg_key[i])[2:-1]
                y = reg.read_value(path, (reg_item[i])[2:-1])['value']
                x = reg.read_value(path, y)['data']
                print(x, file=f)

            except:
                print('-1', file=f)
                pass  # doing nothing on exception

        f.close()

        global rb
        rb = []
        with open('rollback.txt') as my_file:
            for line in my_file:
                rb.append(line.rstrip())

        for i in self.list.curselection():

            z = (item_type[i])[1:]
            if z == 'REGISTRY_SETTING':
                path = (reg_key[i])[2:-1]
                y = reg.read_value(path, (reg_item[i])[2:-1])['value']
                value_data = int((val_data[i])[2:-1])
                x = reg.read_value(path, y)['data']

                if x != value_data:
                    reg.write_value(path, y, value_data, 'REG_DWORD')

    def rollback(self):
        reg = Reg()
        for i in self.list.curselection():
            z = (item_type[i])[1:]
            if z == 'REGISTRY_SETTING':
                path = (reg_key[i])[2:-1]
                y = reg.read_value(path, (reg_item[i])[2:-1])['value']

                reg.write_value(path, y, int(rb[i]), 'REG_DWORD')

    def showSearchResults(self, *args):
        search = self.entry_value.get()
        self.list.delete(0, END)
        for item in self.listContent:
            if search.lower() in item.lower():
                self.list.insert(END, item)

    def selectAll(self):
        self.list.select_set(0, END)

    def deselectAll(self):
        self.list.selection_clear(0, END)

    def saveFile(self):

        file = filedialog.asksaveasfile(mode="w", filetypes=(("Audit files", "*.audit"), ("All files", "*.*")))

        values = [self.list.get(idx) for idx in self.list.curselection()]
        for idx in self.list.curselection():
            print(idx)

        f = open(file.name, "w")
        f.write(str(values))
        f.close()

    def openFile(self):
        global output
        output = []
        global item_type
        item_type = []
        global val_data
        val_data = []
        global reg_key
        reg_key = []
        global reg_item
        reg_item = []

        file = filedialog.askopenfile(mode="r", filetypes=(("Audit files", "*.audit"), ("All files", "*.*")))

        if not file:
            return

        if file:
            output = []

        f = open(file.name, "r")

        global structure

        structure = []
        structure = parse_audit_file(f.read())

        for struct in structure:
            if 'description' in struct:
                output.append(struct['description'])
            else:
                output.append('Tag (description) does not exist for current item.')

        for struct in structure:
            if 'type' in struct:
                item_type.append(struct['type'])
            else:
                item_type.append('Tag (type) does not exist for current item.')

        for struct in structure:
            if 'value_data' in struct:
                val_data.append(struct['value_data'])
            else:
                val_data.append('Tag (value_data) does not exist for current item.')

        for struct in structure:
            if 'reg_key' in struct:
                reg_key.append(struct['reg_key'])
            else:
                reg_key.append('Tag (reg_key) does not exist for current item.')

        for struct in structure:
            if 'reg_item' in struct:
                reg_item.append(struct['reg_item'])
            else:
                reg_item.append('Tag (reg_item) does not exist for current item.')

        output = output[3:-1]
        item_type = item_type[3:-1]
        val_data = val_data[3:-1]
        reg_key = reg_key[3:-1]
        reg_item = reg_item[3:-1]

        values = StringVar()
        values.set(output)

        form = '{}'

        self.list.delete(0, END)

        for (text) in output:
            self.list.insert(END, form.format(text))

        self.listContent = self.list.get(0, END)


def main():
    root = Tk()
    root.geometry("1000x600")
    app = SBT()
    root.mainloop()


if __name__ == '__main__':
    main()
