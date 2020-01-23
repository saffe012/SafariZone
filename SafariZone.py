#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''This program is a simplified version of the Safari Zone minigame found in the
popular Pokemon video games.
'''

import tkinter as tk
import random
import sys

__author__ = "Matt Saffert"
__copyright__ = "Copyright 2020, Matt Saffert"
__credits__ = ["Matt Saffert"]
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "Matt Saffert"
__email__ = "mattsaffert@gmail.com"
__status__ = "Production"


class Pokemon:
    '''
    A class used to represent a Pokemon

    ...

    Attributes
    ----------
    name : str
        The name of the Pokemon
    number : int
        The id number of the Pokemon
    ind_rate : str
        Used in calculating the catch rate of a Pokemon
    catch_rate : float
        The percent chance of catching a given Pokemon
    speed : str
        Used in calculating whether a Pokemon will run away or not
    '''

    def __init__(self, name, number, ind_rate, catch_rate, speed):
        '''
        Parameters
        ----------
        name : str
            The name of the Pokemon
        number : int
            The id number of the Pokemon
        ind_rate : str
            Used in calculating the catch rate of a Pokemon
        catch_rate : float
            The percent chance of catching a given Pokemon
        speed : str
            Used in calculating whether a Pokemon will run away or not
        '''

        self.name = name
        self.number = number
        self.ind_rate = ind_rate
        self.catch_rate = catch_rate
        self.speed = int(speed)


class SafariSimulator(tk.Frame):
    '''
    A class used to represent the Safari Zone Simulator

    ...

    Attributes
    ----------
    master : tkinter.Tk
        An instance of a tkinter GUI (default None)
    poke_list : List[List[str]]
        List of the info about each Pokemon
    safari_balls : int
        Number of safari balls a user has left
    captured_poke : List[str]
        List of the names of Pokemon that have been caught
    first : bool
        If this is the first Pokemon displayed: True
    runButton : tkinter.Button
        Button used to run away
    messageLabel : tkinter.Label
        Label to display information
    throwButton : tkinter.Button
        Button used to throw ball
    rockButton : tkinter.Button
        Button used to throw rock
    baitButton : tkinter.Button
        Button used to throw bait
    image : tkinter.Label
        Displays image of Pokemon in front of user
    catchRateLabel : tkinter.Label
        Label to display how likely a user is to catch Pokemon
    runRateLabel : tkinter.Label
        Label to display how likely a Pokemon is to flee
    run_prob : float
        How likely a Pokemon is to flee
    angryCount : int
        Anger level of the Pokemon
    eatingCount : int
        Eating level of the Pokemon
    monster : __main__.Pokemon
        The monster currently interacting with the user

    Methods
    -------
    createRunButton(run_description)
        Creates a tkinter Button with a command that gets the next Pokemon
    createMessageLabel(message_label)
        Creates a tkinter Label to display a passed in message
    createPokemonImage(file_name)
        Creates a tkinter Button with a command that gets the next Pokemon
    createWidgets()
        Creates Labels and Buttons that will be displayed on the screen
    dropWidgets()
        Destroys the tkinter Labels and Buttons currently in the tkinter GUI
    nextPokemon()
        Randomly picks a new Pokemon to be displayed on screen
    endAdventure()
        Creates window that displays the end of game message
    throwBall()
        Logic for when the Throw Ball button is pressed by the player
    throwRock()
        Logic for when the Throw Rock button is pressed by the player
    throwBait()
        Logic for when the Throw Bait button is pressed by the player
    '''

    def __init__(self, master=None):
        '''
        Parameters
        ----------
        master : tkinter.Tk
            An instance of a tkinter GUI (default None)
        '''

        #  opens and reads file containing data about each Pokemon
        file = open('data/pokedex.csv', 'r')
        line = file.readline()
        poke_list = []
        while line != '':  # each line represents data for a different Pokemon
            line = file.readline()
            line = line.strip('\n')
            words = line.split(',')
            poke_list.append(words)

        #  set instance variables
        self.poke_list = poke_list
        self.safari_balls = 30
        self.captured_poke = []
        self.first = True

        #  These lines set basic window parameters and title
        tk.Frame.__init__(self, master)
        master.minsize(width=275, height=350)
        master.maxsize(width=275, height=400)
        master.title("Safari Zone Simulator")
        self.pack()

        # call nextPokemon() method here to initialize first random pokemon
        self.nextPokemon()

    def createRunButton(self, run_description):
        '''Creates a tkinter Button with a command that gets the next Pokemon

        Parameters
        ----------
        run_description : str
            String that will be placed on the button
        '''

        self.runButton = tk.Button(self)
        self.runButton["text"] = run_description
        self.runButton["command"] = self.nextPokemon
        self.runButton.pack()

    def createMessageLabel(self, message_label):
        '''Creates a tkinter Label to display a passed in message

        Parameters
        ----------
        message_label : str
            String that will be the text of the Label
        '''

        self.messageLabel = tk.Label(bg="grey", text=message_label)
        self.messageLabel.pack(fill="x", padx=5, pady=5)

    def createPokemonImage(self, file_name):
        '''Creates a tkinter Button with a command that gets the next Pokemon

        Parameters
        ----------
        file_name : str
            Location/name of file where image is stored
        '''

        photo = tk.PhotoImage(file=file_name)
        self.image = tk.Label(image=photo)
        self.image.photo = photo
        self.image.pack()

    def createWidgets(self):
        '''Creates 4 tkinter Labels and 4 tkinter Buttons that will be displayed
        on the screen for the user to read/interact with in order to play the game
        '''

        # Creates a tkinter Button with a command that throws a Pokeball
        self.throwButton = tk.Button(self)
        state2 = "Throw Safari Ball (" + str(self.safari_balls) + " left)"
        self.throwButton["text"] = state2
        self.throwButton["command"] = self.throwBall
        self.throwButton.pack()

        # Creates a tkinter Button with a command that gets the next Pokemon
        self.createRunButton("Run Away")

        # Creates a tkinter Button with a command that throws a rock
        self.rockButton = tk.Button(self)
        self.rockButton["text"] = "Throw Rock"
        self.rockButton["command"] = self.throwRock
        self.rockButton.pack()

        # Creates a tkinter Button with a command that throws bait
        self.baitButton = tk.Button(self)
        self.baitButton["text"] = "Throw Bait"
        self.baitButton["command"] = self.throwBait
        self.baitButton.pack()

        # Creates a tkinter Label to display which Pokemon was encountered
        state = "You encountered a wild " + self.monster.name
        self.createMessageLabel(state)

        # Creates a tkinter Label to display the image of the current Pokemon
        file_name = "media/" + str(self.monster.number) + ".gif"
        self.createPokemonImage(file_name)

        # Creates a tkinter Label to display the odds of catching a Pokemon
        state1 = "Your chance of catching it is " + \
            str(self.monster.catch_rate // 1) + "%!"
        self.catchRateLabel = tk.Label(bg="grey", text=state1)
        self.catchRateLabel.pack(fill="x", padx=5, pady=5)

        # Creates a tkinter Label to display the odds of a Pokemon fleeing
        state2 = "The chances it runs is " + str(self.run_prob // 1) + "%!"
        self.runRateLabel = tk.Label(bg="grey", text=state2)
        self.runRateLabel.pack(fill="x", padx=5, pady=5)

    def dropWidgets(self):
        '''Destroys the tkinter Labels and Buttons currently in the tkinter GUI
        '''

        self.runButton.pack_forget()
        self.throwButton.pack_forget()
        self.messageLabel.pack_forget()
        self.image.pack_forget()
        self.catchRateLabel.pack_forget()
        self.rockButton.pack_forget()
        self.baitButton.pack_forget()
        self.runRateLabel.pack_forget()

    def nextPokemon(self):
        '''Randomly picks a new Pokemon to be displayed on screen, gathers
        all of the attributes associated with that Pokemon, creates a Pokemon instance,
        then creates new onscreen Widgets to represent that Pokemon.
        '''

        # if the Pokemon is the first Pokemon to be displayed there are no widgets to destroy
        if not self.first:
            self.dropWidgets()

        self.first = False

        # gets a random Pokemon's data
        number = random.randint(1, 151)
        info = self.poke_list[number - 1]

        number = info[0]  # id number of pokemon
        name = info[1]  # name of Pokemon
        # calculates the catch rate as a percentage
        catch_rate = ((min((int(info[2]) + 1), 151) / 449.5) * 100)
        speed = info[3]  # speed of Pokemon

        # calculates the flee rate as a percentage
        self.run_prob = ((2 * int(speed)) / 256) * 100
        self.angryCount = 0
        self.eatingCount = 0

        # new Pokemon instance
        self.monster = Pokemon(name, number, info[2], catch_rate, speed)
        print(type(self.monster))

        self.createWidgets()

    def endAdventure(self):
        '''Window that displays the end of game message when the user has used
        all of their Pokeballs. Displays the list of Pokemon they caught during
        the game.
        '''

        self.dropWidgets()

        state1 = "You're all out of balls, hope you had fun!"
        finalLabel = tk.Label(bg="grey", text=state1)
        finalLabel.pack(fill="x", padx=5, pady=5)

        if self.captured_poke == []:  # if no Pokemon were caught
            state2 = "Oops, you caught 0 Pokemon."
        else:  # list all caught Pokemon on screen
            state2 = "You caught " + \
                str(len(self.captured_poke)) + \
                " Pokemon:\n" + self.captured_poke[0]
            for i in range(1, len(self.captured_poke)):
                state2 = state2 + '\n' + self.captured_poke[i]

        # Label listing all caught Pokemon
        finalLabel2 = tk.Label(bg="grey", text=state2)
        finalLabel2.pack(fill="x", padx=5, pady=5)

    def throwBall(self):
        '''Computes the logic and adjustment of stats when the Throw Ball
        button is pressed by the player.
        '''

        # ball was thrown so decrement safari_balls
        self.safari_balls = self.safari_balls - 1

        number = random.randint(0, 100)
        # calculate if Pokemon was caught
        if number <= self.monster.catch_rate:  # Pokemon was caught
            self.captured_poke.append(self.monster.name)
            self.dropWidgets()
            self.createRunButton("Continue")
            state = "You caught a wild " + self.monster.name + "!"
            self.createMessageLabel(state)
            file_name = "media/safari_ball.gif"
            self.createPokemonImage(file_name)
        else:  # failed to catch Pokemon
            self.dropWidgets()
            self.createWidgets()

        if self.safari_balls == 0:  # user ran out of balls. End the game
            self.endAdventure()
            sys.exit()

        # calculates how likely the Pokemon is to flee
        if self.angryCount == 0 and self.eatingCount == 0:
            flee_stat = (self.monster.speed % 256) * 2
        elif self.angryCount > 0:  # Pokemon is angry so make it more likely to flee
            flee_stat = (self.monster.speed % 256) * 4
        elif self.eatingCount > 0:  # Pokemon is eating so make it less likely to flee
            flee_stat = (self.monster.speed % 256) / 4

        rand = random.randint(0, 255)
        # if speed gets too high the monster will flee no matter what or there is a random chance Pokemon flees based on flee_stat
        if flee_stat > 255 or flee_stat > rand:
            self.dropWidgets()
            self.createRunButton("Continue")
            state = "The " + self.monster.name + " ran away!"
            self.createMessageLabel(state)

    def throwRock(self):
        '''Computes the logic and adjustment of stats when the Throw Rock
        button is pressed by the player.
        '''

        # calculates the probability that a Pokemon will be caught it a Pokeball is thrown
        self.monster.ind_rate = int(self.monster.ind_rate) * 2
        self.monster.catch_rate = (
            (min(min(int(self.monster.ind_rate), 255), 151) / 449.5) * 100)

        # Pokemon adds a random level of angry
        self.angryCount = self.angryCount + random.randint(1, 5)
        self.eatingCount = 0  # Pokemon stops eating if it's eating

        speed = self.monster.speed * 4  # used to calculate run_prob

        # makes it more likely for a Pokemon to run
        self.run_prob = (min(255, speed) / 256) * 100

        self.dropWidgets()
        self.createWidgets()

    def throwBait(self):
        '''Computes the logic and adjustment of stats when the Throw Bait
        button is pressed by the player.
        '''

        # calculates the probability that a Pokemon will be caught it a Pokeball is thrown
        self.monster.ind_rate = (int(self.monster.ind_rate) / 2) // 1
        self.monster.catch_rate = (
            (min(min(int(self.monster.ind_rate), 255), 151) / 449.5) * 100)

        # Pokemon adds a random level of eating
        self.eatingCount = self.eatingCount + random.randint(1, 5)
        self.angryCount = 0  # Pokemon stops being angry if it's angry

        # changes liklihood of a Pokemon to run
        self.run_prob = (int(self.monster.speed / 2) / 256) * 100

        self.dropWidgets()
        self.createWidgets()


# These lines start the app
app = SafariSimulator(tk.Tk())
app.mainloop()
