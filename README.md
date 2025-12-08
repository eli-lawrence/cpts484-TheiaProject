# CPTS 484 - Theia Project

This repository contains the software project for CPTS 484, a blind assistance application.

## Description

The Theia Project is a web-based application designed to assist visually impaired individuals with indoor navigation and safety. It provides turn-by-turn voice navigation, fall detection, and user-configurable settings.

## Features

*   **Indoor Navigation:** Utilizes a pre-defined map of an indoor space to provide the shortest route to a destination.
*   **Voice-guided Instructions:** Delivers clear, spoken directions for each step of the route.
*   **Voice Commands:** Allows users to control the application using voice inputs. Supported commands include:
    *   "Open settings": Navigates to the settings page.
    *   "Help I've fallen": Manually triggers the fall detection simulation.
    *   "Room [Number]": Sets the navigation destination (e.g., "Room 103").
    *   "Hallway [Number]": Sets the navigation destination to a hallway (e.g., "Hallway 1"). Supports both digits and spoken numbers (e.g., "Hallway One").
    *   "Yes/Okay": Confirms safety during a fall detection alert.
*   **Fall Detection (Simulation):** Simulates a fall detection event. If the user does not respond to voice prompts within a set time, it simulates alerting an emergency contact. Includes continuous listening for user response.
*   **Customizable Settings:** Allows users to configure an emergency contact, preferred language, and voice options.

## Bug Fixes & Improvements

*   **Self-Triggering Prevention:** Fixed a critical issue where the application would hear its own voice prompts (e.g., "Are you okay?") and falsely trigger commands. The app now waits for speech synthesis to complete before activating the microphone.
*   **Improved 'OK' Detection:** Implemented strict word boundary checks to prevent false positives. Phrases like "broken" or "looking" no longer trigger the "I'm OK" response; only distinct "yes", "ok", or "okay" inputs are accepted.
*   **Enhanced Navigation Input:** Added logic to strip trailing punctuation from voice inputs (e.g., "Room 101.") to prevent navigation errors.
*   **Visual Feedback:** Added immediate visual feedback in the status box when manual movement buttons are pressed.

## Getting Started

### Prerequisites

*   Python 3
*   Flask

### Running the Application

1.  Navigate to the `Phase 2` directory.
2.  Install the required dependencies:
    ```
    pip install Flask
    ```
3.  Run the application:
    ```
    python main.py
    ```
4.  Open a web browser and go to `http://127.0.0.1:5000`.

## File Structure

*   `Phase 2/main.py`: The main Flask application file. It handles routing, navigation logic, and communication with the frontend.
*   `Phase 2/navigation.py`: Contains the core navigation logic, including the Dijkstra algorithm for finding the shortest path and building the map.
*   `Phase 2/Templates/index.html`: The main user interface of the application. It includes controls for starting navigation, manual movement, and simulating fall detection.
*   `Phase 2/Templates/settings.html`: The settings page where users can configure their preferences.
*   `Phase 2/Documents/`: Contains all the Phase II documentation.
