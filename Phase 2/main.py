from flask import Flask, render_template, request
from navigation import build_map, dijkstra_nav, voice_navigation

app = Flask(__name__)

settings_data = {
    "emergency_contact_name": "Alex",
    "emergency_contact_phone": "555-123-4567",
    "preferred_voice": "Default",
    "language": "en-US"
}

building_map = build_map()

nav_info = {
    "current_location" : "Hallway 1",
    "destination": None,
    "route": [],
    "instructions" : [],
    "routeIndex": 0
}

@app.route("/")
def index():
    return render_template("index.html", settings_data=settings_data)

@app.route("/speechtotext")
def speechtotext():
    transcript = request.args.get("transcript", "")
    print("Received transcript:", transcript)

    nav_info["last_transcript"] = transcript

    return {"transcript": transcript}

@app.route("/navigate")
def navigate():
    start = request.args.get("start", nav_info["current_location"]) #sets the start location
    dest = request.args.get("destination",nav_info.get("last_transcript", "Room 103")) #gets the inputted destination (or defaults to Room 103)
    if dest: 
        dest = dest[0].upper() + dest[1:]

    distance, path = dijkstra_nav(building_map[start], building_map[dest]) #finds the shortest path
    route_script = voice_navigation(path) #makes the route script for TTS

    #sets various nav info
    nav_info["destination"] = dest
    nav_info["route"] = [n.name for n in path]
    nav_info["instructions"] = route_script
    nav_info["routeIndex"] = 0

    #returns relevant nav data to begin route
    return {
        "instructions": route_script,
        "route": nav_info["route"],
    }

@app.route("/move")
def move():
    direction = request.args.get("direction") #gets requested direction
    current_location = nav_info["current_location"] #gets current location
    current_node = building_map[current_location] #gets the current node

    #gets possible directional nodes
    route_map = {
        "forward": current_node.forward,
        "right": current_node.right,
        "back": current_node.back,
        "left": current_node.left,
    }

    #checks that there is a node the direction chosen
    edge = route_map.get(direction)
    if edge is None:
        return {"error": "No room or hallway that way!", "recalculate": False}

    distance, next_node = edge
    new_location = next_node.name
    nav_info["current_location"] = new_location

    #makes sure we are not out of bounds
    if nav_info["routeIndex"] + 1 < len(nav_info["route"]):
        expected_location = nav_info["route"][nav_info["routeIndex"] + 1] #gets the expected location after movement
    else:
        expected_location = None

    #this happens if they went the wrong direction AKA recalculates route
    if new_location != expected_location:
        distance, new_route = dijkstra_nav(next_node, building_map[nav_info["destination"]]) #gets new route from location
        instructions = voice_navigation(new_route) #gets new script for TTS

        #sets various nav info
        nav_info["route"] = [n.name for n in new_route]
        nav_info["instructions"] = instructions
        nav_info["routeIndex"] = 0

        #returns the data to the html to use for UI
        return {
            "recalculate": True,
            "instructions": instructions,
            "route": nav_info["route"]
        }

    #otherwise, the correct direction was chosen so we proceed as normal
    nav_info["routeIndex"] += 1

    #makes sure we aren't out of bounds
    if nav_info["routeIndex"] < len(nav_info["instructions"]):
        next_instruction = nav_info["instructions"][nav_info["routeIndex"]] #gets the next piece of the script
    else:
        next_instruction = "You have arrived at your destination." #if we are where we want to be, just alerts the user

    #sends info to html for UI
    return {
        "recalculate": False,
        "instructions": next_instruction,
        "route": nav_info["route"]
    }

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        settings_data["emergency_contact_name"] = request.form["emergency_contact_name"]
        settings_data["emergency_contact_phone"] = request.form["emergency_contact_phone"]
        settings_data["language"] = request.form["language"]
        settings_data["preferred_voice"] = request.form["preferred_voice"]
    return render_template("settings.html", settings_data=settings_data)

if __name__ == "__main__":
    app.run(debug=True)
