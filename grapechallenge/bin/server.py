# pip
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pathlib import Path
# local
from grapechallenge.bin.common.router import Router
from grapechallenge.endpoint import user, fruit, fruit_template, mission, template

# Load environment variables
load_dotenv()

app = FastAPI(title="Grape Challenge")

# Mount static files
BASE_PATH = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(BASE_PATH / "template")), name="static")
app.mount("/js", StaticFiles(directory=str(BASE_PATH / "template" / "js")), name="js")
app.mount("/components", StaticFiles(directory=str(BASE_PATH / "template" / "components")), name="components")
app.mount("/css", StaticFiles(directory=str(BASE_PATH / "template" / "css")), name="css")


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

Router(
    "/cells", ["GET"], user.get_cells
).register(app)

# Fruit
Router(
    "/fruit", ["POST"], fruit.post_fruit
).register(app)

Router(
    "/fruits/mine", ["GET"], fruit.get_my_fruits
).register(app)

Router(
    "/fruit/in-progress", ["GET"], fruit.get_my_in_progress_fruit
).register(app)

Router(
    "/fruits/completed/count", ["GET"], fruit.count_my_completed_fruits
).register(app)

Router(
    "/fruit/harvest", ["POST"], fruit.post_harvest_fruit
).register(app)

Router(
    "/fruits/cell", ["POST"], fruit.get_fruits_by_cell_with_template
).register(app)

# Fruit Template
Router(
    "/fruit-template", ["GET"], fruit_template.get_fruit_template
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