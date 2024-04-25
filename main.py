'''
LINK: https://github.com/SoggySwann/RPGProjectJake

AUTHOR: JAKE SWANN
DATE: 4/25/24
ASSIGNMENT: PROJECT 2
COURSE: CPSC 1050

DESCRIPTION: Using classes, branches, loops, methods, etc., I designed a map based navigation game where the user is a hobo. They navigate and use items to gain helath and win if they go to 100 health. 
'''

class ExitNotFoundError(Exception):    # handles when room isnt found
    def __init__(self, room_name, message="Location is too far away"):   #constructor method for the class 
        self.room_name = room_name # assigning room name
        self.message = message #assign messgae of defualt message

    def __str__(self):
        return f"{self.room_name} -> {self.message}"  #formatted string


class Room:  #class for locations in game 
    def __init__(self, name, description, exits, item=None):
        self.name = name  #assings name 
        self.description = description  #assigns decription
        self.exits = exits #assigns exits 
        self.item = item  # assigns item
        self.item_taken = False  #flag to track if the item has been taken

    def get_name(self):  #gets name of room 
        return self.name

    def get_description(self):  #gets description
        return self.description

    def get_exits(self):  #gets exits 
        return self.exits

    def list_exits(self):  #lists exits 
        return "\n".join(self.exits)

    def get_item(self):  #checks if theres an item in room 
        if not self.item_taken:
            return self.item
        else:
            return None

    def take_item(self):  #represents taking item from room
        self.item_taken = True

    def use_item(self, player):  #using item 
        if self.item:    #if there is item
            item_name, (health_effect, description) = list(self.item.items())[0]  #get info
            print(description)   #prints info
            player.health += health_effect   #changes health accordingly
            print(f"Current health: {player.health}")  #print healt
            self.item_taken = True   #item is now taken
        else:
            print("There is no item in this location.")   #if theres no item print this                

    def __str__(self): #method for room
        item_info = f"{list(self.item.keys())[0]}" if self.item else "No item available"   #gets item ifno
        return f"{self.name}: {self.description}\n{item_info}"  #returns string


class AdventureMap:  #map class
    def __init__(self):   
        self.map = {}   #initialized to later store locations

    def add_room(self, room):  #adds locations
        self.map[room.name.lower()] = room

    def get_room(self, room_name):    #gets locations
        room = self.map.get(room_name.lower())   #get location from map
        if room is None: # if room isnt found
            raise ExitNotFoundError(room_name)   
        return room


class Player:  # player class
    def __init__(self):
        self.health = 50  # initial health for player


def main():   #main fucntion 
    adventure_map = AdventureMap()  #instance of map
    player = Player()   #instance of player

    #adding all locations
    adventure_map.add_room(Room("McDonald's", "You shuffle around aimlessly until finding the golden arches.", ['Corner Store'], {"A worker sees you stumble in and pass out on a table. They feel bad for you and decide throw a big mac your way": (30, "The burger melts in your mouth as you gobble down and lick your fingers.")}))

    adventure_map.add_room(Room("Under a Bridge", "The sound of a harmonica and blues echo in the air. Following the sound, you're lead to a hobo camp under an abandoned overpass.", ["Casino", "Intersection", "Shady Neighborhood"], {"You make friends with the homeless folk and remeniss about experiences. After a while they start making dinner, mentioning there's a hotdog with your name on it.": (40, "The warm hotdog is just what you need to fill up!.")}))

    adventure_map.add_room(Room("Corner Store", "You smell the scent of cheap cigarettes and honey buns getting stronger. Following your nose leads to the local corner store.\nUpon walking in you recieve stares from everyone.", ["Shady Neighborhood", "McDonald's"], {"You want to leave the store as soon as possible before you're kicked out. From of the corner of your eye you see a flashy pill box with a picture of a rhino on it": (-40, "You grab the box of rhino pills, eat a few, then dash out of the store. Your heart is pumping rather fast now and you long to find a hobo wife. Life sucks.")}))

    adventure_map.add_room(Room("Shady Neighborhood", "You stumble around until a smelly man gives you info on places you can walk to.", ["Corner Store", "Under a Bridge", "Park Bench"], {"He offers you a warm pickle from his back pocket. It's a dill pickle from the looks of it.": (30, "The pickle is only a few days old and turns out to be rather tasty!")}))

    adventure_map.add_room(Room("Casino", "You follow the flashing signs until you reach the casino. Upon entering you walk around and take in the sights. ", ["Under a Bridge"], {"You go to use the restroom and find a bag of a white powder-like substance": (-30, "You injest the powder and feel like a million bucks! 5 minutes later you start to sober up. You are now addicted to cocaine.")}))

    adventure_map.add_room(Room("Intersection", "You follow street signs until reaching an intersection.", ["Park Bench", "Under a Bridge"], {"It's hot, dry, and you need something to quench your thirst. You go up to your competition, another hobo.\nHe's missing one leg and most of his teeth. He offers you a supposed lemon-lime gatorade that's half empty.": (30, "The gatorade turns out to be urine, a sub-par source of hydration but still worth something!.")}))

    adventure_map.add_room(Room("Park Bench", "You find a comfy park bench under a shady tree to sleep on. After moving a bag of dog poop off the seat, you lay down and take a nap", ["Shady Neighborhood", "Intersection"], {"Upon waking up, you find a lost small poodle roaming around. It looks to be well maintained and would make a nice meal.": (-30, "You cook the dog to the best of your abilities. Your fire goes out early but you eat anyways. The dog was raw so you now have salmonela and a dog tracker in your stomach.")}))
