import massupload as mu
from colorama import init
from ezstyle import ci, commandBox
init(convert=True)
print(commandBox)

while True:
    opt = ci(f"", "blue")
    if opt == '1':              #[1] Copy Group       - (Testing Before Done)
        mu.executeCommand(1)
    elif opt == '2':            #[2] Copy Shirts      - (Testing Before Done)
        mu.executeCommand(2)
    elif opt == '3':            #[3] Copy Pants       - (Testing Before Done)
        mu.executeCommand(3)
    elif opt == '4':            #[4] Copy a Clothing  - Done
        mu.executeCommand(4)
    elif opt == '5':            #[5] Display Robux    - Done
        mu.executeCommand(5)
    elif opt == '6':            #[6] Display Uploaded - Done
        mu.executeCommand(6)
    elif opt == '7':            #[7] Project Clothing - Done
        mu.executeCommand(7)
    elif opt == '8':            #[8] Refresh          - Done
        mu.executeCommand(8)
    elif opt == '9':            #[9] Credits          - Done    
        mu.executeCommand(9)