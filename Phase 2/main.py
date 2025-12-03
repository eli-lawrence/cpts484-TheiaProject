from flask import Flask, render_template_string, request

app = Flask(__name__)

settings_data = {
    "emergency_contact_name": "Alex",
    "emergency_contact_phone": "555-123-4567",
    "preferred_voice": "Default",
    "language": "en-US"
}

INDEX_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Blind Assistance App</title>
  <style>
    body {
      font-family: sans-serif;
      background: #111;
      color: #f5f5f5;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 2rem 1rem 4rem;
    }
    h1, h2 { text-align: center; }
    .container { max-width: 700px; width: 100%; }
    .card {
      background: #222;
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 0 12px rgba(0,0,0,0.4);
    }
    .btn {
      display: inline-block;
      padding: 1rem 1.5rem;
      margin: 0.25rem 0;
      font-size: 1.1rem;
      border-radius: 999px;
      border: none;
      cursor: pointer;
      width: 100%;
    }
    .btn-primary { background: #2d8cff; color: #fff; }
    .btn-secondary { background: #444; color: #fff; }
    .btn-danger { background: #ff4b4b; color: #fff; }
    a { color: #2d8cff; }
    .status {
      margin-top: 1rem;
      padding: 1rem;
      background: #000;
      border-radius: 8px;
      min-height: 3rem;
    }
    .countdown { font-weight: bold; margin-top: 0.5rem; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Blind Assistance App</h1>
    <p style="text-align:center;">
      <a href="{{ url_for('settings') }}">Companion Settings</a>
    </p>

    <div class="card">
      <h2>Verbal Directions</h2>
      <button class="btn btn-primary" onclick="speakDirections()">
        Play Directions
      </button>
    </div>

    <div class="card">
      <h2>Fall Detection</h2>
      <button id="fallButton" class="btn btn-danger" onclick="startFallDetection()">
        Simulate Fall
      </button>

      <button id="okButton" class="btn btn-secondary" onclick="markUserOkay()" style="display:none;">
        I'm OK
      </button>

      <button id="okAfterCallButton" class="btn btn-secondary" onclick="resetAfterCall()" style="display:none;">
        Person is OK Now
      </button>

      <div id="status" class="status" aria-live="polite"></div>
      <div id="countdown" class="countdown"></div>
    </div>
  </div>

<script>
    function speak(text)
    {
        if (!("speechSynthesis" in window))
        {
            return;
        }

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "{{ settings_data['language'] }}";
        window.speechSynthesis.speak(utterance);
    }

    function speakDirections()
    {
        const msg = "testing";
        speak(msg);
        setStatus("Speaking directions...");
    }

    let fallActive = false;
    let countdownTimer = null;
    let secondsLeft = 0;

    function setStatus(text)
    {
        document.getElementById("status").textContent = text;
    }

    function setCountdown(text)
    {
        document.getElementById("countdown").textContent = text || "";
    }

    function startFallDetection()
    {
        if (fallActive)
        {
            return;
        }

        fallActive = true;
        secondsLeft = 10;

        showDuringCountdownButtons();
        setStatus("I detected a possible fall. Are you okay?");
        setCountdown("Respond within: " + secondsLeft + " s");

        speak("I detected a fall. Are you okay?");

        if (countdownTimer)
        {
            clearInterval(countdownTimer);
        }

        countdownTimer = setInterval(function()
        {
            secondsLeft--;

            if (secondsLeft <= 0)
            {
                clearInterval(countdownTimer);
                triggerEmergencyContact();
            }
            else
            {
                setCountdown("Respond within: " + secondsLeft + " s");
            }
        }, 1000);
    }

    function showDuringCountdownButtons()
    {
        document.getElementById("okButton").style.display = "block";
        document.getElementById("okAfterCallButton").style.display = "none";
    }

    function showAfterCallButtons()
    {
        document.getElementById("okButton").style.display = "none";
        document.getElementById("okAfterCallButton").style.display = "block";
    }

    function resetButtons()
    {
        document.getElementById("okButton").style.display = "none";
        document.getElementById("okAfterCallButton").style.display = "none";
    }

    function markUserOkay()
    {
        fallActive = false;

        if (countdownTimer)
        {
            clearInterval(countdownTimer);
        }

        setCountdown("");
        resetButtons();
        setStatus("User marked OK.");
        speak("Okay, thank you.");
    }

    function triggerEmergencyContact()
    {
        setCountdown("");
        showAfterCallButtons();
        setStatus("No response detected. Calling emergency contact.");
        speak("No response detected. Calling your emergency contact.");
    }

    function resetAfterCall()
    {
        fallActive = false;
        setStatus("Status cleared.");
        setCountdown("");
        resetButtons();
    }
</script>

</body>
</html>
"""

SETTINGS_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Companion Settings</title>
  <style>
    body {
      font-family: sans-serif;
      background: #111;
      color: #f5f5f5;
      display: flex;
      justify-content: center;
      padding: 2rem 1rem 4rem;
    }
    .card {
      background: #222;
      border-radius: 12px;
      padding: 1.5rem 2rem;
      max-width: 600px;
      width: 100%;
      box-shadow: 0 0 12px rgba(0,0,0,0.4);
    }
    h1 { text-align: center; }
    label {
      display: block;
      margin-top: 1rem;
      font-weight: bold;
    }
    input, select {
      width: 100%;
      padding: 0.5rem;
      margin-top: 0.25rem;
      border-radius: 6px;
      border: 1px solid #444;
      background: #111;
      color: #fff;
    }
    .btn {
      padding: 0.75rem 1.5rem;
      margin-top: 1.5rem;
      border-radius: 999px;
      border: none;
      cursor: pointer;
      background: #2d8cff;
      color: #fff;
      width: 100%;
    }
    a { color: #2d8cff; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Companion Settings</h1>
    <p style="text-align:center;">
      <a href="{{ url_for('index') }}">Back</a>
    </p>

    <form method="post">
      <label for="emergency_contact_name">Emergency Contact Name</label>
      <input id="emergency_contact_name" name="emergency_contact_name"
             value="{{ settings_data['emergency_contact_name'] }}">

      <label for="emergency_contact_phone">Emergency Contact Phone</label>
      <input id="emergency_contact_phone" name="emergency_contact_phone"
             value="{{ settings_data['emergency_contact_phone'] }}">

      <label for="language">Language</label>
      <select id="language" name="language">
        <option value="en-US" {% if settings_data['language']=="en-US" %}selected{% endif %}>English (US)</option>
        <option value="en-GB" {% if settings_data['language']=="en-GB" %}selected{% endif %}>English (UK)</option>
      </select>

      <label for="preferred_voice">Preferred Voice</label>
      <input id="preferred_voice" name="preferred_voice"
             value="{{ settings_data['preferred_voice'] }}">

      <button class="btn" type="submit">Save</button>
    </form>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_TEMPLATE, settings_data=settings_data)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        settings_data["emergency_contact_name"] = request.form["emergency_contact_name"]
        settings_data["emergency_contact_phone"] = request.form["emergency_contact_phone"]
        settings_data["language"] = request.form["language"]
        settings_data["preferred_voice"] = request.form["preferred_voice"]
    return render_template_string(SETTINGS_TEMPLATE, settings_data=settings_data)

if __name__ == "__main__":
    app.run(debug=True)
