import requests, json, os
from PIL import Image
from re import findall
from ezstyle import *
from time import sleep
from colorama import Fore, init
from bs4 import BeautifulSoup
init(convert=True)
#=========================================
#               __ _      
#  __ ___ _ _  / _(_)__ _ 
# / _/ _ \ ' \|  _| / _` |
# \__\___/_||_|_| |_\__, |
#                   |___/ 
#=========================================
with open("config.json", "r") as configFile:
	configuration = json.load(configFile)

cookie = configuration["auth"]["cookie"]

customClothingInfo      = configuration["clothing"]["customInfo"]
userGroupId             = configuration["clothing"]["groupId"]
userClothingPrice       = configuration["clothing"]["price"]
userClothingDescription = configuration["clothing"]["description"]

templateChange     = configuration["optional"]["templateChanger"]
rateLimitTimeout   = configuration["optional"]["rateLimitTimeout"]
uploadFee          = 10

#=========================================
#         _             
#  ______| |_ _  _ _ __ 
# (_-< -_)  _| || | '_ \
# /__|___|\__|\_,_| .__/
#                 |_|   
#=========================================
#Declaring Request Session
session                           = requests.Session()
session.cookies[".ROBLOSECURITY"] = cookie
session.headers["referer"]        = "https://www.roblox.com"

#--Getting User's Info and Validating Cookie
XCSRFRequest = session.post("https://auth.roblox.com/")
if "X-CSRF-Token" in XCSRFRequest.headers: 
    session.headers["X-CSRF-Token"] = XCSRFRequest.headers["X-CSRF-Token"]

#Checking Requests Sent
def checkRequest(type, method, request):
    method = method.upper()
    type   = type.upper()

    if request.status_code   == 200:
        cl(f"{request.reason}{Fore.WHITE} {(25-(len(request.reason)))*' '}| {Fore.LIGHTGREEN_EX}{method} {Fore.WHITE}{(25-(len(method)))*' '}| {Fore.LIGHTGREEN_EX}{type}", "green", str(request.status_code))
        return {"success": True, "code": 200}
    elif request.status_code == 429:
        cl(f"{request.reason}{Fore.WHITE} {(25-(len(request.reason)))*' '}| {Fore.RED}{method} {Fore.WHITE}{(25-(len(method)))*' '}| {Fore.RED}{type}", "red", str(request.status_code))
        ce(f"Waiting for {rateLimitTimeout} Seconds\n", "red")
        return {"success": False, "code": 429}
    else:
        cl(f"{request.reason}{Fore.WHITE} {(25-(len(request.reason)))*' '}| {Fore.RED}{method} {Fore.WHITE}{(25-(len(method)))*' '}| {Fore.RED}{type}", "red", str(request.status_code))
        return {"success": False, "code": request.status_code}

