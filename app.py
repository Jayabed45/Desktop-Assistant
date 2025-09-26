import pyttsx3
import os
import subprocess
import platform
import random
from datetime import datetime
import sys

class VoiceAssistant:
    def __init__(self):
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.8)
        
        # Check if voice input is available
        self.voice_input_available = self.check_voice_input()
        
        # Application mappings
        self.applications = self.setup_application_mappings()
        
        print("\n" + "="*60)
        print("VOICE ASSISTANT READY!")
        if self.voice_input_available:
            print("Mode: Voice Input Enabled")
        else:
            print("Mode: Text Input (Voice not available)")
        print("="*60)
    
    def check_voice_input(self):
        """Check if voice input dependencies are available"""
        try:
            import speech_recognition as sr
            # Try to initialize microphone
            try:
                microphone = sr.Microphone()
                recognizer = sr.Recognizer()
                with microphone as source:
                    recognizer.adjust_for_ambient_noise(source)
                return True
            except:
                return False
        except ImportError:
            return False
    
    def setup_application_mappings(self):
        """Setup application mappings based on operating system"""
        system = platform.system()
        
        if system == "Windows":
            return {
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'paint': 'mspaint.exe',
                'file explorer': 'explorer.exe',
                'command prompt': 'cmd.exe',
                'task manager': 'taskmgr.exe',
                'chrome': 'chrome.exe',
                'firefox': 'firefox.exe',
                'edge': 'msedge.exe',
                'word': 'winword.exe',
                'excel': 'excel.exe',
                'powerpoint': 'powerpnt.exe',
                'media player': 'wmplayer.exe',
                'photos': 'msphotos.exe',
                'settings': 'start ms-settings:',
                'control panel': 'control.exe',
                'paint': 'mspaint.exe'
            }
        elif system == "Darwin":  # macOS
            return {
                'safari': 'Safari',
                'chrome': 'Google Chrome',
                'firefox': 'Firefox',
                'calculator': 'Calculator',
                'calendar': 'Calendar',
                'messages': 'Messages',
                'mail': 'Mail',
                'photos': 'Photos',
                'music': 'Music',
                'notes': 'Notes',
                'textedit': 'TextEdit',
                'terminal': 'Terminal',
                'finder': 'Finder',
                'system preferences': 'System Preferences',
            }
        else:  # Linux
            return {
                'firefox': 'firefox',
                'chrome': 'google-chrome',
                'calculator': 'gnome-calculator',
                'file manager': 'nautilus',
                'text editor': 'gedit',
                'terminal': 'gnome-terminal',
                'media player': 'vlc',
            }
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen_voice(self):
        """Listen for voice input"""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            with microphone as source:
                print("🎤 Listening... (speak now)")
                self.speak("I'm listening")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            
            print("🔄 Processing...")
            text = recognizer.recognize_google(audio)
            print(f"👤 You said: {text}")
            return text.lower()
            
        except Exception as e:
            print(f"Voice recognition error: {e}")
            return ""
    
    def get_text_input(self):
        """Get input from text"""
        return input("👤 You (type): ").lower()
    
    def open_application(self, app_name):
        """Open an application based on command"""
        system = platform.system()
        app_name_lower = app_name.lower()
        
        # Find the best matching application
        matched_app = None
        for key in self.applications:
            if key in app_name_lower:
                matched_app = key
                break
        
        if matched_app:
            try:
                app_command = self.applications[matched_app]
                
                if system == "Windows":
                    if app_command.startswith('start '):
                        os.system(app_command)
                    else:
                        subprocess.Popen(app_command, shell=True)
                elif system == "Darwin":  # macOS
                    subprocess.Popen(['open', '-a', app_command])
                else:  # Linux
                    subprocess.Popen([app_command])
                
                return f"✅ Opening {matched_app}"
            except Exception as e:
                return f"❌ Sorry, I couldn't open {app_name}"
        else:
            # Try direct command
            try:
                if system == "Windows":
                    subprocess.Popen(app_name, shell=True)
                else:
                    subprocess.Popen([app_name])
                return f"🔧 Attempting to open {app_name}"
            except:
                return f"❌ I don't know how to open {app_name}"
    
    def open_file(self, filename):
        """Open a file from common directories"""
        system = platform.system()
        
        # Common directories to search
        search_dirs = [
            os.path.expanduser("~\\Desktop") if system == "Windows" else os.path.expanduser("~/Desktop"),
            os.path.expanduser("~\\Documents") if system == "Windows" else os.path.expanduser("~/Documents"),
            os.path.expanduser("~\\Downloads") if system == "Windows" else os.path.expanduser("~/Downloads")
        ]
        
        for search_dir in search_dirs:
            if os.path.exists(search_dir):
                for file in os.listdir(search_dir):
                    if filename.lower() in file.lower():
                        file_path = os.path.join(search_dir, file)
                        try:
                            if system == "Windows":
                                os.startfile(file_path)
                            elif system == "Darwin":
                                subprocess.Popen(['open', file_path])
                            else:
                                subprocess.Popen(['xdg-open', file_path])
                            return f"✅ Opening {file}"
                        except:
                            return f"❌ Found {file} but couldn't open it"
        
        return f"❌ Couldn't find a file named {filename}"
    
    def open_website(self, website):
        """Open a website in the default browser"""
        try:
            if not website.startswith(('http://', 'https://')):
                website = 'https://' + website
            
            system = platform.system()
            
            if system == "Windows":
                os.system(f'start {website}')
            elif system == "Darwin":
                subprocess.Popen(['open', website])
            else:
                subprocess.Popen(['xdg-open', website])
            
            return f"🌐 Opening {website}"
        except:
            return f"❌ Couldn't open the website"
    
    def get_time(self):
        """Get current time"""
        current_time = datetime.now().strftime("%I:%M %p")
        return f"🕒 The current time is {current_time}"
    
    def get_date(self):
        """Get current date"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"📅 Today is {current_date}"
    
    def list_applications(self):
        """List available applications"""
        app_list = "\n".join([f"   • {app}" for app in self.applications.keys()])
        return f"📋 Available applications:\n{app_list}"
    
    def show_help(self):
        """Show help information"""
        help_text = """
