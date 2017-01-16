#coding:utf-8  
from Tkinter import *
import time
import threading
import scrapycounty
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
    	mode = 0
    	for index, var in enumerate(MODES):
    		b = Radiobutton(self, text=var,
		                    variable=mode, value=index, 
		                    font=UNIONFRONT,
		                    indicatoron=0, width=18)
    		b.grid(row=0, column=index, sticky='W')
    		if index == 0:
    			b.select()

    	# text message
		global text
		text = ScrolledText(self, height=15, width=75)
		text.grid(column=1,row=1, rowspan=7, columnspan=3, sticky='W')

    	# Select County -- global countyname[0-8]
		global countyname
		countyname = IntVar()
		for index, item in enumerate(COUNTY):
			self.b = Radiobutton(self, text=item['name']+'(%s)' % item['date'], 
								 font=UNIONFRONT, command=self.selection_acive,
								 variable=countyname, value=index, 
								 height=1, width=15, anchor=W)
			self.b.grid(column=0, row=index+1, sticky='W')

		# Button1 -- select
		self.sel = Button(self, text="Select", width=15, 
						  font=UNIONFRONT,command=self.selectscrpy)
		self.sel.grid(column=0, row=LENGTH+2, columnspan=2, sticky='W')

        # Button2 -- run
        self.run = Button(self, text="Run", fg="red", 
        			       font=UNIONFRONT, state='disabled')
        self.run.grid(column=3, row=LENGTH+2, sticky='EW')

        sys.stdout = self
        self.resizable(True,False)

    def write(self, txt):
        text.insert(END, str(txt))

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

    def selectscrpy(self):
    	self.run.configure(state='normal',command=normal_mode)

    	option = countyname.get()
        selection = "You selected the " + str(COUNTY[option]['name']) + " county.\n"
        text.insert(INSERT, selection)

    	self.lable1 = Label(self, text=u"Enter Tab Name Here:", font=UNIONFRONT)
    	self.lable1.grid(column=1, row=8, sticky='EW')
    	self.lable2 = Label(self, text=u"Download pdf? (Y/N)", font=UNIONFRONT)
    	self.lable2.grid(column=1, row=9, sticky='EW')

    	option = countyname.get()
        self.entryVariable1 = StringVar()
        self.entry1 = Entry(self, textvariable=self.entryVariable1)
        self.entry1.grid(column=2, row=8, sticky='EW')
        #self.entryVariable1.set(u"Enter Old Tab Name Here:")
        self.entryVariable2 = StringVar()
        self.entry2 = Entry(self, textvariable=self.entryVariable2)
        self.entry2.grid(column=2, row=9, sticky='EW')
        #self.entryVariable2.set(u"Download pdf? (Y/N)")
        if option == 5 or option == 3:
        	self.entry2.configure(state='normal')
        else:
        	self.entry2.configure(state='disabled')

def normal_mode():
	th = threading.Thread(target=count)  
	th.setDaemon(True)
	th.start()

def count():
	time.sleep(0.5)
	scrapycounty.morris(0, '01/09/2017')


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Scrapy County')
    app.mainloop()