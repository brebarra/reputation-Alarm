# Reputation Alarm

A Raspberry Pi project to scan Taylor Swift's Instagram feed for the word "reputation", triggering a flashing LED when "reputation (Taylor's Version)" is announced.

This was designed as a personal project and may require modification for other hardware setups or RSS feeds.

# Requirements

- Raspberry Pi Zero W, modified with USB-C for power
- Python 3
- pigpiod enabled/running
- RGB LED connected to the specified GPIO pins
- Custom RSS.app JSON feed

# Features

- Checks the RSS feed every 5 minutes for a balance between frequent polling and avoiding unnecessary requests
- LED flashing patterns alternating between green/white and red/white
- Debug printing to console
- Generic `.3mf` file for printing a two-tone case (+ white eye) to hold the modified Raspberry Pi and LED
- Printable sticker for the front of the case

# Installation

```
git clone https://github.com/brebarra/reputation-alarm.git
cd reputation-alarm
pip install -r requirements.txt
sudo systemctl start pigpiod
```

# Future Improvements

The code currently rechecks all Instagram posts in the RSS feed, regardless of whether they are new or not. It may be more efficient to store the last-seen post and only run the full scan when a new post appears.