#=========================================
#           _        _            
#  __ _ ___| |_   __| |__ _ ______
# / _` / -_)  _| / _| / _` (_-<_-<
# \__, \___|\__| \__|_\__,_/__/__/
# |___/                           
#=========================================
class get:
    def XCsrf(cookie):
        xcsrfRequest = session.post("https://auth.roblox.com/v2/logout", cookies={".ROBLOSECURITY": cookie})
        return xcsrfRequest.headers["x-csrf-token"]

    #Removing Duplicate Clothings
    def removeDuplicates(copiedClothingData):
        userGroupClothingLink = "https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorType=Group&IncludeNotForSale=false&Limit=30&CreatorTargetId=" + str(userGroupId)
        duplicates            = []

        while True:
            userGroupClothingRequest = session.get(userGroupClothingLink)
            userGroupClothingData    =  userGroupClothingRequest.json()
            checkRequest("USER-GROUP-CLOTHING", "GET", userGroupClothingRequest)

            for userClothing in userGroupClothingData["data"]:
                for copiedClothing in copiedClothingData:
                    if userClothing["name"] == copiedClothingData[copiedClothing]["Name"]:
                        copiedClothingData.pop(copiedClothing, None)
                        duplicates.append(userClothing["name"])
                        break

            #Gets All Clothings, Besides Just 30
            if userGroupClothingData["nextPageCursor"] == None:
                break
            else:
                userGroupClothingLink = "https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorType=Group&IncludeNotForSale=false&Limit=30&CreatorTargetId=" + str(userGroupId) + "&cursor=" + userGroupClothingData["nextPageCursor"]

        for duplicatedClothing in duplicates:
            cl(f"Deleted Duplicate: {duplicatedClothing}", "blue")

        return copiedClothingData

    def robux():
        robuxRequest     = session.get("https://economy.roblox.com/v1/user/currency")
        robuxRequestData = robuxRequest.json()
        robux            = robuxRequestData["robux"]
        return robux

    def projectClothing(assetId, amount): #Basically makes your clothing to the front page, the higher the amount, the longer it stays there
        if int(amount) > get.robux():
            ci("Amount is Higher Than Robux", "red", symbol="!")
            exit()

        deleteAssetRequest = session.post("https://www.roblox.com/asset/delete-from-inventory", data={"assetId": assetId})
        checkRequest("DELETE-ASSET", "POST", deleteAssetRequest)
        
        sleep(1)
        
        updatePriceRequest = session.post(f"https://itemconfiguration.roblox.com/v1/assets/{assetId}/update-price",
            headers = {"Content-Type": "application/json"},
            data    = json.dumps({"priceConfiguration": {"priceInRobux": str(amount)}})
        )
        checkRequest("UPDATE-PRICE", "POST", updatePriceRequest)

        clothingHTMLRequest = session.get(f"https://www.roblox.com/catalog/{assetId}")
        checkRequest("CLOTHING-PAGE-HTML", "GET", clothingHTMLRequest)

        clothingHTML     = BeautifulSoup(clothingHTMLRequest.text, "html.parser")
        itemContainer    = clothingHTML.find("div", {"id": "item-container"})
        expectedSellerID = itemContainer["data-expected-seller-id"]
        dataProductID    = itemContainer["data-product-id"]

        projectClothingRequest = session.post(
        f"https://economy.roblox.com/v1/purchases/products/{dataProductID}", 
            data={"expectedCurrency": "1", "expectedPrice": str(amount), "expectedSellerId": str(expectedSellerID)}
        )
        checkRequest("PROJECT-CLOTHING", "POST", projectClothingRequest)

    def uploadedClothings(displayOffsale):
        if displayOffsale.lower() in ["yes", "y"]:
            displayOffsale = True
        else:
            displayOffsale = False

        if displayOffsale:
            userGroupRequestURL = "https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorType=Group&IncludeNotForSale=true&Limit=30&CreatorTargetId=" + str(userGroupId)
        else:
            userGroupRequestURL = "https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorType=Group&IncludeNotForSale=false&Limit=30&CreatorTargetId=" + str(userGroupId)

        info = {}

        while True:
            userGroupRequest     = session.get(userGroupRequestURL)
            userGroupRequestData = userGroupRequest.json()
            checkRequest("USER-GROUP-CLOTHING", "GET", userGroupRequest)

            for i in userGroupRequestData["data"]:
                if displayOffsale:
                    try:
                        i["price"]
                    except KeyError: #There is only a KeyError for ["price"] if it's offsale, since for offsales, the api returns without a "price" index.
                        if i["assetType"] == 11:    
                            info[i["id"]] = {
                                "Name":        str(i["name"]),
                                "Type":        "Shirts",
                                "Description": i["description"]
                            }

                        elif i["assetType"] == 12:
                            info[i["id"]] = {
                                "Name":        str(i["name"]),
                                "Type":        "Pants",
                                "Description": i["description"]
                            }
                else:
                    if i["assetType"] == 11:    
                        info[i["id"]] = {
                            "Name":        str(i["name"]),
                            "Type":        "Shirts",
                            "Description": i["description"],
                            "Price":       i["price"]
                        }

                    elif i["assetType"] == 12:
                        info[i["id"]] = {
                            "Name":        str(i["name"]),
                            "Type":        "Pants",
                            "Description": i["description"],
                            "Price":       i["price"]
                        }

            #Gets All Clothings, Besides Just 30
            if userGroupRequestData["nextPageCursor"] == None:
                break
            else:
                userGroupRequestURL = "https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorType=Group&IncludeNotForSale=false&Limit=30&CreatorTargetId=" + str(userGroupId) + "&cursor=" + userGroupRequestData["nextPageCursor"]

        #Displaying Part
        nameAlignSpaces  = max(len(info[i]["Name"]) for i in info)
        typeAlignSpaces  = max(len(info[i]["Type"]) for i in info)
        if not displayOffsale:
            priceAlignSpaces = max(len(str(info[i]["Price"])) for i in info)

        for i in info:
            if displayOffsale:
                cl(f"{info[i]['Name']}{(nameAlignSpaces-len(info[i]['Name']))*' '} {Fore.WHITE}|{Fore.BLUE} Offsale {Fore.WHITE}|{Fore.BLUE} {info[i]['Type']}{(typeAlignSpaces-len(str(info[i]['Type'])))*' '} {Fore.WHITE}|{Fore.BLUE} https://www.roblox.com/catalog/{i}", "blue", symbol=str(i))
            else:
                cl(f"{info[i]['Name']}{(nameAlignSpaces-len(info[i]['Name']))*' '} {Fore.WHITE}|{Fore.BLUE} {info[i]['Price']} R${(priceAlignSpaces-len(str(info[i]['Price'])))*' '} {Fore.WHITE}|{Fore.BLUE} {info[i]['Type']}{(typeAlignSpaces-len(str(info[i]['Type'])))*' '} {Fore.WHITE}|{Fore.BLUE} https://www.roblox.com/catalog/{i}", "blue", symbol=str(i))

