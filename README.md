# ArxivAlerts

A small Python program which notifies you when your favourite authors submit articles to arxiv.org. When new articles are found, ArxivAlerts creates a pretty 
summary of the new publications which can be opened from a desktop notification.

## Requirements

- Python > 3
- libraries: beautifulsoup4, python3-gi

The program was written for linux and makes use of systemd. If you don't have systemd on your OS, you can still use the ArxivAlerts but you'll have to find 
another way to run the program periodically.

## Installation
The install scripts simply creates a systemd timer that executes the main program daily.

`$git clone https://github.com/robinplantey/ArxivAlerts.git`

`$cd ArxivAlerts`

`$chmod +x install`

`$./install`

## How to use

Simply add a line "last name, first name" the file "subscriptions.txt" for each author you'd like to get updates for.
