# Jarvis - Advanced Voice Assistant

An intelligent voice-controlled assistant built with Python that can perform various tasks through voice commands.

## Features

### Core Functionality
- **Voice Recognition**: Understands natural speech commands
- **Text-to-Speech**: Responds with clear voice output
- **Time & Date**: Get current time and date
- **Weather Information**: Get weather for any city (requires API key)
- **News Updates**: Get top news headlines (requires API key)

### Productivity
- **Reminders**: Set timed reminders (minutes/hours)
- **Timers**: Set countdown timers
- **Notes**: Take and read notes
- **Calculations**: Perform mathematical calculations
- **File Operations**: Open files and applications
- **System Control**: Shutdown, restart, lock, sleep computer

### Information & Entertainment
- **Web Search**: Search Google for information
- **Jokes**: Tell random jokes
- **Application Launcher**: Open various applications
- **File Search**: Search for files on your computer
- **System Information**: Get OS details

## Setup

1. **Install Dependencies**:
   ```bash
   pip install speechrecognition pyttsx3 requests pypiwin32
   ```

2. **Configure API Keys**:
   - Get OpenWeatherMap API key from: https://openweathermap.org/api
   - Get News API key from: https://newsapi.org/
   - Edit `jarvis_config.json` and replace the placeholder values

3. **Run the Assistant**:
   ```bash
   python jarvis.py
   ```

## Voice Commands

### Basic Commands
- "Hello" or "Hi" - Greeting
- "What time is it" - Current time
- "What's the date" - Current date
- "Help" - List available commands

### Weather & News
- "Weather in [city]" - Get weather information
- "Get news" or "News" - Get top headlines

### Productivity
- "Remind me in 5 minutes to [message]" - Set reminder
- "Set timer for 10 minutes" - Set countdown timer
- "Take a note [text]" - Save a note
- "Read notes" - Read saved notes
- "Calculate 2 + 2" - Perform calculation

### Applications
- "Open calculator" - Open Windows Calculator
- "Open chrome" - Open Google Chrome
- "Open word" - Open Microsoft Word
- "Open file explorer" - Open File Explorer

### System Control
- "Shutdown" - Shutdown computer (30 second delay)
- "Restart" - Restart computer (30 second delay)
- "Cancel shutdown" - Cancel pending shutdown/restart
- "Lock computer" - Lock the workstation
- "Sleep" - Put computer to sleep
- "System info" - Get OS information

### Search & Entertainment
- "Search google for [query]" - Web search
- "Search files for [filename]" - Search local files
- "Tell me a joke" - Random joke
- "Exit" or "Bye" - Quit the assistant

## Configuration

Edit `jarvis_config.json` to customize:
- API keys for weather and news
- File paths for notes and reminders
- Other settings

## Requirements

- Python 3.6+
- Windows OS (some system commands are Windows-specific)
- Internet connection for weather/news features
- Microphone for voice input
- Speakers/headphones for voice output

## Troubleshooting

- **API not working**: Check your API keys in `jarvis_config.json`
- **Voice not recognized**: Ensure microphone is working and not muted
- **System commands fail**: Some commands require administrator privileges
- **Import errors**: Install missing dependencies with pip

## Future Enhancements

- Multi-language support
- Smart home integration
- Email and messaging
- Calendar integration
- Music control
- Advanced AI conversations
- GUI interface
- Mobile app companion