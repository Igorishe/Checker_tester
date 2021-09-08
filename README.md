# MobChecker

Mobile proxy checker bot.

This Bot allows

1. Get list of mobile proxies from your account by API;
2. Check proxy availability status for all list or just in certain country;
3. Check single proxy from your account by its port;
4. Check every 5-minutes IP-address rotation;

**Important!**

*Bot parses proxylist from the certain web-service API. If you use another 
service API_functions won't work correctly, so you need your own solution.*

## Deploy MobChecker with Docker

**Important!** *Don't forget to create .env file in your project directory.* 

Env file includes:

* BOT_TOKEN - telegram bot token from BotFather;
* ALLOWED_USERS - telegram id whitelist for bot;
* PROXY_LOGIN - login to access proxy-server;
* PROXY_PASSWORD - password to access proxy-server;
* PROXY_HOST - proxy IP-address (for single proxy check);
* CHECK_URL=https://domain-for-check-request.com
* IPINFO_TOKEN - token for ipinfo.io;
* AUTH_ID - id for API authorization;
* AUTH_KEY - token for API authorization;
* API_HOST=https://api-endpoint-to-get-proxylist

In order to start you need to install docker on your server.

Then clone the project from Git-repository and build && run docker container:

Enter working directory:
`cd Checker_tester`

Clone project from GitHub:
`git pull https://github.com/Igorishe/Checker_tester.git`

Build docker container:
`docker build -t bot .` - here "bot" is your container name

Run docker container:
`docker run -it -d bot`

If you'd like to pause bot polling just stop the container:
`docker container stop 36d2189fb612` - here 36d2189fb612 is a container id, 
you can check your container id with `docker ps` command.