🤖 VOICE ASSISTANT HELP:

🎯 APPLICATION COMMANDS:
   • 'open [application]' - Open an app (e.g., 'open calculator')
   • 'open file [name]' - Open a file (e.g., 'open file document')
   • 'open website [url]' - Open a website (e.g., 'open website google.com')
   • 'list applications' - Show all available apps

📅 INFORMATION COMMANDS:
   • 'time' - Current time
   • 'date' - Today's date
   • 'help' - Show this help

💬 GENERAL COMMANDS:
   • 'hello' - Greeting
   • 'how are you' - Check status
   • 'exit' or 'quit' - Close assistant

💡 TIP: You can say 'open notepad' or 'open calculator' to test!
        """
        return help_text
    
    def process_command(self, command):
        """Process the command and generate a response"""
        if not command:
            return "I didn't catch that. Could you please repeat?"
        
        command = command.lower()
        
        # Open commands
        if any(word in command for word in ["open", "launch", "start"]):
            if "website" in command:
                words = command.split()
                for word in words:
                    if '.' in word and any(ext in word for ext in ['.com', '.org', '.net', '.io']):
                        return self.open_website(word)
                return "Please specify which website you want to open."
            
            elif "file" in command:
                words = command.split()
                if "file" in words:
                    file_index = words.index("file")
                    if file_index + 1 < len(words):
                        filename = " ".join(words[file_index + 1:])
                        return self.open_file(filename)
                return "Please specify which file you want to open."
            
            else:
                words = command.split()
                for keyword in ["open", "launch", "start"]:
                    if keyword in words:
                        keyword_index = words.index(keyword)
                        if keyword_index + 1 < len(words):
                            app_name = " ".join(words[keyword_index + 1:])
                            return self.open_application(app_name)
                return "Please specify what you want to open."
        
        # Information commands
        elif "time" in command:
            return self.get_time()
        
        elif "date" in command:
            return self.get_date()
        
        elif "list" in command and "application" in command:
            return self.list_applications()
        
        # Greetings
        elif any(word in command for word in ["hello", "hi", "hey"]):
            return random.choice(["Hello! How can I help you?", "Hi there!", "Hey! What can I do for you?"])
        
        elif "how are you" in command:
            return random.choice(["I'm doing well, thank you!", "I'm great! How are you?", "All systems working perfectly!"])
        
        elif "thank you" in command or "thanks" in command:
            return random.choice(["You're welcome!", "My pleasure!", "Anytime!"])
        
        elif any(word in command for word in ["bye", "goodbye", "exit", "quit"]):
            return "exit"
        
        elif "help" in command:
            return self.show_help()
        
        else:
            return random.choice([
                "I can open applications or files for you. Try 'open calculator' or 'help' for more options.",
                "Say 'help' to see what I can do!",
                "Try saying 'open notepad' or 'what time is it?'"
            ])
    
    def run(self):
        """Main loop for the voice assistant"""
        self.speak("Hello! I'm your voice assistant. Say 'help' to see what I can do!")
        
        while True:
            # Get input based on availability
            if self.voice_input_available:
                command = self.listen_voice()
                if not command:  # If voice recognition failed, fall back to text
                    self.speak("I didn't catch that. Please type your command.")
                    command = self.get_text_input()
            else:
                command = self.get_text_input()
            
            if command:
                response = self.process_command(command)
                
                if response == "exit":
                    self.speak("Goodbye! Have a great day!")
                    break
                
                if response:
                    self.speak(response)

def install_dependencies():
    """Install required dependencies"""
    print("🔧 Checking dependencies...")
    
    # Check if pyttsx3 is installed
    try:
        import pyttsx3
        print("✅ pyttsx3 is installed")
    except ImportError:
        print("📦 Installing pyttsx3...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyttsx3"])
    
    # Check if speech_recognition is installed
    try:
        import speech_recognition
        print("✅ speech_recognition is installed")
    except ImportError:
        print("📦 Installing speech_recognition...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "SpeechRecognition"])
    
    # Try to install PyAudio
    try:
        import pyaudio # pyright: ignore[reportMissingModuleSource]
        print("✅ PyAudio is installed")
    except ImportError:
        print("⚠️  PyAudio not installed - voice input may not work")
        print("💡 You can still use text input mode")

if __name__ == "__main__":
    print("🚀 Voice Assistant Starting...")
    
    # Install dependencies
    install_dependencies()
    
    # Create and run assistant
    assistant = VoiceAssistant()
    assistant.run()