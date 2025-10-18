# pip
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
# local
from grapechallenge.bin.common.router import Router
from grapechallenge.endpoint import user, fruit, mission, template

# Load environment variables
load_dotenv()

app = FastAPI(title="Grape Challenge")


# #
# Routers

# Health
Router(
    "/health", ["GET"], lambda: {"status": "ok"}
).register(app)

# User
Router(
    "/user", ["POST"], user.post_user
).register(app)

Router(
    "/users", ["POST"], user.post_users
).register(app)

Router(
    "/login", ["POST"], user.post_login
).register(app)

Router(
    "/logout", ["POST"], user.post_logout
).register(app)

# Fruit
Router(
    "/fruit", ["POST"], fruit.post_fruit
).register(app)

Router(
    "/fruits/mine", ["GET"], fruit.get_mine_fruits
).register(app)

Router(
    "/fruit/in-progress", ["GET"], fruit.get_in_progressed_fruit
).register(app)

# Mission
Router(
    "/mission/complete", ["POST"], mission.post_mission
).register(app)

# Template
Router(
    "/", ["GET"], template.home_page
).register(app)

Router(
    "/home", ["GET"], template.home_page
).register(app)

Router(
    "/grove", ["GET"], template.grove_page
).register(app)

Router(
    "/login", ["GET"], template.login_page
).register(app)


# #
# main

if __name__ == "__main__":
    uvicorn.run(
        **{
            "app": "server:app",
            "host": "0.0.0.0",
            "port": 8000,
            "reload": True
        }
    )