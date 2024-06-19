# author: Michael Hüppe
# date: 11.05.2024
# project: /trackBody.py

import argparse
import time

from bodyTracking_widget.resources.bodyTracker import BodyTracker

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script with headless option")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--camera_index", type=int, default=0, help="Camera Index value (default: 0)")
    args = parser.parse_args()
    args.headless = False
    if args.headless:
        bodyTracker = BodyTracker()
        bodyTracker.setTrackingVisibility(
            {"face": False,
             "rightHand": False,
             "leftHand": False,
             "body": False}
        )
        prompt = "Enter q to quit"
        response = input(prompt)
        while response.lower() != "q":
            response = input(prompt)
    else:
        from bodyTracking_widget.movement_detection import main

        main()
