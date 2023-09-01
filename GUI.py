import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from Game import Game
from Game import ItemNotPresentError
from Player import Player
import logging

class App(tk.Frame):
    # Creates a Frame for the application
    # and populates the GUI ...
    def __init__(self, win):
        super().__init__(master=win)
    
        # Create the game model object ... 
        self.game = Game()
        self.createMenuItems()
        self.createGameParts()
        logging.basicConfig(filename='demo.log',filemode='w',level=logging.DEBUG)

        

    # win has 1 row and 1 columns ...
        win.rowconfigure(0, weight=1)
        win.columnconfigure(0, weight=1)
        self.grid(row=0, column=0)
        messagebox.showinfo("Welcome","You were welcomed by the master with a cup of tea.\nYou wake up alone in the storeroom of a house.\nYou need to escape from the house.")

    def createMenuItems(self):
        """
        Create menu items, including common menubar and cascading menubar.
        
        """
        # Add some menu options to the window ...
        menubar = tk.Menu()
        menubar.add_command(label="Quit", command=self.master.destroy)
        menubar.add_command(label="About", command=self.showAbout)
        menubar.add_command(label="Help", command=self.showHelp)
        menubar.add_command(label="Player", command=self.showPlayer)

        ActionMenu = tk.Menu()
        menubar.add_cascade(label="Action", menu=ActionMenu)
        ActionMenu.add_command(label="Cure",command=self.doCureCommand)
        ActionMenu.add_command(label="Shower",command=self.doShowerCommand)
        ActionMenu.add_command(label="Unlock",command=self.doUnlockCommand)
        ActionMenu.add_command(label="Feed",command=self.doFeedCommand)
        ActionMenu.add_command(label="Dress",command=self.doDressCommand)

        self.master.config(menu=menubar)

    def showAbout(self):
        """
        Open a message box to show details about the application.

        """
        messagebox.showinfo("About","Escape from House Game\nEnjoy!")
        logging.debug("About")
   
    def showHelp(self):
        """Open a message box to show help message."""
        messagebox.showinfo("Help","You feel uncomfortable and start to walk around.")
        logging.debug("Help")
   
    
    def createGameParts(self):
        # Create all the GUI frame widgets and layout
        # Using a grid manager ...
        self.columnconfigure(0, pad=50)
        self.columnconfigure(1, pad=50)
        self.columnconfigure(2, pad=50)
        self.rowconfigure(0, pad=40)
        self.rowconfigure(1, pad=40)
        self.rowconfigure(2, pad=40)
        # Establish labels ...
        self.label1 = tk.Label(self, bg='chocolate', fg='white', text=self.game.currentRoom.getLongDescription())
        self.label1.grid(row=0,column=1,sticky='n')
        self.label2 = tk.Label(self, bg='chocolate', fg='white', text="item:\nclue:")
        self.label2.grid(row=1,columnspan=2)
        
        # Set room visual ...
        photo = Image.open('images/storeroom.jpg')
        photo = photo.resize((450,300))
        self.img = ImageTk.PhotoImage(photo)
        self.panel1 = tk.Label(self, image=self.img)
        self.panel1.grid(row=0,column=1,sticky='s')
        
        # Set item visual ...
        whtphoto=Image.open(f'images/white.jpg')
        whtphoto=whtphoto.resize((220,220))
        self.img2 = ImageTk.PhotoImage(whtphoto)
        self.panel2 = tk.Label(self, image=self.img2)
        self.panel2.grid(row=0,column=0)

        # Establish buttons 
        self.bfind=tk.Button(self,text="Find", command=self.doFindCommand)
        self.bfind.grid(row=2,column=1,sticky='w')
        self.btake=tk.Button(self,text="Take", command=self.doTakeCommand)
        self.btake.grid(row=2,column=1,sticky='e')

        # Add an OptionsMenu widget (direction)
        options = ['east','west','south','north','northwest','southwest','down','up','downstairs','upstairs']    # List with all options
        self.v = tk.StringVar(self)
        self.v.set(options[0])  # default value
        self.v.trace("w",self.doGoCommand)
        # trace() detects when a variable value has changed and calls a callback method accordingly
        self.w = tk.OptionMenu(self,self.v,*options)
        # *options unpacks the options list ...
        self.w.grid(row=2,column=1)
        
    def doGoCommand(self,*args):
        """
        Use doGoCommand method in Game Module.
        :param: *args is used here as the callback is providing arguments that we don't need
        :return: None
        """
        secondword = self.v.get()
        self.game.doGoCommand(secondword)
        self.label1.configure(text=self.game.currentRoom.getLongDescription())
        chngphoto=Image.open(f'images/{self.game.currentRoom.description}.jpg')
        chngphoto=chngphoto.resize((450,300))
        self.img = ImageTk.PhotoImage(chngphoto)
        self.panel1.configure(image=self.img)
        logging.debug(f' {secondword}')
    
    def doFindCommand(self):
        """Use doGoCommand method in Game Module.
        :return: None
        """
        self.game.doFindCommand()
        self.label2.configure(text=f'item: {self.game.currentRoom.item}\nclue: {self.game.currentRoom.clue}')
        if self.game.currentRoom.item:   
            itemphoto = Image.open(f'images/{self.game.currentRoom.item}.jpg')
            itemphoto = itemphoto.resize((220,220))
            self.img3 = ImageTk.PhotoImage(itemphoto)
            self.panel2.configure(image=self.img3)
        logging.debug(" Find")

    def doTakeCommand(self):
        """Use doTakeCommand method in Game Module. Implement exception handlers.
        :return: None
        """
        try:
            if self.game.currentRoom.item and self.game.currentRoom.item[0]!='coat':
                logging.debug(f' Take {self.game.currentRoom.item}')
                self.game.doTakeCommand(self.game.currentRoom.item[0])
                self.panel2.configure(image=self.img2)
                self.label2.configure(text=f'item:\nclue:') 
            else:
                raise ItemNotPresentError("No item")
        except ItemNotPresentError as e:
                logging.exception(e)
 
    def doCureCommand(self):   
        """Use doCureCommand method in Game Module.
        :return: None
        """
        self.game.doCureCommand()
        logging.debug(" Cure")
    
    def doShowerCommand(self):
        """Use doShowerCommand method in Game Module.
        :return: None
        """
        self.game.doShowerCommand()
        logging.debug(" Shower")
    
    def doUnlockCommand(self):
        """Use doUnlockCommand method in Game Module.
        :return: None
        """
        self.game.doUnlockCommand()
        if self.game.currentRoom==self.game.locker_room:
            chngphoto=Image.open(f'images/locker room.jpg')
            chngphoto=chngphoto.resize((450,300))
            self.img = ImageTk.PhotoImage(chngphoto)
            self.panel1.configure(image=self.img)
            self.label1.configure(text=self.game.currentRoom.getLongDescription())
        logging.debug(" Unlock")    
   
    def doFeedCommand(self):
        """Use doFeedCommand method in Game Module.
        :return: None
        """
        self.game.doFeedCommand()
        self.label1.configure(text=self.game.currentRoom.getLongDescription())
        logging.debug(" Feed")
    
    def doDressCommand(self):
        """Use doDressCommand method in Game Module.
        :return: None
        """
        self.game.doDressCommand()
        logging.debug(" Dress")
        self.panel2.configure(image=self.img2)
        self.label2.configure(text=f'item:\nclue:')
    
    def showPlayer(self):
        """Show the details of Player
        :return: None
        """
        messagebox.showinfo("Player",f'name: {self.game.player.name}\nclothes: {self.game.player.clothes}\nbackpack: {self.game.player.backpack}\nhealth: {self.game.player.health}\nsmell: {self.game.player.smell}')  
        logging.debug(" Player")                                                                                                              

def main():

    win = tk.Tk()                   # Create a window
    win.title("Escape from House Game")  # Set window title
    win.geometry("850x600")         # Set window size
    win.resizable(False, True)     # Both x and y dimensions ...

    # Create the GUI as a Frame
    # and attach it to the window ...
    myApp = App(win)

    # Call the GUI mainloop ...
    win.mainloop()

if __name__ == "__main__":
    main()
