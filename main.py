import random

miles = 1000
money = 500
food = 500
bullets = 3
medicine = 1
days = 0
message = ""
city = False
events_range = [1, 30]
damage_value = 27
medicine_value = 15
members_value = 4
location_range = [1 , 10]
location_value = 9
miles_range = [10 , 50]
days_range = [1 , 3]
food_divider = 2
damage_range = [17 , 37]

big_places = [
"France" ,
"Spain" ,
"Germeny" ,
"United Kingdom" ,
"Switzerland" ,
"Lithuania" ,
"Netherlands" ,
"Belgium" ,
"Poland" ,
"Italy" ,
"Monaco" ,
"Greece" ,
"Bulgaria"
]

small_places = [
"park" ,
"campsite" ,
"river" ,
"trail" ,
"lake" ,
"mountain"
]

colors = [
"red" ,
"blue" ,
"green" ,
"purple" ,
"black" ,
"white"
]

shapes = [

"circle" ,
"square" ,
"triangle" ,
"rectangle" ,
"hexagon" ,
"pentagon" ,
"poly"
]

animals = {
"bison": {"food": 200 , "bullets": 5 , "rare": 4 } ,
"deer": {"food": 100 , "bullets": 3 , "rare": 6} ,
"rabbit": {"food": 50 , "bullets": 2 , "rare": 8} ,
"bird": {"food": 10 , "bullets": 1 , "rare": 10}
}
damage_types = ["animal bite" , "sickness" , "bear attack" , "food poisoning" , "frost bite"]

store = {
"bullets": {"price":25 , "amount": 10 , "id": "10"} ,
"food": {"price":250 , "amount": 100 , "id": "20"} ,
"medicine": {"price":25 , "amount": 1 , "id": "30"}
}

menus = {
    1 : "MOVE" ,
    2 : "HUNT" ,
    3 : "HEAL" ,
    4 : "BUY" ,
    5 : "EXIT"
}

members = {
    1: {"name": None , "health": 100} ,
    2: {"name": None , "health": 100} ,
    3: {"name": None , "health": 100} ,
    4: {"name": None , "health": 100}

}

dead_members = []

def foods(requirement,players):
    global food
    preq = food - requirement
    food -= requirement
    if preq < 0:
        conseq_num = round(abs(preq) / players)
        message = "You are out of food"
        for member,data in members.items():
            if data['name'] not in dead_members:
                data['health'] -= conseq_num
                member_health = data['health']
                member_name = data['name']
                if member_health <= 0:
                    dead_members.append(member_name)
                    members[member]['health'] = 0
                    message += f"\n{member_name} has starved to death"
    else:
        message = None

    if food < 0:
        food = 0
    return message

def move():
    global miles
    global food
    global days
    global city

    loc_num = random.randint(location_range[0],location_range[1])
    if loc_num >= location_value:
        city = True
    else:
        city = False

    miles_num = random.randint(miles_range[0],miles_range[1])
    miles -= miles_num

    days_num = random.randint(days_range[0],days_range[1])
    days += days_num

    active_players = len(members) - len(dead_members)
    food_requirement = round(miles_num / food_divider) * active_players
    food_message = foods(food_requirement,active_players)

    if city == True:
        loc_choice = random.choice(big_places)
        big_places.remove(loc_choice)
        message = f"You have traveled to {loc_choice.upper()} in {miles_num} miles and {days_num} days"
    else:
        loc_choice = random.choice(small_places)
        color_choice = random.choice(colors)
        shape_choice = random.choice(shapes)
        message = f"You have traveled to {color_choice.upper()} {loc_choice.upper()} {shape_choice.upper()} in {miles_num} miles and {days_num} days"
    if food_message != None:
        message += f"\n{food_message}"




    return message

def buy():
    global money
    global food
    global bullets
    global medicine
    status_buy = True
    message =""
    while status_buy:
        menu_buy()
        print(message)
        item_number = input("Enter the item number: ")
        isValid = False
        for k,v in store.items():
            if item_number == store[k]['id']:
                isValid = True
                item_cost = store[k]['price']
                item_amount = store[k]['amount']
                if money >= item_cost:
                    money -= item_cost

                    if k == "bullets":
                        bullets += item_amount
                    elif k == "medicine":
                        medicine += item_amount
                    elif k == "food":
                        food += item_amount

                    message = f"You bought {k}"
                else:
                    message = "You don't have enough money"


        if item_number == "0":
            status_buy = False
            message = "You are exiting the store"
        elif isValid == False:
            message = "That is not a valid option"

def menu():

    global days
    global miles
    global money
    global food
    global bullets
    global city
    global medicine

    MENU = f'''

    [STATS]
    -{members[1]["name"]}: HEALTH {members[1]["health"]}%
    -{members[2]["name"]}: HEALTH {members[2]["health"]}%
    -{members[3]["name"]}: HEALTH {members[3]["health"]}%
    -{members[4]["name"]}: HEALTH {members[4]["health"]}%
    _________________________________________________________

    -DAYS: {days}
    -MILES LEFT: {miles}
    -MONEY: {money}
    -FOOD: {food}
    -BULLETS: {bullets}
    -MEDICINE: {medicine}

    '''

    for k,v in menus.items():
        if v == "BUY" and city == False:
            pass
        else:
            MENU += f"\n     [{k}] - {v}"
    MENU += "\n"
    print(MENU)