#=========================================
#                        _            
#  __ ___ _ __ _  _   __| |__ _ ______
# / _/ _ \ '_ \ || | / _| / _` (_-<_-<
# \__\___/ .__/\_, | \__|_\__,_/__/__/
#        |_|   |__/                   
#=========================================
class copy:
    def assetImg(assetId, type):
        with open(f"Storage/clothingPostData/{assetId}.png", "wb") as assetFile:
            assetFile.write(session.get(findall(r"<url>(.+?)(?=</url>)", session.get(f"https://assetdelivery.roblox.com/v1/asset?id={assetId}").text.replace("http://www.roblox.com/asset/?id=", "https://assetdelivery.roblox.com/v1/asset?id="))[0]).content)
            if templateChange:
                if str(type).lower() in ["shirts", "shirt", "11"]:
                    try:
                        clothingAsset    = Image.open(f"Storage/clothingPostData/{assetId}.png")
                    except:
                        cl(f"Skipping Asset ({assetId}, {type}), (Error Getting Asset Image)", "red", symbol="!")

                    clothingTemplate = Image.open("Storage/shirtTemplate.png")
                    clothingAsset.paste(clothingTemplate, (0,0), mask = clothingTemplate)
                    clothingAsset.save(f"Storage/clothingPostData/{assetId}.png")

                elif str(type).lower() in ["pants", "pant", "12"]:
                    try:
                        clothingAsset    = Image.open(f"Storage/clothingPostData/{assetId}.png")
                    except:
                        cl(f"Skipping Asset ({assetId}, {type}), (Error Getting Asset Image)", "red", symbol="!")

                    clothingTemplate = Image.open("Storage/pantTemplate.png")
                    clothingAsset.paste(clothingTemplate, (0,0), mask = clothingTemplate)
                    clothingAsset.save(f"Storage/clothingPostData/{assetId}.png")

        return f"Storage/clothingPostData/{assetId}.png"

    def singleClothing(assetId):
        canUpload = get.robux()/uploadFee >= 1

        if not canUpload:
            ci(f"You Cannot Upload Any Clothings, (Atleast {uploadFee} Robux Needed)", "red", symbol="!")
            exit()

        info = {}

        copiedClothingInfoRequest = session.post("https://catalog.roblox.com/v1/catalog/items/details", json = {"items": [{ "itemType": "Asset", "id": assetId}]})
        copiedClothingInfoData    = copiedClothingInfoRequest.json()
        checkRequest("CATALOG-CLOTHING-INFO", "GET", copiedClothingInfoRequest)

        info[int(assetId)] = {
            "Name":        copiedClothingInfoData["data"][0]["name"],
            "Type":        copiedClothingInfoData["data"][0]["assetType"],    
            "Description": copiedClothingInfoData["data"][0]["description"],
            "Price":       copiedClothingInfoData["data"][0]["price"]    
        }

        for i in info:
            if customClothingInfo:
                UploadGroupClothing(
                    assetId     = i,
                    type        = info[i]["Type"],
                    name        = info[i]["Name"],
                    description = userClothingDescription,
                    price       = userClothingPrice
                )
            else:
                UploadGroupClothing(
                    assetId     = i,
                    type        = info[i]["Type"],
                    name        = info[i]["Name"],
                    description = info[i]["Description"],
                    price       = info[i]["Price"]
                )

    def groups(copyGroupId, filter, amount):
        if str(filter).lower() in ["y", "yes"]:
            filter = True
        elif str(filter).lower() in ["n", "no"]:
            filter = False
        
        if amount == 0:
            amount = get.robux()/uploadFee
            if amount < 1:
                ci(f"You Cannot Upload Any Clothings, (Atleast {uploadFee} Robux Needed)", "red", symbol="!")
                exit()
        elif amount > get.robux()/uploadFee:
            ci(f"You Do Not Have Enough Robux ({get.robux()}) to Upload {amount} Clothes.", "red", symbol="!")
            exit()

        info              = {}
        groupClothingLink = "https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorType=Group&IncludeNotForSale=false&Limit=30&CreatorTargetId=" + str(copyGroupId)

        while True:
            copyGroupClothingRequest = session.get(groupClothingLink)
            groupClothings           = copyGroupClothingRequest.json()
            checkRequest("TARGET-GROUP-CLOTHING", "GET", copyGroupClothingRequest)

            for i in groupClothings["data"]:
                if len(info) == amount:
                    break

                if i["assetType"] == 11:    
                    info[i["id"]] = {
                        "Name":        str(i["name"]),
                        "Type":        "Shirts",
                        "Description": i["description"],
                        "Price":       i["price"]
                    }

                elif i["assetType"] == 12:
                    info[i["id"]] = {
                        "Name":        str(i["name"]),
                        "Type":        "Pants",
                        "Description": i["description"],
                        "Price":       i["price"]
                    }

            #Gets All Clothings, Besides Just 30
            if groupClothings["nextPageCursor"] == None or len(info) == amount:
                break
            else:
                groupClothingLink = "https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorType=Group&IncludeNotForSale=false&Limit=30&CreatorTargetId=" + str(copyGroupId) + "&cursor=" + groupClothings["nextPageCursor"]
        
        if filter:
            info = get.removeDuplicates(info)

        for i in info:
            if customClothingInfo:
                UploadGroupClothing(
                    assetId     = i,
                    type        = info[i]["Type"],
                    name        = info[i]["Name"],
                    description = userClothingDescription,
                    price       = userClothingPrice
                )
            else:
                UploadGroupClothing(
                    assetId     = i,
                    type        = info[i]["Type"],
                    name        = info[i]["Name"],
                    description = info[i]["Description"],
                    price       = info[i]["Price"]
                )

    def classicClothings(type, sort, keyword, amount, filter):
        if str(filter).lower() in ["y", "yes"]:
            filter = True
        elif str(filter).lower() in ["n", "no"]:
            filter = False
        
        if amount == 0:
            amount = get.robux()/uploadFee
            if amount < 1:
                ci(f"You Cannot Upload Any Clothings, (Atleast {uploadFee} Robux Needed)", "red", symbol="!")
                exit()
        elif amount > get.robux()/uploadFee:
            ci(f"You Do Not Have Enough Robux ({get.robux()}) to Upload {amount} Clothes.", "red", symbol="!")
            exit()

        sortedClothingList = {
            1: f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={keyword}&limit=120&salesTypeFilter=1&subcategory=Classic{type}",
            
            2: f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={keyword}&limit=120&salesTypeFilter=1&sortAggregation=5&sortType=1&subcategory=Classic{type}",
            3: f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={keyword}&limit=120&salesTypeFilter=1&sortAggregation=3&sortType=1&subcategory=Classic{type}",
            4: f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={keyword}&limit=120&salesTypeFilter=1&sortAggregation=1&sortType=1&subcategory=Classic{type}",
            
            5: f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={keyword}&limit=120&salesTypeFilter=1&sortAggregation=5&sortType=2&subcategory=Classic{type}",
            6: f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={keyword}&limit=120&salesTypeFilter=1&sortAggregation=3&sortType=2&subcategory=Classic{type}",
            7: f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={keyword}&limit=120&salesTypeFilter=1&sortAggregation=1&sortType=1&subcategory=Classic{type}",
            
            8: f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={keyword}&limit=120&salesTypeFilter=1&sortType=3&subcategory=Classic{type}"
        }

        info = {}
        sortedClothingRequestURL  = sortedClothingList[sort]
        
        while True:
            #GETTING THE CLOTHING PAGE INFO (FOR SCRAPING)
            sortedClothingRequest     = session.get(sortedClothingRequestURL)
            sortedClothingRequestData = sortedClothingRequest.json()
            checkRequest("CATALOG-CLOTHINGS", "GET", sortedClothingRequest)

            if sortedClothingRequestData["data"] == None:
                ci("Keyword has Been Censored, Restart Script", "red", "!")
                exit()

            for i in sortedClothingRequestData["data"]:
                if len(info) == amount:
                    break

                #GETTING THE CLOTHING INFO
                copiedClothingInfoRequest = session.post("https://catalog.roblox.com/v1/catalog/items/details", json = {"items": [{ "itemType": "Asset", "id": str(i["id"])}]})
                copiedClothingInfoData    = copiedClothingInfoRequest.json()
                checkRequest("CATALOG-CLOTHING-INFO", "GET", copiedClothingInfoRequest)
   
                info[copiedClothingInfoData["data"][0]["id"]] = {
                    "Name":        copiedClothingInfoData["data"][0]["name"],
                    "Type":        copiedClothingInfoData["data"][0]["assetType"],    
                    "Description": copiedClothingInfoData["data"][0]["description"],
                    "Price":       copiedClothingInfoData["data"][0]["price"]    
                }

            if sortedClothingRequestData["nextPageCursor"] == None or len(info) == amount:
                break
            else:
                sortedClothingRequestURL = sortedClothingList[sort] + "&cursor=" + sortedClothingRequestData["nextPageCursor"]

        if filter:
            info = get.removeDuplicates(info)

        for i in info:
            if customClothingInfo:
                UploadGroupClothing(
                    assetId     = i,
                    type        = info[i]["Type"],
                    name        = info[i]["Name"],
                    description = userClothingDescription,
                    price       = userClothingPrice
                )
            else:
                UploadGroupClothing(
                    assetId     = i,
                    type        = info[i]["Type"],
                    name        = info[i]["Name"],
                    description = info[i]["Description"],
                    price       = info[i]["Price"]
                )
  
