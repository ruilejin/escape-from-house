from Room import Room
from Player import Player
from tkinter import messagebox
import logging
"""
    This class is the main class of the "Escape from House" application. 
        
    To play this game, create an instance of this class and call the "play"
    method.

    This main class creates and initialises all the others: it creates all
    rooms, creates the parser and starts the game.  It also evaluates and
    executes the commands that the parser returns.
"""

class ItemNotPresentError(Exception):
    """
               Define an exception for ItemNotPresentError
        :param Exception: item not in the current room
        :return: None
    """
    def __init__(self,message):
        messagebox.showinfo("warning",message)

class Game:

    def __init__(self):
        """
        Initialises the game
        """
        self.createRooms()
        self.player = Player('you', ['one piece'])
        self.currentRoom = self.storeroom

    def createRooms(self):
        """
            Sets up all room assets
        :return: None
        """

        # third floor
        self.study = Room("study", clue='you need green potion, peacock feather, yellow flower to make an antidote',item=['key'])
        self.storeroom = Room("storeroom", item=['peacock_feather'])
        self.pharmacy_room = Room("pharmacy room", item=['green_potion'])
        self.garden = Room("garden", item=['yellow_flower'])
        self.fireplace2 = Room("fireplace2", clue=['it\'s connected with kitchen in 1st floor'])

        # second floor
        self.bedroom = Room("bedroom")
        self.living_room2 = Room("living room 2")
        self.bathroom = Room("bathroom", clue=['to eliminate the smell you can shower '])
        self.locker_room = Room("locker room", item=['coat'],clue=['you can pretend to be the master by dressing the coat'])
        self.outside_of_locker_room = Room("outside of locker room")

        # first floor
        self.living_room1 = Room("living room 1", clue=['a photo of dog biting sausage'])
        self.kitchen = Room("kitchen", item=['sausages'])
        self.lobby = Room("lobby", clue=['there is a dog outside'])
        self.fireplace1 = Room("fireplace1", clue=['it\'s connected with pharmacy room in 2nd floor'])

        # outside
        self.dog = Room("dog")
        self.outside = Room('outside')

        # relationships of third-floor rooms
        self.storeroom.setExit("east", self.garden)
        self.storeroom.setExit("south", self.pharmacy_room)
        self.garden.setExit("west", self.storeroom)
        self.garden.setExit("south", self.study)
        self.study.setExit("north", self.garden)
        self.study.setExit("west", self.pharmacy_room)
        self.pharmacy_room.setExit("east", self.study)
        self.pharmacy_room.setExit("north", self.storeroom)
        self.pharmacy_room.setExit("south", self.fireplace2)
        self.fireplace2.setExit("north", self.pharmacy_room)

        # relationships of second-floor rooms
        self.living_room2.setExit("west", self.bedroom)
        self.living_room2.setExit("north", self.bathroom)
        self.bathroom.setExit("south", self.living_room2)
        self.bathroom.setExit("west", self.locker_room)
        self.locker_room.setExit("south", self.bedroom)
        self.locker_room.setExit("east", self.outside_of_locker_room)
        self.outside_of_locker_room.setExit("east",self.bathroom)

        # relationships of first-floor rooms
        self.living_room1.setExit("northwest", self.lobby)
        self.living_room1.setExit("southwest", self.kitchen)
        self.kitchen.setExit("east", self.living_room1)
        self.kitchen.setExit("south", self.fireplace1)
        self.fireplace1.setExit("north",self.kitchen)
        self.lobby.setExit("east", self.living_room1)
        self.lobby.setExit("west", self.dog)
        self.dog.setExit("east", self.lobby)
        self.outside.setExit("east",self.dog)


        # between fireplaces
        self.fireplace2.setExit("down", self.fireplace1)
        self.fireplace1.setExit("up", self.fireplace2)

        # ends of stairs
        self.study.setExit("downstairs", self.bedroom)
        self.bedroom.setExit("upstairs", self.study)
        self.living_room2.setExit("downstairs", self.living_room1)
        self.living_room1.setExit("upstairs", self.living_room2)

    
    def doGoCommand(self, secondWord,*args):
        """
            Performs the GO command
        :param secondWord，*args: the direction the player wishes to travel in,*args is used here as the callback is providing arguments that we don't need.
        :return: None
        """
        nextRoom = self.currentRoom.getExit(secondWord)
        
        if nextRoom == None:
            messagebox.showinfo("warning","no door")
        #step into bedroom but caught by master and sent back to storeroom
        elif nextRoom == self.bedroom:
            messagebox.showinfo("warning","You're caught by master in the bedroom and sent back.")
            self.currentRoom = self.storeroom
        #step into locker room
        elif nextRoom == self.locker_room:
            messagebox.showinfo("Info","It is locked.")
            if 'key' not in self.player.backpack:
                messagebox.showinfo("Info","You don't have the key.")
            else:
                messagebox.showinfo("Info","Use key to unlock.")
            #didn't unlock so still not in the locker room
            self.currentRoom = self.outside_of_locker_room
        else:
            self.currentRoom = nextRoom
            if nextRoom == self.dog:
                if 'coat' not in self.player.clothes \
                        or self.player.smell == 'smells':
                    messagebox.showinfo("Info","Dog barks because you are stranger. ")
                else:
                    messagebox.showinfo("Info","Dog thinks you are master. ")
            if nextRoom == self.outside:
                messagebox.showinfo("Info","Congratulations! You are free!")
    
    def doFindCommand(self):
        """
               Perform the FIND command.Fetch clues and items.
        :return: None
        """
        self.currentRoom.getFindDescription()

    def doTakeCommand(self, secondWord):
        """
             Performs the TAKE command
        :param: secondWord: the item the player wishes to take into backpack
        :return: None
        """
        try:
          if self.currentRoom.item:
            messagebox.showinfo("Info", f'{self.currentRoom.item} is in your backpack now.')
            self.player.takeItem(secondWord)
            self.currentRoom.item.remove(secondWord)  
        except ItemNotPresentError:
            
          pass

    def doCureCommand(self):
        """
             Performs the CURE command.
        :return: None
        """
        if 'yellow_flower' not in self.player.backpack\
                or 'green_potion' not in self.player.backpack\
                or 'peacock_feather' not in self.player.backpack:
            messagebox.showinfo("Info","There's no enough ingredients.")
        elif self.currentRoom != self.pharmacy_room:
            messagebox.showinfo("Info","You are not at a right place!")
        else:
            self.player.health = 'healthy'
            self.player.backpack.remove('yellow_flower')
            self.player.backpack.remove('green_potion')
            self.player.backpack.remove('peacock_feather')
            messagebox.showinfo("Info","You are healthy now!")
    
    def doShowerCommand(self):
        """
             Perform the SHOWER command.
        :return: None
        """
        if self.currentRoom != self.bathroom:
            messagebox.showinfo("Info","You are not at a right place!")
        else:
            self.player.smell = 'no smells'
            messagebox.showinfo("Info","You have no smells now.")

    def doUnlockCommand(self):
        """
            Perform the UNLOCK command.
        :return: None
        """
        if self.currentRoom!=self.outside_of_locker_room:
            messagebox.showinfo("Info","No room needs to be unlocked.")
        elif 'key' not in self.player.backpack:
            messagebox.showinfo("Info","You don't have the key.")
        else:
            self.currentRoom = self.locker_room

    def doDressCommand(self):
        """
             Performs the DRESS command
        :param secondWord: the item the player wishes to take into backpack
        :return: None
        """
        if self.currentRoom!=self.locker_room or self.locker_room.item == False:
            messagebox.showinfo("Info","Nothing can dress.")
            return
        elif self.player.smell == 'smells':
            messagebox.showinfo("Info","You haven't take shower.")
        else:
            self.player.dressUp('coat')
            self.locker_room.item.remove('coat')
            messagebox.showinfo("Info","Dressed")
    
    def doFeedCommand(self):
        """
             Perform the FEED command.
        :return: None
        """
        if self.currentRoom != self.dog:
            messagebox.showinfo("Info","There is no object to feed.")
        else:
            if self.currentRoom == self.dog \
                    and 'coat' not in self.player.clothes \
                    or self.player.smell == 'smells':
                messagebox.showinfo("Info","Dog barks because you are stranger. ")

            elif 'sausages' not in self.player.backpack:
                messagebox.showinfo("Info","Don't have sausages.")

            else:
                messagebox.showinfo("Info","You can pass the dog now.")
                if self.player.health == 'poisoned':
                   messagebox.showinfo("Info","You are too sick to escape.")
                else:
                    self.dog.setExit("west", self.outside)





def main():
    game = Game()

if __name__ == "__main__":
    main()