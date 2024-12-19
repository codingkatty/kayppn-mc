# Minecraft Telegram Bot 🤖
A Telegram bot made to solve frequent issues in my Minecraft server group chat with friends, on Telegram. It can be easily added to a group chat on Telegram.

Bot username: [@kayppnmcserver_bot](https://t.me/kayppnmcserver_bot)

The bot provides solutions to issues such as:
- Quick solution to check server status (online/offline)
- Quick access to coordinates
- Flexible and can configure any artenos server

To try it yourself, you can simply messsage @kayppnmcserver_bot (the bot) on Telegram.

## Commands and Functions ⚙️
You can use /help to get a series of commands.

1. **/setserver** <br>
Use `/setserver <address>` to configure a server address for the check status command. This allows flexibility for others to check their own server instead of a preset one.

> Right now, it is only limited to Artenos servers. This is because our server is hosted on Artenos and the API we're using to get status has a rather weird unfixable bug towards Artenos servers. We will continue to make it better by supporting other server types.

2. **/mcstatus** <br>
Use `/mcstatus` to get the status of server, whether is online or offline. It has 3 random responses for online/offline (totaling 6). Example responses are:
- "CHAT ITS ONLINE GOGOGO!!"
- "Your life is on the line."
- "Line up in queue."

When server is offline:
- "Server Offline 🥲"
- "Server is ded."
- "Nope not the time yet."

3. **/setcoords** <br>
Use `/setcoords <x> <z> <remark>` to store a set of coordinates in the database. It is chat specific and you can store many of them. It is useful to store coordinates to important places such as mines, fortress and bases (etc) for easy and fast access.

4. **/getcoords** <br>
Use `/getcoords` to get a list of coordinates.

## Tech Stack 📚
![HTML](https://img.shields.io/badge/HTML-orange?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-blue?style=for-the-badge&logo=css3&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telegram API](https://img.shields.io/badge/Telegram%20Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)

## Future Additions ✨
More user friendly features to edit/delete set content.