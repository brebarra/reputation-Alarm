import requests
import time
import pigpio

json_url = "YOUR_RSS_FEED"
confirmed = 0

RED_PIN = 13
GREEN_PIN = 12
BLUE_PIN = 19
pi = pigpio.pi()

# Colour definitions in RGB format
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def repCheck():
    global confirmed
    
    try:
        response = requests.get(json_url)
        response.raise_for_status()  # Error if fails
        data = response.json()

        for post in data.get("items", []):  # Get posts from JSON
            title = post.get("title", "").lower()
            summary = post.get("content_text", "").lower() 
            link = post.get("url", "")

            if "reputation" in title or "reputation" in summary:
                print(f"REPUTATION TV CONFIRMED")
                print(f"Post: {link}")

                confirmed = 1
                
                return  # Ends

        print("No mention yet.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON: {e}")


    
def fadeColour(start_rgb, end_rgb, duration=2.0, steps=50):
        step_time = duration / steps
        for i in range(steps + 1):
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (i / steps))
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (i / steps))
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (i / steps))

            pi.set_PWM_dutycycle(RED_PIN, r)
            pi.set_PWM_dutycycle(GREEN_PIN, g)
            pi.set_PWM_dutycycle(BLUE_PIN, b)

            time.sleep(step_time)

def soundTheAlarm():
    try:
        cycleCount = 0 #resetting the cycle every 15 seconds)

        while True:
            fadeColour(WHITE, GREEN, duration=3)
            fadeColour(GREEN, WHITE, duration=3)
        
            cycleCount += 1

            if cycleCount >= 5:
                fadeColour(WHITE, RED, duration=1.5)
                time.sleep(1)
                fadeColour(RED, WHITE, duration=1.5)
                cycleCount = 0

    except KeyboardInterrupt:
        print("\nGoodbye!\n")
        pi.set_PWM_dutycycle(RED_PIN, 0)
        pi.set_PWM_dutycycle(GREEN_PIN, 0)
        pi.set_PWM_dutycycle(BLUE_PIN, 0)
        pi.stop()


while True:
    repCheck()
    if confirmed == 1:
        soundTheAlarm()
        break
    time.sleep(300) # Check every 5 mins
   