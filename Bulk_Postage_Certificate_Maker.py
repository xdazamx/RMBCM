"""
Royal Mail Bulk Certificate Maker (RMBCM)

This program takes a list of information about parcels from the user
and produces an image to bypass writing one out by hand.

Created on Thu Jul 20 17:23:01 2017
Version 1: Mon Jul 24 15:53:01 2017

References: http://code.activestate.com/recipes/579013-draw-text-to-image/

@author: D A Hawkes
"""

from PIL import Image, ImageFont, ImageDraw
import os
import time

Items = ["Name", "Address", "Postcode", "Service Used"]
Postage_types = {"1":"1st Class",
                 "2":"2nd Class"}
Bool = {"Y":True,
        "N":False}

def Resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def Intro():
    print("Royal Mail Bulk Certificate Maker (RMBCM 2.0)\n")

def Get_input(Prompt, Output):  #Gets input from the user and checks it for dtype error.
    run = 1
    while run == 1:
        try:
            return Output(input(Prompt))
        except ValueError:
            print("Please type a correct input")

def Check_package(package):

    run = True
    while run == True :
        try:
            to_check = Bool[Get_input("\nWould you like to change the entered information?[Y/N]:\n\n{}\n".format(package), str).upper()]
            run = False
        except KeyError:
            print("Please enter either 'y' for yes or 'n' for no.")

    check = to_check
    while check == True:
        component = Get_input("Which part would you like to edit?\n Name(1), Address(2), Postcode(3) or Service(4): {}\n".format(package), str).upper()
        if component.upper() == "1":
            package[0] = Get_input("Enter Name:   ", str).title()
            
            run_1 = True
            while run_1 == True:
                try:
                    check = Bool[Get_input("Is there another edit you would like to make? (Y/N)", str).upper()]
                    run_1 = False 
                except KeyError:
                    print("Please enter 'y' for yes and 'n' for no.")

        elif component.upper() == "2":
            package[1] = Get_input("Enter Address:   ", str).title()
            
            run_1 = True
            while run_1 == True:
                try:
                    check = Bool[Get_input("Is there another edit you would like to make? (Y/N)", str).upper()]
                    run_1 = False 
                except KeyError:
                    print("Please enter 'y' for yes and 'n' for no.") 
                    
        elif component.upper() == "3":
            package[2] = Get_input("Enter Postcode:   ", str).upper()
            
            run_1 = True
            while run_1 == True:
                try:
                    check = Bool[Get_input("Is there another edit you would like to make? (Y/N)", str).upper()]
                    run_1 = False 
                except KeyError:
                    print("Please enter 'y' for yes and 'n' for no.")
                    
        elif component.upper() == "4":
            postage_check = True
            while postage_check == True:
                try:
                    package[3] = Postage_types[Get_input("Enter service:   ", str)]
                    postage_check = False
                except(KeyError):
                    print("Please type 1 or 2 for 1st class & 2nd class respectively")
            
            run_1 = True
            while run_1 == True:
                try:
                    check = Bool[Get_input("Is there another edit you would like to make? (Y/N)", str).upper()]
                    run_1 = False 
                except KeyError:
                    print("Please enter 'y' for yes and 'n' for no.")
                    
        else:
            print("Please enter the number that corresponds to the part you wish to change.")
        
    return package

def Exit(check):
    if check.upper() == "EXIT":
        return False
    else:
        return True

def Input():    #Takes the input from the user and parcels them into a list that is read by Overlay().
    postal_list = []
    run = True
    while run == True:
        for package_number in range(30):
            
            if package_number <= 5 :
                name = Get_input("Enter Name:   ", str).title()
            else:
                name = Get_input("Enter Name or type 'exit' to finish input:   ", str).title()

            if Exit(name) == False:
                    break

            addr = Get_input("Enter Address:   ", str).title()
            pcode = Get_input("Enter Postcode:   ", str).upper()

            postage_check = True
            while postage_check == True:
                try:
                    serv = Postage_types[Get_input("Enter Service:   ", str)]
                    postage_check = False
                except(KeyError):
                    print("Please type 1 or 2 for 1st class & 2nd class respectively")

            current_package = [name, addr, pcode, serv]
            current_package = Check_package(current_package)
            postal_list.append(current_package)

        run = False

    return  postal_list

def Import():   #Imports the BCP.
    image = Image.open(Resource_path("BCP.png")).convert("RGB")
    return image

def Overlay(image, post):   #Overlays the postage information onto the BCP.
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 35)

    x_pos = [110, 523, 800, 1162]

    for j, item in enumerate(post):
        for i, entry in enumerate(item):
            draw.text((x_pos[i], 350 + 43 * j), "{}".format(entry), font= font, fill= (0, 0, 0))

    draw.text((900, 1885), "{}".format(len(post)), font= font, fill= (0, 0, 0))

    return image

def Save_image(image):  #Saves the overlay onto the BCP as a new .png .
    image.save("Bulk Postage Certificate.png")

def Main():
    Intro()
    Parcels = Input()
    BCP = Import()
    image = Overlay(BCP, Parcels)
    Save_image(image)
    print("Image saved as 'Bulk Postage Certificate.png'.")
    time.sleep(3)

Main()