# initial print message intro
    print("\nJAKE'S HOBO SIMULATOR\n\nHello random citizen and welcome to the hobo simulator! \nYou will now be stripped of all belongings but the clothes on your back and dropped off at a shady neighborhood in Detroit.\nMonitor your health along the way to make sure you don't die.\nIf you get to 100 health, you will be healthy enough to get a job and win the game!\nCurrent Health: 50\n")

    current_room = adventure_map.get_room("Shady Neighborhood")  #setting starting room

    while True:  #main loop
        print(f"{current_room}")   #prints current room info 
        if current_room.get_item():   #if item exists 
            print("(Use item? Yes/No)")
            use_item_choice = input().upper()
            if use_item_choice == "YES":   #if they use item
                current_room.use_item(player)   #use item
                print()
                if player.health >= 100:   #if health is 100 the win
                    print("You are now healthy enough to get a job. Congrats!")
                    exit()
                if player.health <= 0:   #if health too low theu loose 
                    print("Due to your poor health, you died. Better luck next time!")
                    exit()
            elif use_item_choice == "NO":    #if they dont use item
                print(f"Your current health: {player.health}")
            else:
                while use_item_choice != "NO" and use_item_choice != "YES":   #input validation
                    print("Invalid Choice. Please choose Yes or No.")
                    use_item_choice = input().upper()
                    if use_item_choice == "YES":
                        current_room.use_item(player)
                        print()
                        if player.health >= 100:
                            print("You are now healthy enough to get a job. Congrats!")
                            exit()
                        if player.health <= 0:
                            print("Due to your poor health, you died. Better luck next time!")
                            exit()
                    elif use_item_choice == "NO":
                        print(f"Your current health: {player.health}")
                    else:
                        continue


        else:
            print("There is no longer an item here.")  #if item isnt in location anymore
            print(f"Your current health: {player.health}")

        print("Which location do you want to walk to next? Enter your answer (or 'Exit' to quit).")
        print(current_room.list_exits())
        user_input = input().capitalize().strip()

        if user_input == "Exit":  #if player inpts exit 
            print("Exiting the game...")
            break #quits game

        if user_input in adventure_map.map:   # if valid location
            next_room_name = user_input   
            current_room = adventure_map.get_room(next_room_name)  #sets room 
        elif user_input.lower() in map(str.lower, current_room.get_exits()): #if input mathes exit
            next_room_name = user_input.capitalize()
            try:
                current_room = adventure_map.get_room(next_room_name) #move to next room 
            except ExitNotFoundError as e:  #if room not found
                print(f"Invalid room: {e}") 
        else:
            while True:
                print(f"Location '{user_input}' isn't known. Please enter a valid location.")
                print(current_room.list_exits())
                user_input = input().capitalize().strip()

                if user_input in adventure_map.map:  #if location exists
                    next_room_name = user_input  #next location is input
                    current_room = adventure_map.get_room(next_room_name)   #next room
                    break
                elif user_input.lower() in map(str.lower, current_room.get_exits()):  #if input is valid 
                    next_room_name = user_input.capitalize()
                    try:
                        current_room = adventure_map.get_room(next_room_name)  #get next room
                        break
                    except ExitNotFoundError as e:   #if invalid room 
                        print(f"Invalid room: {e}")
                else:
                    continue  #go back through loop

if __name__ == "__main__":
    main()