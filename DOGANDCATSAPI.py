
# Imports /// Requests for GET/PUSH,ect /// Time to delay while looking in chat /// json to parse json data
import requests
import json
import time


#Variables
# Webex-URL's
roomsurl = ('https://api.ciscospark.com')
posturl = ('https://webexapis.com')


#Webex-Params
rms = ('/v1/rooms')
msgs = ('/v1/messages')


# Webex-Key ==> "This is hardcoded if want to use change every 10 hours"
at = ('') #ADDYOUROWNWEBEXTOKENOVERHERE


# Dog key + mainurl
dogkey = ('') #ADDYOUWOWNDOGAPIKEYOVERHERE
dogurl = ('https://api.thedogapi.com')


# Dog-Params
image = ('/v1/images/search')
png = ('/v1/images/search?mime_types=png')
gif = ('/v1/images/search?mime_types=gif')


# CATURL
caturl = ('https://api.thecatapi.com')
boxes = ('/v1/images/search?category_ids=5')
clothes = ('/v1/images/search?category_ids=15')
space = ('/v1/images/search?category_ids=2')
sunglasses = ('/v1/images/search?category_ids=4')


# Empty variable to use in script
gevondenkamer = ""




#Definitions
#Definition to shorten actual code // search for command ## Display command ## Request for dog ## Post Dog ## Errorcode checking \\ 
def opvraag(mainurl,extraurl, wat, tekst1, tekst2, tekst3):
    if message == wat:

        print(f'\n Found command:  {tekst1}  \nRandom  {tekst2} inc:\n')

        # get request to API
        dog_get = requests.get(mainurl+extraurl, dogkey)

        random_dog = dog_get.json()
        select_url = random_dog[0]['url']
        print(select_url)
        post_parameters = {"parentId": parent_id, "roomId": roomIdToGetMessages,
                           "text": f"{tekst3}" ,"files": select_url}

        dog_post = requests.post(posturl + msgs, data=json.dumps(post_parameters), headers={
                                 'Authorization': accessToken, 'Content-Type': 'application/json'})

        if not dog_post.status_code == 200:
            raise Exception("Incorrect reply from Webex API. Status code: {}. Text: {}".format(
                dog_post.status_code, dog_post.text))




# Definition for /help en /catcategories - Text only
def help(wat,markdown,tekst1):
    if message == wat:
        
        
        print(f'\n Found command: {tekst1}')

        
        post_parameters = {"parentId": parent_id, 
                            "roomId": roomIdToGetMessages,
                            "markdown": f"{markdown}",
                            }

        
        msg_post = requests.post(posturl + msgs, data=json.dumps(post_parameters), headers={'Authorization': accessToken, 'Content-Type': 'application/json'})

        if not msg_post.status_code == 200:
            raise Exception("Incorrect reply from Webex API. Status code: {}. Text: {}".format(msg_post.status_code, msg_post.text))





# Definition for Catcategories with markdown
def categories(wat,tekst1,mainurl,extrurl,mkdown):
            if message == wat:

                print(f'\n Found command:  {tekst1}  \nRandom  {tekst1} inc:\n')

                # get request to API
                dog_get = requests.get(mainurl+extrurl, dogkey)

                random_dog = dog_get.json()
                select_url = random_dog[0]['url']
                print(select_url)
                post_parameters = {"parentId": parent_id, "roomId": roomIdToGetMessages,
                                "markdown": mkdown ,"files": select_url,}

                dog_post = requests.post(posturl + msgs, data=json.dumps(post_parameters), headers={
                                        'Authorization': accessToken, 'Content-Type': 'application/json'})

                if not dog_post.status_code == 200:
                    raise Exception("Incorrect reply from Webex API. Status code: {}. Text: {}".format(
                        dog_post.status_code, dog_post.text))




# Tokens // Use hardcode Y or N ==> N ==> give own accesstoken ==> y go to next \\ // Errorcodecontrol \\ 
#        //In Loop so if they type something else they stay inside of it \\
while True:
    

    choice = input("Wil je een reeds ingevulde token gebruiken ? (ja/nee)").lower()


    while choice[0] != 'n' and choice[0] != 'j':
        print('Gelieve alleen met ja of nee te antwoorden !')
        choice = input('Alle, we gont nog ki proberen: Wil je de reeds ingevulde token gebruiken (ja of nee) ?').lower()


    if choice[0] == "n":
        accessToken = input("Geef hier je eigen access token in : ")
        accessToken = "Bearer " + accessToken
        headers = {'Authorization': accessToken}
        statuscheck = requests.get(url=roomsurl + rms, headers={"Authorization": accessToken})


        if not statuscheck.status_code == 200:
            print('Ingegeven Token klopt niet !!')
        elif statuscheck.status_code == 200:
            print('In orde !')
            break

    else:
        accessToken = 'Bearer ' + at
        headers = {'Authorization': accessToken}
        break


#Testing if the hardcoded token is still valid
r = requests.get(   "https://api.ciscospark.com/v1/rooms",
                    headers = {"Authorization": accessToken}
                )


if not r.status_code == 200:
    raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))


