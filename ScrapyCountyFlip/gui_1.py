#coding:utf-8  
from Tkinter import *
import time
import threading
import hunterdon_save
from manual_mode import *
import normal_mode
from ScrolledText import ScrolledText

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
UNIONFRONT = ('Arial', 12, 'bold')
class simpleapp_tk(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        # Menu buttons -- global mode [0:normal 1:manual 2:check 3:help]
        MODES = ['Normal', 'Manual', 'Check', 'Help']
        global mode
        mode = IntVar()
        for index, var in enumerate(MODES):
            b = Radiobutton(self, text=var,
                            variable=mode, value=index,
                            font=UNIONFRONT, command=self.switch_mode,
                            indicatoron=0, width=18)
            b.grid(row=0, column=index, sticky='W')
            if index == 0:
            	b.select()
            elif index == 2:
                b.configure(state='disabled')

    	# text message
		global text
		text = ScrolledText(self, height=15, width=75)
		text.grid(column=1, row=1, rowspan=7, columnspan=3, sticky='W')

    	# Select County -- global countyname[0-8]
		global countyname
		countyname = IntVar()
        self.buttons = []
        for index, item in enumerate(COUNTY):
            b = Radiobutton(self, text=item['name']+'(%s)' % item['date'], 
            					 font=UNIONFRONT, command=self.selection_acive,
            					 variable=countyname, value=index, 
            					 height=1, width=15, anchor=W)
            b.grid(column=0, row=index+1, sticky='W')
            self.buttons.append(b)

		# Button1 -- select
        self.sel = Button(self, text="Select", width=15, 
        				  font=UNIONFRONT,command=self.selectscrpy)
        self.sel.grid(column=0, row=LENGTH+2, columnspan=2, sticky='W')

        # Button2 -- run
        self.run = Button(self, text="Run", fg="red", 
        			       font=UNIONFRONT, state='disabled')
        self.run.grid(column=3, row=LENGTH+2, sticky='EW')

        global old_name_vairable, new_name_variable, string_variable
        old_name_vairable = StringVar()
        new_name_variable = StringVar()
        string_variable = StringVar()

        self.lable1 = Label(self, text=u"Input tab name: ", font=UNIONFRONT, anchor=W)
        self.lable1.grid(column=1, row=8, sticky='EW')
        self.lable2 = Label(self, text=u"Download PDF? (Y/N)", font=UNIONFRONT, anchor=W)
        self.lable2.grid(column=1, row=9, sticky='EW')
        self.entry1 = Entry(self, textvariable=old_name_vairable)
        self.entry1.grid(column=2, row=8, sticky='EW')
        self.entry2 = Entry(self, textvariable=string_variable)
        self.entry2.grid(column=2, row=9, sticky='EW')
        self.entry3 = Entry(self, textvariable=new_name_variable)
        self.entry3.configure(state='disabled')
        self.entry3.grid(column=3, row=8, sticky='EW')

        sys.stdout = self
        self.resizable(False, False)

    # Scroll Text
    def write(self, txt):
        text.insert(END, str(txt))
        text.see(END)

    # SELECT radiobuttons callback
    def selection_acive(self):
    	self.run.configure(state='disabled')
        text.delete('1.0', "end")
        option = countyname.get()
        if option == 3:
            text.insert(INSERT, "Hunterdon county is using .pdf\n")
        elif option == 5:
            text.insert(INSERT, "Mercer county is using .pdf\nPlease follow: \n")
            text.insert(INSERT, "Step 1: Download sheriff_foreclosuresales_list.pdf from http://nj.gov/counties/mercer/pdfs/sheriff_foreclosuresales_list.pdf\n")
            text.insert(INSERT, "Step 2: Open http://www.pdftoexcel.com/\n")
            text.insert(INSERT, "Step 3: Upload sheriff_foreclosuresales_list.pdf and download .xlsx\n")
            text.insert(INSERT, "Step 4: Save as sheriff_foreclosuresales_list.xlsx in ScrapyCounty_windows folder\n")

    # Select button callback
    def selectscrpy(self):
    	self.run.configure(state='normal', command=run_scrapy)

    	option = countyname.get()
        selection = "You've selected the " + str(COUNTY[option]['name']) + " county.\n"
        text.insert(INSERT, selection)

    	option = countyname.get()
        mode_option = mode.get()
        if mode_option == 0:
            if option == 5 or option == 3:
            	self.entry2.configure(state='normal')
            else:
            	self.entry2.configure(state='disabled')

    # Mode Switch radiobutton callback
    def switch_mode(self):
        mode_option = mode.get()
        # manual mode
        if mode_option == 1:
            old_name_vairable.set("Old tab name here: ")
            new_name_variable.set("New tab name here: ")
            self.entry3.configure(state='normal')
            self.lable2.configure(text=u'Input start row: ')
            self.buttons[3].configure(state='disabled')
            self.buttons[5].configure(state='disabled')
        # normal mode
        elif mode_option == 0:
            old_name_vairable.set("")
            new_name_variable.set("")
            self.entry3.configure(state='disabled')
            self.lable2.configure(text=u'Download PDF? (Y/N)')
            self.buttons[3].configure(state='normal')
            self.buttons[5].configure(state='normal')

# Run backend scrapy
def run_scrapy():
    mode_option = mode.get()
    if mode_option == 0:
    	th = threading.Thread(target=normal)
    	th.setDaemon(True)
    	th.start()
    elif mode_option == 1:
        th = threading.Thread(target=manual)
        th.setDaemon(True)
        th.start()

def normal():
    time.sleep(0.5)
    number = countyname.get()
    sel = string_variable.get()
    name = old_name_vairable.get()
    if number == 3:
        if sel == "Y":
            hunterdon_save.hunterdon_save()
        else:
            print "No new file will be downloaded. Make sure sale.pdf is the newest."
        normal_mode.normal_mode(number, name)
    elif number == 5:
        if sel == "Y":
            hunterdon_save.hunterdon_save()
            normal_mode.normal_mode(number, name)
        else:
            print "Please read above."
    else:
        print "normal"
        normal_mode.normal_mode(number, name)
    #scrapycounty.bergen(county, tab_name)
    #print "normal mode run"



def manual():
    time.sleep(0.5)
    county = countyname.get()
    old_tab_name = old_name_vairable.get()
    new_tab_name = new_name_variable.get()
    startrow = string_variable.get()
    print "%s: %s and %s start with %s" % (county, old_tab_name, new_tab_name, startrow)
    manual_mode(county, old_tab_name, new_tab_name, int(startrow))
    #print "manual mode run"

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Scrapy County')
    app.mainloop()