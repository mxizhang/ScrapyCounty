from Tkinter import *
import scrapycounty
import sys
import item_write
import mercer_convert
import hunterdon_save
from gspread import exceptions

morris = {'name': 'Morris', 'csv': 'morris_items.csv', 'date': 'Thr'}
essex = {'name': 'Essex', 'csv': 'essex_items.csv', 'date': 'Tue'}
bergen = {'name': 'Bergen', 'csv': 'bergen_items.csv', 'date': 'Fri'}
hunterdon = {'name': 'Hunterdon', 'csv': 'hunterdon_items.csv', 'date': 'Wed'}
union = {'name': 'Union', 'csv': 'union_items.csv', 'date': 'Wed'}
mercer = {'name': 'Mercer', 'csv': 'mercer_items.csv', 'date': 'Wed'}
middlesex = {'name': 'Middlesex', 'csv': 'middlesex_items.csv', 'date': 'Wed'}
monmouth = {'name': 'Monmouth', 'csv': 'monmouth_items.csv', 'date': 'Mon'}
passaic = {'name': 'Passaic', 'csv': 'passaic_items.csv', 'date': 'Tue'}

COUNTY = [morris, essex, bergen, hunterdon, union, mercer, middlesex, monmouth, passaic]
LENGTH = len(COUNTY)
class simpleapp_tk(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        global var
        var = IntVar()
        for index, item in enumerate(COUNTY):
        	self.b = Radiobutton(self, text=item['name']+'(%s)' % item['date'], variable=var, value=index, command=self.sel)
        	self.b.grid(column=0, row=index, columnspan=2, sticky='W')

        self.hi_there = Button(self, text="Select", command=self.selectscrpy)
        self.hi_there.grid(column=0, row=index+1, columnspan=2, sticky='EW')

        self.text = Text(self, height=10, width=40)
        self.text.grid(column=3,row=0, rowspan=index+1, columnspan=2, sticky='N')

        sys.stdout = self
        self.resizable(True,False)
        self.grid_columnconfigure(0, weight=1)

    def selectscrpy(self):
    	self.button = Button(self, text="Run", fg="red", command=self.runscrapy)
        self.button.grid(column=3, row=LENGTH, columnspan=2, sticky='EW')
    	option = var.get()
        self.entryVariable1 = StringVar()
        self.entry1 = Entry(self, textvariable=self.entryVariable1)
        self.entry1.grid(column=3, row=7, sticky='EW')
        self.entryVariable1.set(u"Enter Old Tab Name Here:")
        self.entryVariable2 = StringVar()
        self.entry2 = Entry(self, textvariable=self.entryVariable2)
        self.entry2.grid(column=3, row=8, sticky='EW')
        self.entryVariable2.set(u"Download pdf? (Y/N)")
        if option == 5 or option == 3:
        	self.entry2.configure(state='normal')
        else:
        	self.entry2.configure(state='disabled')


    def sel(self):
        self.text.delete('1.0', "end")
        option = var.get()
        selection = "You selected the " + str(COUNTY[option]['name']) + " county.\n"
        self.text.insert(INSERT, selection)

        if option == 3:
            self.text.insert(INSERT, "Hunterdon county is using .pdf\n")
        elif option == 5:
            self.text.insert(INSERT, "Mercer county is using .pdf\nPlease follow: \n")
            self.text.insert(INSERT, "Step 1: Download sheriff_foreclosuresales_list.pdf from http://nj.gov/counties/mercer/pdfs/sheriff_foreclosuresales_list.pdf\n")
            self.text.insert(INSERT, "Step 2: Open http://www.pdftoexcel.com/\n")
            self.text.insert(INSERT, "Step 3: Upload sheriff_foreclosuresales_list.pdf and download .xlsx\n")
            self.text.insert(INSERT, "Step 4: Save as sheriff_foreclosuresales_list.xlsx in ScrapyCounty_windows folder\n")


    def write(self, txt):
        self.text.insert(END, str(txt))

    def runscrapy(self):
        option = var.get()
        name = self.entryVariable1.get()

        if option == 0:
            scrapycounty.morris(0, name)
        elif option == 5:
            if self.entryVariable2.get().upper() == 'Y':
                hunterdon_save.hunterdon_save()
            item_write.item_write(5, name)
        elif option == 1:
            scrapycounty.essex(1, name)
        elif option == 2:
            scrapycounty.bergen(2, name)
        elif option == 3:
            if self.entryVariable2.get().upper() == 'Y':
                mercer_convert()
                item_write.item_write(3, name)
        elif option == 6:
            scrapycounty.middlesex(6, name)
        elif option == 4:
            scrapycounty.union(4, name)
        elif option == 7:
            scrapycounty.monmouth(7, name)
        elif option == 8:
            scrapycounty.passaic(8, name)
        else:
            print "NOT FOUND! "


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Scrapy County')
    app.mainloop()