from Tkinter import *
import tkMessageBox
from ttk import *
from PIL import Image
import oceanOp, digimeshOp
from binascii import unhexlify, hexlify
import csv
from time import sleep


class Gui(Frame):

    """Create a GUI with all buttons and labels with their specific functions"""
    def __init__(self, parent, spectra, comunic):
        Frame.__init__(self, parent)
        self.parent = parent

        self.comunic = comunic
        self.spectra = spectra

        self.menuGen = Menu(self.parent)

        self.menuBar = Menu(self.menuGen, tearoff=0)
        self.menuBar.add_command(label="Reflectance", command=self.set_refl)
        self.menuBar.add_command(label="Fluorescence", command=self.set_fluo)
        self.menuBar.add_separator()
        self.menuBar.add_command(label="Exit", command=self.close_gui)
        
        
        self.menuGen.add_cascade(label="Calibration Menu", menu=self.menuBar)
        self.parent.config(menu=self.menuGen)


        self.parent.title("Summer Project")


        
        
        self.pack(fill=BOTH, expand=1)
        self.style = Style()
        self.style.theme_use("default")
        
        self.frame1 = Frame(self, height=100)
        self.frame1.pack(side=TOP)
        
        self.label1 = Label(self.frame1, text="UQ Wireless Spectrophotometer", font='Purisa 16 bold italic')
        self.label1.pack(side=TOP, padx=5, pady=5)


        parent.protocol("WM_DELETE_WINDOW", self.close_gui)
        

        self.frame2 = Frame(self, relief=RAISED, borderwidth=2, height=650, width=350)
        self.frame2.pack(side=LEFT, padx=5, pady=5)

        self.label2 = Label(self.frame2, text="Photometer Calibration", font='Purisa 16 italic')
        self.label2.pack(side=TOP, pady=15, padx=40)

        

        

        self.frame3 = Frame(self, relief=RAISED, borderwidth=2, height=650, width=350)
        self.frame3.pack(side=RIGHT, padx=5, pady=5, fill=X)

        self.label3 = Label(self.frame3, text="Digimesh Settings", font='Purisa 16 italic')
        self.label3.pack(side=TOP, pady=15, padx=40)

        self.frameChan = Frame(self.frame3)
        self.frameChan.pack(fill=X)

        self.label4 = Label(self.frameChan, text="Channel:", width=8)
        self.label4.pack(side=LEFT, padx=10, pady=10)

        self.entry1 = Entry(self.frameChan)
        self.entry1.pack(fill=X, padx=5, expand=True)
        self.entry1.insert(END, hexlify(comunic.chan_init))

        self.frameID = Frame(self.frame3)
        self.frameID.pack(fill=X)

        self.label5 = Label(self.frameID, text="PAN ID:", width=8)
        self.label5.pack(side=LEFT, padx=10, pady=10)

        self.entry2 = Entry(self.frameID)
        self.entry2.pack(fill=X, padx=5, expand=True)
        self.entry2.insert(END, hexlify(comunic.pan_init))

        self.frameMAC = Frame(self.frame3)
        self.frameMAC.pack(fill=X)

        self.label6 = Label(self.frameMAC, text="MAC ADD:", width=8)
        self.label6.pack(side=LEFT, padx=10, pady=10)

        self.entry3 = Entry(self.frameMAC, width=14)
        self.entry3.insert(END, hexlify(comunic.addr_init_high))
        self.entry3.pack(side=LEFT, padx=5)

        self.entry4 = Entry(self.frameMAC, width=14)
        self.entry4.insert(END, hexlify(comunic.addr_init_low))
        self.entry4.pack(side=RIGHT, padx=5)


        self.frameAcc = Frame(self.frame3)
        self.frameAcc.pack(fill=X)

        self.saveButton = Button(self.frameAcc, text="Save", command=self.save)
        self.saveButton.pack(side=LEFT, padx=10, pady=10)

        self.testButton = Button(self.frameAcc, text="Test", command=self.testing)
        self.testButton.pack(side=LEFT, padx=24, pady=10)

        self.clearButton = Button(self.frameAcc, text="clear", command=self.clear)
        self.clearButton.pack(side=RIGHT, padx=10, pady=10)

        self.frameRange = Frame(self.frame2, width=50)
        self.entryMin = Entry(self.frameRange, width=10)
        self.entryMin.insert(END, "0")
        self.entryMin.pack(side=LEFT, padx=10, pady=5)

        self.labelTo = Label(self.frameRange, text="TO")
        self.labelTo.pack(side=LEFT, padx=68)

        self.entryMax = Entry(self.frameRange, width=8)
        self.entryMax.insert(END, "0")
        self.entryMax.pack(side=RIGHT, padx=10, pady=5)

        self.frameRange.pack(fill=X)

        self.frame21 = Frame(self.frame2)
        self.frame21.pack(fill=X)

        self.maxButton = Button(self.frame21, text="Min calibrate", command=spectra.calibrate_min)
        self.maxButton.pack(side=LEFT, padx=10, pady=10)

        
        self.graphButton = Button(self.frame21, text="Graph", command=self.write_refl)
        self.graphButton.pack(side=LEFT, padx=25, pady=10)
        

        self.minButton = Button(self.frame21, text="Max calibrate", command=spectra.calibrate_max)
        self.minButton.pack(side=RIGHT, padx=10, pady=10)


        
        self.frame22 = Frame(self.frame2)
        self.graphButton = Button(self.frame22, text="Graph", command=self.write_fluo)
        self.graphButton.pack(side=LEFT, padx=25, pady=10)
        

        self.minButton = Button(self.frame22, text="Calibrate", command=spectra.calibrate_max)
        self.minButton.pack(side=RIGHT, padx=10, pady=10)


    """Create a message box when we try to close the program, if the program is closed then also close the serial
    communicatioin ports"""
    def close_gui(self):
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            self.comunic.close()
            self.parent.destroy()
        

    """Clear entry boxes for channel, address, panID and MAC address"""
    def clear(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        print("holi")

    """Read all the entry boxes and save their specific values into XBEE PRO, those values are stored in the internal
    memory of the XBEE PRO, for instance is safe to modify values and later disconnect the XBEE module"""
    def save(self):
        kwargs = {"CH": self.entry1.get(), "ID": self.entry2.get(), "DH": self.entry3.get(), "DL": self.entry4.get()}
        self.comunic.gui_save(**kwargs)


    """Send two types of messages to test:
    1.- The message formatted to the server, so we test communication with the main server.
    2.- The word (testing...!!!) in order to check basic communication with another XBEE module connected to the app XCTU in a computer.
    NOTE: if message 1 is received on the main server (this message should be received HSS: 1.2), then the XBEE module was correctly set up
    """
    def testing(self):
        #self.comunic.send_data("testing...!!!")
        count = 0
        kwargs1 = {"HSS": "1.2"}
        while (count < 5):
            self._send_sensor(**kwargs1)
            count = count + 1
            sleep(1)

        
    """Show parameters for fluorescence calibration"""
    def set_fluo(self):
        self.frame21.pack_forget()
        self.frame22.pack()

    """Show parameters for reflectance calibration"""
    def set_refl(self):
        self.frame22.pack_forget()
        self.frame21.pack()


    """Write all the values read (that are between the range given in the program) to a csv file""" 
    def write_csv(self):
        count = 0
   
        with open('readSTS4.csv', 'w') as csvfile:
            #Give name to the columns for the csv file
            fieldnames = ['wavelengths', 'amplitude']

            #Specify that we want this file to be opened by excel.
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel') 
            writer.writeheader()
            while count < 1024:
                if(float(self.spectra.wavelengths[count]) > float(self.entryMin.get()) and float(self.spectra.wavelengths[count]) < float(self.entryMax.get()) and float(self.spectra.percentage_wave[count]) > 0):
                    #write values to their specific column.
                    writer.writerow({'wavelengths': self.spectra.wavelengths[count],
                                 'amplitude': self.spectra.percentage_wave[count]})
                count = count + 1
        csvfile.close()

    """Read values for fluorescence and then write those values to a csv file"""
    def write_fluo(self):
        self.write_csv()
        self.spectra.read_samples_fluo()

    """Read values for reflectance and then write those values to a csv file"""
    def write_refl(self):
        self.write_csv()
        self.spectra.read_samples()

    """Send testing message in order to check if the format chosen for the message is the correct when sending to the main server"""
    def _send_sensor(self, **kwargs):
        data = "<=>"
        id_wasp = "000000001"
        data = data + unhexlify("800" + str(len(kwargs))) + "#" + id_wasp + "#" + "HSS_01" + "#" + "214" + "#"
        print data
        for key, value in kwargs.iteritems():
            data = data + str(key) + ":" + str(value) + "#"

        self.comunic.send_data(data)
        return data


                

        

def main():
    root = Tk()
    spectra = oceanOp.STS()
    comunic = digimeshOp.XBEE_PRO()
    root.geometry("750x300+300+300")
    app = Gui(root, spectra, comunic)
    root.mainloop()


if __name__ == '__main__':
    main()
