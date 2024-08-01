import keyboard        
import json
import easygui

''' 
users.json is formatted like so:
{
    "123123": {
        "name": "Sam",
        "signed_in": false
    },
    "234234": {
        "name": "Bob",
        "signed_in": true
    }
}

'''





def load_users() -> dict:
  with open('users.json', 'r') as infile:
    users = dict(json.load(infile))
  return users


def save_users(users: dict):
  with open("users.json", "w") as outfile:
    json.dump(users, outfile, indent=4)


def get_user(users: dict, id: int) -> dict | None:
  val = users.get(str(id))
  if val == None:
    return None
  else:
    return dict(val)
      
def validate_input(input: str) -> str | None:

  # Clean and validate input
  cleaned_input = str.strip(str.lower(input))
  if not str.isalnum(cleaned_input):
    return None
  else:
    return input
  
def toggle_user(users: dict, id: int) -> dict:
  signed_in = not bool(users[str(id)]["signed_in"])
  users[str(id)]["signed_in"] = signed_in
  if signed_in:
    print("Signed in!")
  else:
    print("Signed out")

  return users

  

def handle_given_id(users: dict, id: int) -> dict:
  user = get_user(users, id)
  if user == None:
    # New user
    add: bool = easygui.boolbox("User not found.  Add new user with this card?", "User not found", ("Add", "Cancel"), None, "Cancel", "Cancel")
    if add:
      name: str = str(easygui.enterbox("Enter the new user's username", "Add new user"))
      users[str(id)] = {
        "name": name,
        "signed_in": False
      }
      print("Added new user: " + name)
    else:
      print("Canceled adding new user")

  else:
    # Toggle user state
    users = toggle_user(users, id)

  return users


def handle_card_input(input: str):
  id = validate_input(input)
  users = load_users()
  users = handle_given_id(users, id)
  save_users(users)



input = list()


def on_key_press(event):
  print(event)
  char = str(event.name)
  if char == "enter" and len(input) > 0:
    print(input)
    handle_card_input(''.join(input))
    input.clear()
  elif char.isalnum() and len(char) <= 1:
    input.append(str(char))
  else:
    print(str(char) + " is an invalid character")



keyboard.on_press(on_key_press)



keyboard.wait()