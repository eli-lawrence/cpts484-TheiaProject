# User Manual - Theia Blind Assistance App

Welcome to the Theia Blind Assistance Application. This guide will help you understand how to use the application's features for indoor navigation, safety monitoring, and customization.

## 1. Getting Started

1.  Ensure the application is running (refer to `README.md` for technical setup).
2.  Open your web browser and navigate to `http://127.0.0.1:5000`.
3.  You will see the main dashboard with options for Navigation, Manual Movement, and Fall Detection.

## 2. Voice Navigation

The primary way to interact with the app is through voice commands.

### How to Start
1.  Click the **"Start Voice Command"** button on the dashboard.
2.  Wait for the app to say **"Listening"**.
3.  Speak your command clearly.

### Navigation Commands
*   **"Room [Number]"**: Sets the destination to a specific room.
    *   *Example:* "Room 103"
*   **"Hallway [Number]"**: Sets the destination to a specific hallway.
    *   *Example:* "Hallway 1" or "Hallway One"

Once a destination is set, the app will read out the first instruction (e.g., "Go forward 50 feet to Hallway 2").

### Other Voice Commands
*   **"Open settings"**: Navigates to the settings page.
*   **"Help I've fallen"** (or similar phrases): Immediately triggers the fall detection simulation.

## 3. Manual Navigation Controls

If you are testing without voice or need to correct your location manually, you can use the **Manual Movement** buttons.

*   **Forward / Back / Left / Right**: Press these buttons to move your virtual location in the app.
*   **Recalculation**: If you move off the planned path (e.g., turn wrong), the app will automatically recalculate the route and read the new instructions.

## 4. Fall Detection & Safety

The application includes a fall detection system that can be triggered manually or by voice.

### Triggering Fall Detection
*   **Voice:** Say "Help I've fallen" after clicking "Start Voice Command".
*   **Button:** Click the red **"Simulate Fall"** button on the dashboard.

### What Happens Next?
1.  The app will announce: *"I detected a fall. Are you okay?"*
2.  A **20-second countdown** begins.
3.  The app listens for your response.

### Responding to the Alert
*   **If you are OK:**
    *   Say **"Yes"** or **"Okay"** clearly.
    *   OR Click the **"I'm OK"** button that appears on the screen.
    *   *Result:* The alert is cancelled, and the app says "Okay, thank you."
*   **If you do NOT respond:**
    *   After 20 seconds, the app simulates an emergency call.
    *   It announces: *"No response detected. Calling your emergency contact."*

### Resetting After an Emergency Call
After an emergency call is simulated, a **"Person is OK Now"** button will appear. Click this to reset the system and return to normal operation.

## 5. Companion Settings

You can customize the application to fit your needs. Click the **"Companion Settings"** link at the top of the home page or say "Open settings".

### Configurable Options
*   **Emergency Contact Name:** The name of the person to contact in an emergency.
*   **Emergency Contact Phone:** The phone number to dial.
*   **Language:** Choose between English (US) and English (UK).
*   **Preferred Voice:** (Text field) Specify a preferred voice name for the speech synthesizer (browser dependent).

Click **"Save"** to apply your changes.