#Webex rooms GET request to load rooms.
while True:
    room = {}
    r = requests.get(url=roomsurl + rms,headers={"Authorization": accessToken})
    data = r.json()
    rooms = r.json()["items"]
    roomTitleToGetMessages = ""
    roomIdToGetMessages = ""


    # Displays a list of rooms. // Print list of rooms with for loop \\ // Ask input if input exists with the parse use it \\ 
    #                           // Else make new room and use that one \\
    print("Kamerlijst:")
    roomlist = []
    for room in rooms:
        print(room["title"])


    ## Ask // input and parse title and id so we can use it to select \\
    room_input = input(f"\nKies een kamer uit de lijst hierboven om te monitoren voor bot commando's : ")


    for room in rooms:
        if room["title"] == room_input:
            gevondenkamer = room


    #If // we find something in "gevondenkamer" we put them in variables\\
    if gevondenkamer:
        roomTitleToGetMessages = gevondenkamer["title"]
        roomIdToGetMessages = gevondenkamer["id"]


    # //Make one if gevondenkamer = "" \\  // Use the name we chose with the room_input variable \\ 
    else:
        print("Sorry, room bestaat niet :" + room_input)
        body = {'title': room_input}
        res = requests.post(roomsurl + rms, headers=headers, json=body)
        print("Nu wel; we hebben deze aangemaakt :" + room_input)
        roomIdToGetMessages = res.json()['id']
        roomTitleToGetMessages = res.json()['title']
        

    print("Found room : " + roomTitleToGetMessages)
    
    #Make post in found room // Show that we are here and working \\
    body = {"markdown": "### Bot Actief - Om alle commando's op te vragen gebruik /help",
            "roomId": roomIdToGetMessages}
    requests.post(url=posturl + msgs, headers={"Authorization": accessToken}, json=body)


    # The active part // While True loop we never break \\ // Time.sleep to not go over the maximum request limit \\
    # // Sending a get messages get every 1 second, parse the returned json and then store it inside message until loop restarts \\
    while True:
        time.sleep(1)
        print('Luisteren')
        GetParameters = {"roomId": roomIdToGetMessages, "max": 1}
        
        r = requests.get(posturl+msgs,params=GetParameters, headers={"Authorization": accessToken})


        #Errorchecking // \\
        if not r.status_code == 200:
            raise Exception("Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))


        #Reply on the previous request
        json_data = r.json()
        if len(json_data["items"]) == 0:
            raise Exception("There are no messages in the room.")


        elif len(json_data["items"]) == 1:
            print("Nog niks ontvangen")


        # Store // message that is parsed out of the json data to use and reply later on \\
        messages = json_data["items"]


        #Finding PID // Find id en PID and store in variable \\.
        for message in messages:
            if 'parentId' in message:
                parent_id  = message['parentId']

            else:
                parent_id = message["id"]


        # Store // First msg in chat and use to reply in next part \\
        message = messages[0]["text"]


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
                        #USING THE DEF FROM THE BEGINNING OF THE SCRIPT WITH ADDED PARAMS
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/



#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
                                        #FIRST ALL THE "BASIC" COMMANDS
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/


# command: /help
        help("/help","""## Mogelijke commando's.\n\n**/hond** : ``` krijg een random hond ```\n**/hondgif** : ``` krijg een random hond in gif formaat ```\n \
        **/hondpng** : ``` krijg een random hond in png formaat ```\n**/miauw** : ``` krijg een random kat ``` \
        \n**/catcategories** : ``` Hoe vraag ik verschillende categoriën Katten op ```""",'/help') 

# command: /hond
        opvraag(dogurl,image, '/hond', '/hond', 'Random hond','Rando DOGGY')

# command: /hondgif
        opvraag(dogurl,gif, '/hondgif', '/hondgif', 'Random hondgif','DOOOOOOOOOOOOG GIF')

# command: /hondpng
        opvraag(dogurl,png, '/hondpng', '/hondpng', 'hond in png','DOOOOOOOOOOOG in PNGFORMAT')
    
# command: /miauw
        opvraag(caturl,image, '/miauw', '/miauw', 'What a cat ?','CAAAAAAAAT')




#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
                                 #FROM HERE ON ITS ALL ABOUT THE CATEGORIES
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/


# command: /catcategories
        help("/catcategories","""## Te verkrijgen Categoriën.\n\n**/doos** : ``` Krijg een kat in een doos ```\n**/kleren** : ``` Krijg een kat met kleren ```\n \
        **/space** : ``` Krijg een spaceKitty ```\n**/zonnebril** : ``` Krijg een kat met een zonnebril```\n""","/catcategories")

# command: /doos      
        categories('/doos', '/doos',caturl,boxes,'- [x] ```Kitten in a box```\n - [ ]  ```Kitten outside a box```')

# command: /kleren      
        categories('/kleren', '/kleren',caturl,clothes,'- [x] ```Clothing und Cat Always Funz```\n - [ ] ```Naked Cat```')

# command: /space      
        categories('/space', '/space',caturl,space,'- [x] ```SpaceCat```\n - [ ]  ```Scaredy Cat```') 

# command: /zonnebril      
        categories('/zonnebril', '/zonnebril',caturl,sunglasses,'- [x] ```Cat with sunglasses```\n - [ ]  ```Cat without sunglasses```')
