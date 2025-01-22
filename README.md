Stream Hub Bot
A multi-platform bot that integrates with Discord, Twitch, YouTube, and other social media platforms. The bot provides live notifications, automated role management, and an easy-to-use web dashboard.

Table of Contents
Installation
Configuration
Running the Bot
Available Commands
Deploying with Docker
Troubleshooting
Installation
Prerequisites
Ensure you have the following installed:

Python 3.10+
Docker & Docker Compose (optional for deployment)
PostgreSQL or SQLite for database storage
Setup Steps
Clone the repository:

bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/stream_hub_bot.git
cd stream_hub_bot
Create and activate a virtual environment:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create an .env file to store API credentials:

bash
Copy
Edit
cp .env.example .env
nano .env
Configure the configs/user1.json file with your Discord bot token and other API keys.

Configuration
Edit the configs/user1.json file to include your credentials and bot settings:

json
Copy
Edit
{
  "discord": {
    "token": "YOUR_DISCORD_BOT_TOKEN",
    "prefix": "~",
    "guild_id": 123456789012345678
  },
  "twitch": {
    "client_id": "YOUR_TWITCH_CLIENT_ID",
    "oauth_token": "YOUR_TWITCH_OAUTH_TOKEN"
  },
  "youtube": {
    "api_key": "YOUR_YOUTUBE_API_KEY"
  }
}
Running the Bot
Option 1: Running Locally
Once everything is set up, start the bot with:

bash
Copy
Edit
python main_bot.py
You should see the following output:

arduino
Copy
Edit
📄 Loaded config: user1.json
✅ Bot is online and ready!
Option 2: Running with Docker
Ensure Docker is installed, then run:

bash
Copy
Edit
docker-compose up --build
Available Commands
General Commands
Command	Description
~ping	Check if the bot is online
~restart	Restart the bot
~shutdown	Shut down the bot
~addrole @user Role	Add a role to a user
Moderation Commands
Command	Description
~clear 5	Delete the last 5 messages
~ban @user	Ban a user from the server
Office Channel Commands
Command	Description
~createhouse HouseName @User	Create a voice channel with a key role
~givekey @User HouseName	Give access to a private channel
~takekey @User HouseName	Remove access from a private channel
Deploying with Docker
Make sure your .env file is configured correctly.

Start the services using:

bash
Copy
Edit
docker-compose up --build -d
Stop the services when needed:

bash
Copy
Edit
docker-compose down
Troubleshooting
Common Issues and Fixes
1. Bot Not Responding to Commands
Ensure the prefix is correct (~) in configs/user1.json.

Ensure the bot has the necessary permissions in the Discord server.

Check if the bot is running properly using:

bash
Copy
Edit
python main_bot.py --debug
2. Database Errors
Ensure the database (bot_data.db) exists and is not corrupted.
If using PostgreSQL, check connection credentials.
Run migrations if needed.
3. Docker Issues
Ensure Docker is running with:

bash
Copy
Edit
sudo systemctl start docker
Run the health check script manually to verify API connections:

bash
Copy
Edit
python health_check.py
4. Logging Issues
Ensure the logs directory exists (logs/bot.log).
If logs are missing, verify the logger configuration in logger.py.
Contributing
Contributions are welcome! To contribute:

Fork the repository.

Create a new feature branch:

bash
Copy
Edit
git checkout -b feature-name
Commit your changes and push the branch.

Submit a pull request for review.

License
This project is licensed under the MIT License.