#=========================================
#           _              _ _           
# _  _ _ __| |___  __ _ __| (_)_ _  __ _ 
#| || | '_ \ / _ \/ _` / _` | | ' \/ _` |
# \_,_| .__/_\___/\__,_\__,_|_|_||_\__, |
#      |_|                          |___/ 
#=========================================
def UploadGroupClothing(assetId, type, name, description, price):
    # WRITING ASSET DATA FOR POST REQUEST
    assetData = {
        "name":            name,
        "description":     description,
        "creatorTargetId": int(userGroupId),
        "creatorType":     "Group"
    }

    imgAssetPath = copy.assetImg(assetId, type)

    with open("Storage/clothingPostData/config.json", "w") as file:
        file.write(json.dumps(assetData, indent=4))

    #UPLOADING SHIRTS/PANTS
    if str(type).lower() in ["shirts", "shirt", "11"]:
        groupClothingPostRequest = session.post(
            "https://itemconfiguration.roblox.com/v1/avatar-assets/11/upload",
            files   = {name + ".png": open(imgAssetPath, "rb"), "config": open("Storage/clothingPostData/config.json", "rb")}
        )

    elif str(type).lower() in ["pants", "pant", "12"]:
        groupClothingPostRequest = session.post(
            "https://itemconfiguration.roblox.com/v1/avatar-assets/12/upload",
            files   = {name + ".png": open(imgAssetPath, "rb"), "config": open("Storage/clothingPostData/config.json", "rb")}
        )

    clothingUploadResults = checkRequest(f"CLOTHING-UPLOAD ({name})", "POST", groupClothingPostRequest)
    if not clothingUploadResults["success"] and clothingUploadResults["code"] == 429:
        sleep(rateLimitTimeout)
        UploadGroupClothing(
            assetId      = assetId,
            type         = type,
            name         = name,
            description  = description,
            price        = price
        )

    #RELEASING AND PRICING SHIRT/PANTS
    if groupClothingPostRequest.status_code == 200:
        uploadedAssetId = groupClothingPostRequest.json()["assetId"]
        groupClothingPricePostRequest = session.post(f"https://itemconfiguration.roblox.com/v1/assets/{uploadedAssetId}/release",
            headers = {"Content-Type": "application/json"},
            data    = json.dumps({"price": str(price), "priceConfiguration": {"priceInRobux": str(price)}, "saleStatus": "OnSale"})
        )
        checkRequest(f"CLOTHING-PRICING ({uploadedAssetId})", "POST", groupClothingPricePostRequest)