def menu_buy():
    global money
    global food
    global bullets
    global medicine
    print("")
    print("##### WELCOME TO THE STORE! #####")
    print(" [STATS] ")
    print(f"- MONEY: {money}")
    print(f"- BULLETS: {bullets}")
    print(f"- MEDICINE: {medicine}")
    print(f"- FOOD: {food}")
    print("-----------------------\n")
    for k,v in store.items():
        print(f"- [ {v['id']} ] {k.upper()}: ${v['price']} for {v['amount']}")
    print("- [  0 ] EXIT STORE")
    print("##################################")
    print("")

def hunt():
    global bullets
    global food

    animal_list = []
    empty = 0

    for animal in animals:
        for amount in range(animals[animal]['rare']):
            animal_list.append(animal)

    random.shuffle(animal_list)
    animal_choice = random.choice(animal_list)
    bullets_used = animals[animal_choice]['bullets']
    food_amount = animals[animal_choice]['food']

    bullets -= bullets_used

    if bullets < 0:
        message = f"You ran out of bullets while hunting a {animal_choice}."
    else:
        food += food_amount
        message = f"You hunted a {animal_choice} using {bullets_used} bullet(s) and got {food_amount} pounds of food."

    return message

def damage():
    member_num = random.randint(1,4)
    damage_num = random.randint(damage_range[0],damage_range[1])
    damage_choice = random.choice(damage_types)
    member_name = members[member_num]['name']

    if member_name not in dead_members:
        members[member_num]['health'] -= damage_num


    member_health = members[member_num]['health']
    if member_name in dead_members:
        message = ""
    elif member_health <= 0:
        dead_members.append(member_name)
        members[member_num]['health'] = 0
        message = f"{member_name} is dead due to {damage_choice}"
    else:
        message = f"{member_name} has suffered {damage_choice} losing {damage_num} health"

    return message

def heal():
    global medicine_value
    global medicine
    temp_dict = {}
    for k,v in members.items():
        if v['name'] not in dead_members:
            get_name = v['name']
            get_health = v['health']
            temp_dict[get_name] = get_health
    sort_health = sorted(temp_dict.items(), key=lambda x:x[1])
    sort_dict = dict(sort_health)

    num = 0
    for name,health in sort_dict.items():
        num += 1
        if num == 1:
            health_total = health + medicine_value
            if health_total > 100:
                for k,v in members.items():
                    if v['name'] == name:
                        members[k]['health'] = 100
            else:
                for k,v in members.items():
                    if v['name'] == name:
                        members[k]['health'] += medicine_value
            medicine -= 1
            message = f"{name} has been healed with medicine"
        else:
            break
    return message

name_check = []
family_name = input("Enter your family name: ")

member1_name = input("Enter name of first player: ")
members[1]["name"] = member1_name.upper()
name_check.append(member1_name.upper())

p2name_status = True
while p2name_status:
    member2_name = input("Enter name of second player: ")
    if member2_name.upper() in name_check:
        print("That name is already in use")
    else:
        members[2]["name"] = member2_name.upper()
        name_check.append(member2_name.upper())
        p2name_status = False

p3name_status = True
while p3name_status:
    member3_name = input("Enter name of third player: ")
    if member3_name.upper() in name_check:
        print("That name is already in use")
    else:
        members[3]["name"] = member3_name.upper()
        name_check.append(member3_name.upper())
        p3name_status = False

p4name_status = True
while p4name_status:
    member4_name = input("Enter name of fourth player: ")
    if member4_name.upper() in name_check:
        print("That name is already in use")
    else:
        members[4]["name"] = member4_name.upper()
        name_check.append(member4_name.upper())
        p4name_status = False

print("")
print(f"Welcome to the Tracy Trails Game, {family_name.upper()} family!")
print(f"Your family members are {member1_name}, {member2_name}, {member3_name}, and {member4_name}")
print(f"Your goal is to get to Tracy which is {miles} miles away")
print("Get everyone there safely. Good luck!")
print("")


status = True
while status:
    menu()
    print(message)
    if len(dead_members) == members_value:
        print("ALL YOUR MEMBERS HAVE DIED! GAME OVER")
        status = False
        option = None
    else:
        option = input("Enter an option: ")
    if miles <= 0:
        print(f"CONGRATULATIONS!  YOU FINISHIND THE GAME IN {days} DAYS")
        status = False
    elif option == "1":
        event = random.randint(events_range[0],events_range[1])
        if event >= damage_value:
            message = damage()
        else:
            city = False
            message = move()
    elif option == "2":
        if bullets >= 1:
            message = hunt()
        else:
            message = "You do not have enough bullets to hunt"
    elif option == "3":
        if medicine > 0:
            message = heal()
        else:
            message = "You can't heal right now"
    elif option == "4":
        buy()
    elif option == "5":
        status = False
