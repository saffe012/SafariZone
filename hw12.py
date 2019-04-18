import tkinter as tk
import random

#Extra-Credit Completed: Part 1 & Part 2

#FIRST: Implement and test your Pokemon class below
class Pokemon:

    def __init__(self, name, number, ind_rate, catch_rate, speed):

        self.name = name
        self.number = number
        self.ind_rate = ind_rate
        self.catch_rate = catch_rate
        self.speed = int(speed)

    def __str__(self):

        return self.species
    



#NEXT: Complete the class definition provided below
class SafariSimulator(tk.Frame, Pokemon):
    def __init__(self, master=None):
        #read in the data file from pokedex.csv at some point here
        #it's up to you how you store and handle the data (e.g., list, dictionary, etc.),
        #but you must use your Pokemon class in some capacity
        file = open('pokedex.csv', 'r')
        line = file.readline()
        poke_list = []
        while line != '':
            line = file.readline()
            line = line.strip('\n')
            words = line.split(',')
            poke_list.append(words)

        self.poke_list = poke_list

        #don't forget to initialize any instance variables you want to track here
        self.safari_balls = 30
        self.captured_poke = []
        #DO NOT MODIFY: These lines set basic window parameters and create widgets
        tk.Frame.__init__(self, master)
        master.minsize(width=275, height=350)
        master.maxsize(width=275, height=400)
        master.title("Safari Zone Simulator")
        self.pack()
        #call nextPokemon() method here to initialize your first random pokemon
        self.first = True
        self.nextPokemon()
        self.createWidgets()

    def createWidgets(self):

        #You need to create an additional "throwButton"
        self.throwButton = tk.Button(self)
        state2 = "Throw Safari Ball(" + str(self.safari_balls) + " left)"
        self.throwButton["text"] = state2
        self.throwButton["command"] = self.throwBall
        self.throwButton.pack()

        #"Run Away" button has been completed for you as an example:
        self.runButton = tk.Button(self)
        self.runButton["text"] = "Run Away"
        self.runButton["command"] = self.nextPokemon
        self.runButton.pack()

        self.rockButton = tk.Button(self)
        self.rockButton["text"] = "Throw Rock"
        self.rockButton["command"] = self.throwRock
        self.rockButton.pack()

        self.baitButton = tk.Button(self)
        self.baitButton["text"] = "Throw Bait"
        self.baitButton["command"] = self.throwBait
        self.baitButton.pack()

        #A label for status messages has been completed for you as an example:
        state = "You encountered a wild " + self.name
        self.messageLabel = tk.Label(bg="grey",text=state)
        self.messageLabel.pack(fill="x", padx=5, pady=5)

        #You need to create two additional labels:
        
        #Complete and pack the pokemonImageLabel here.
        file_name = str(self.number) + ".gif"
        photo = tk.PhotoImage(file=file_name)
        self.w = tk.Label(image=photo)
        self.w.photo = photo
        self.w.pack()
        
        #Complete and pack the catchRateLabel here.
        state1 = "Your chance of catching it is " + str(self.catch_rate//1) + "%!"
        self.catchRateLabel = tk.Label(bg="grey",text=state1)
        self.catchRateLabel.pack(fill="x",padx=5,pady=5)

        state2 = "The chances it runs is " + str(self.run_prob//1) + "%!"
        self.runRateLabel = tk.Label(bg="grey",text=state2)
        self.runRateLabel.pack(fill="x",padx=5,pady=5)

    def nextPokemon(self):
        
        #This method must:
            #generate a random pokedex number
            #get the info for the appropriate pokemon
            #ensure text in the messageLabel and catchRateLabel matches this pokemon
            #change the pokemonImageLabel to show the right pokemon
        self.ball = True
        if self.first == True:
            number = random.randint(1,151)
            info = self.poke_list[number-1]
            name = info[1]
            catch_rate = ((min((int(info[2])+1),151)/449.5) * 100)
            number = info[0]
            speed = info[3]
            self.run_prob = ((2*int(speed))/256)*100
            self.angryCount = 0
            self.eatingCount = 0
            Pokemon.__init__(self, name, number, info[2], catch_rate, speed)
            self.first = False
        else:
            number = random.randint(1,151)
            info = self.poke_list[number-1]
            name = info[1]
            catch_rate = ((min((int(info[2])+1),151)/449.5) * 100)
            number = info[0]
            speed = info[3]
            self.run_prob = ((2*int(speed))/256)*100
            self.angryCount = 0
            self.eatingCount = 0
            Pokemon.__init__(self, name, number, info[2], catch_rate, speed)
            
            self.runButton.pack_forget()
            self.throwButton.pack_forget()
            self.messageLabel.pack_forget()
            self.w.pack_forget()
            self.catchRateLabel.pack_forget()
            self.rockButton.pack_forget()
            self.baitButton.pack_forget()
            self.runRateLabel.pack_forget()
            self.createWidgets()

        #hint: to see how to create an image, look at the documentation for the PhotoImage class in tkinter
            #once you generate a PhotoImage instance, it can be displayed by setting self.pokemonImageLabel["image"] to it
            #weird note: the PhotoImage instance needs to be stored as a self. variable either in this class or in your Pokemon class

    def endAdventure(self):

        self.runButton.pack_forget()
        self.throwButton.pack_forget()
        self.messageLabel.pack_forget()
        self.w.pack_forget()
        self.rockButton.pack_forget()
        self.baitButton.pack_forget()
        self.runRateLabel.pack_forget()
        self.catchRateLabel.pack_forget()

        state1 = "You're all out of balls, hope you had fun!"
        self.finalLabel = tk.Label(bg="grey",text=state1)
        self.finalLabel.pack(fill="x",padx=5,pady=5)

        if self.captured_poke == []:
            state2 = "Oops, you caught 0 Pokemon."
        else:
            state2 = "You caught " + str(len(self.captured_poke)) + " Pokemon:\n" + self.captured_poke[0]
            for i in range(1,len(self.captured_poke)):
                state2 = state2 + '\n' + self.captured_poke[i]
        
        self.finalLabel2 = tk.Label(bg="grey",text=state2)
        self.finalLabel2.pack(fill="x",padx=5,pady=5)
        
        #This method must: 

            #display advengture completion message
            #list captured pokemon

        #hint: to remove a widget from the layout, you can call the pack_forget() method
            #for example, self.pokemonImageLabel.pack_forget() removes the pokemon image

    
    def throwBall(self):

        self.safari_balls = self.safari_balls - 1
        self.runButton.pack_forget()
        self.throwButton.pack_forget()
        self.messageLabel.pack_forget()
        self.w.pack_forget()
        self.rockButton.pack_forget()
        self.baitButton.pack_forget()
        self.runRateLabel.pack_forget()
        self.catchRateLabel.pack_forget()
        self.createWidgets()
        number = random.randint(0,100)
        if number <= self.catch_rate:
            self.captured_poke.append(self.name)
            self.runButton.pack_forget()
            self.throwButton.pack_forget()
            self.messageLabel.pack_forget()
            self.w.pack_forget()
            self.rockButton.pack_forget()
            self.baitButton.pack_forget()
            self.runRateLabel.pack_forget()
            self.catchRateLabel.pack_forget()
            self.runButton = tk.Button(self)
            self.runButton["text"] = "Continue"
            self.runButton["command"] = self.nextPokemon
            self.runButton.pack()
            state = "You caught a wild " + self.name + "!"
            self.messageLabel = tk.Label(bg="grey",text=state)
            self.messageLabel.pack(fill="x", padx=5, pady=5)
            file_name = "safari_ball.gif"
            photo = tk.PhotoImage(file=file_name)
            self.w = tk.Label(image=photo)
            self.w.photo = photo
            self.w.pack()
        else:
            self.runButton.pack_forget()
            self.throwButton.pack_forget()
            self.messageLabel.pack_forget()
            self.w.pack_forget()
            self.rockButton.pack_forget()
            self.baitButton.pack_forget()
            self.runRateLabel.pack_forget()
            self.catchRateLabel.pack_forget()
            self.throwButton = tk.Button(self)
            state2 = "Throw Safari Ball(" + str(self.safari_balls) + " left)"
            self.throwButton["text"] = state2
            self.throwButton["command"] = self.throwBall
            self.throwButton.pack()
            self.runButton = tk.Button(self)
            self.runButton["text"] = "Run Away"
            self.runButton["command"] = self.nextPokemon
            self.runButton.pack()
            self.rockButton = tk.Button(self)
            self.rockButton["text"] = "Throw Rock"
            self.rockButton["command"] = self.throwRock
            self.rockButton.pack()
            self.baitButton = tk.Button(self)
            self.baitButton["text"] = "Throw Bait"
            self.baitButton["command"] = self.throwBait
            self.baitButton.pack()
            state = "You you failed to catch the wild " + self.name
            self.messageLabel = tk.Label(bg="grey",text=state)
            self.messageLabel.pack(fill="x", padx=5, pady=5)
            file_name = str(self.number) + ".gif"
            photo = tk.PhotoImage(file=file_name)
            self.w = tk.Label(image=photo)
            self.w.photo = photo
            self.w.pack()
            state1 = "Your chance of catching it is " + str(self.catch_rate//1) + "%!"
            self.catchRateLabel = tk.Label(bg="grey",text=state1)
            self.catchRateLabel.pack(fill="x",padx=5,pady=5)
            state2 = "The chances it runs is " + str(self.run_prob//1) + "%!"
            self.runRateLabel = tk.Label(bg="grey",text=state2)
            self.runRateLabel.pack(fill="x",padx=5,pady=5)

        if self.safari_balls == 0:
            self.endAdventure()
        if self.angryCount == 0 and self.eatingCount == 0:
            x = (self.speed % 256) * 2
        elif self.angryCount > 0:
            x = (self.speed % 256) * 4
        elif self.eatingCount > 0:
            x = (self.speed % 256) / 4
        if x > 255:
            self.runButton.pack_forget()
            self.throwButton.pack_forget()
            self.messageLabel.pack_forget()
            self.rockButton.pack_forget()
            self.baitButton.pack_forget()
            self.runRateLabel.pack_forget()
            self.w.pack_forget()
            self.catchRateLabel.pack_forget()
            self.runButton = tk.Button(self)
            self.runButton["text"] = "Continue"
            self.runButton["command"] = self.nextPokemon
            self.runButton.pack()
            state = "The " + self.name + " ran away!"
            self.messageLabel = tk.Label(bg="grey",text=state)
            self.messageLabel.pack(fill="x", padx=5, pady=5)
        else:
            rand = random.randint(0,255)
            if rand < x:
                self.runButton.pack_forget()
                self.throwButton.pack_forget()
                self.messageLabel.pack_forget()
                self.rockButton.pack_forget()
                self.baitButton.pack_forget()
                self.runRateLabel.pack_forget()
                self.w.pack_forget()
                self.catchRateLabel.pack_forget()
                self.runButton = tk.Button(self)
                self.runButton["text"] = "Continue"
                self.runButton["command"] = self.nextPokemon
                self.runButton.pack()
                state = "The " + self.name + " ran away!"
                self.messageLabel = tk.Label(bg="grey",text=state)
                self.messageLabel.pack(fill="x", padx=5, pady=5)

    def throwRock(self):
        
        self.ind_rate = int(self.ind_rate) * 2    
        self.catch_rate = ((min(min(int(self.ind_rate),255),151)/449.5) * 100)
        
        self.angryCount = self.angryCount + random.randint(1,5)
        self.eatingCount = 0

        speed = self.speed * 4
        
        self.run_prob = (min(255, speed)/256) * 100

        self.runButton.pack_forget()
        self.throwButton.pack_forget()
        self.messageLabel.pack_forget()
        self.w.pack_forget()
        self.catchRateLabel.pack_forget()
        self.rockButton.pack_forget()
        self.baitButton.pack_forget()
        self.runRateLabel.pack_forget()
        self.createWidgets()

    def throwBait(self):

        self.ind_rate = (int(self.ind_rate) / 2)//1    
        self.catch_rate = ((min(min(int(self.ind_rate),255),151)/449.5) * 100)
        
        self.eatingCount = self.eatingCount + random.randint(1,5)
        self.angryCount = 0
        
        self.run_prob = (int(self.speed/2)/256)*100

        self.runButton.pack_forget()
        self.throwButton.pack_forget()
        self.messageLabel.pack_forget()
        self.w.pack_forget()
        self.catchRateLabel.pack_forget()
        self.rockButton.pack_forget()
        self.baitButton.pack_forget()
        self.runRateLabel.pack_forget()
        self.createWidgets()

        
        
        #This method must:

            #decrement the number of balls remaining
            #check to see if endAdventure() should be called
            #otherwise, try to catch the pokemon

        #Don't forget to update the throwButton's text to reflect one less pokeball
        #Don't forget to call runAway to generate a new pokemon if this one is caught


#DO NOT MODIFY: These lines start your app
app = SafariSimulator(tk.Tk())
app.mainloop()