#=========================================       
#  _____ _____ __ _  _| |_ ___ 
# / -_) \ / -_) _| || |  _/ -_)
# \___/_\_\___\__|\_,_|\__\___|
#=========================================
def executeCommand(input):
    #What 0 or All means is that it will keep uploading until all the clothing is copied, for ex, all group's clothing. Or until there's no more robux left to upload.
    if input == 1:
        targetId = ci("Group Target ID: ", "blue")
        filter   = ci("(y/n) Filter Duplicates: ", "blue")
        amount   = ci("(0=All) Upload Amount: ", "blue")

        copy.groups(copyGroupId=targetId, filter=filter, amount=int(amount))

    elif input == 2:
        keyword  = ci("Keywords: ", "blue").strip().replace(" ", "+")
        print(clothingSortBox)
        sort     = ci("Sort: ", "blue")
        amount   = ci("(0=All) Upload Amount: ", "blue")
        filter   = ci("(y/n) Filter Duplicates: ", "blue")

        copy.classicClothings(type="Shirts", sort=int(sort), keyword=keyword, amount=int(amount), filter=filter)
    
    elif input == 3:
        keyword  = ci("Keywords: ", "blue").strip().replace(" ", "+")
        print(clothingSortBox)
        sort     = ci("Sort: ", "blue")
        amount   = ci("(0=All) Upload Amount: ", "blue")
        filter   = ci("(y/n) Filter Duplicates: ", "blue")

        copy.classicClothings(type="Pants", sort=int(sort), keyword=keyword, amount=int(amount), filter=filter)
    
    elif input == 4:
        assetId = ci("Asset ID: ", "blue")

        copy.singleClothing(assetId=assetId)

    elif input == 5:
        cl(f"R$: {get.robux()}", "blue")
    
    elif input == 6:
        offsale = ci("(y/n) Display Offsales Only: ", "blue")
        get.uploadedClothings(offsale)

    elif input == 7:
        clothingId = ci("Clothing ID: ", "blue")
        amount     = ci("Amount to Project: ", "blue")
        get.projectClothing(str(clothingId), str(amount))

    elif input == 8:
        os.system("cls")
        print(commandBox)

    elif input == 9:
        print(credits)

try:
    usernameRequest     = session.get("https://users.roblox.com/v1/users/authenticated")
    usernameRequestData = usernameRequest.json()
    username            = usernameRequestData['name']
    cl(f"Logged in as {username} | R$ {get.robux()}", "blue")
except Exception as err:
    ci(f"Your cookie is invalid, restart the program with a valid cookie", "red", symbol="!")
    exit()