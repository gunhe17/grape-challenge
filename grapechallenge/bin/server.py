# pip
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pathlib import Path
# local
from grapechallenge.bin.common.router import Router
from grapechallenge.endpoint import (
    user, fruit, fruit_template, mission, mission_template, template, bible
)

# Load environment variables
load_dotenv()

app = FastAPI(title="Grape Challenge")

# Mount static files
BASE_PATH = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(BASE_PATH / "template")), name="static")
app.mount("/js", StaticFiles(directory=str(BASE_PATH / "template" / "js")), name="js")
app.mount("/components", StaticFiles(directory=str(BASE_PATH / "template" / "components")), name="components")
app.mount("/css", StaticFiles(directory=str(BASE_PATH / "template" / "css")), name="css")
app.mount("/images", StaticFiles(directory=str(BASE_PATH / "template" / "images")), name="images")
app.mount("/favicon", StaticFiles(directory=str(BASE_PATH / "template" / "favicon")), name="favicon")


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

Router(
    "/users/count", ["GET"], user.get_user_count
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

Router(
    "/fruits/count", ["GET"], fruit.get_fruit_count
).register(app)

Router(
    "/fruits/stats/by-template", ["GET"], fruit.get_fruit_stats_by_template
).register(app)

# Fruit Template
Router(
    "/fruit-template", ["GET"], fruit_template.get_fruit_template
).register(app)

# Mission
Router(
    "/mission", ["GET"], mission.get_missions
).register(app)

Router(
    "/mission/complete", ["POST"], mission.post_mission
).register(app)

Router(
    "/mission/test", ["POST"], mission.post_test_mission
).register(app)

Router(
    "/mission/interaction", ["PATCH"], mission.post_interaction
).register(app)

Router(
    "/mission/report/daily", ["GET"], mission.get_daily_mission_report
).register(app)

Router(
    "/mission/event/in-progress", ["GET"], mission.get_event_missions
).register(app)

Router(
    "/mission/event/complete", ["POST"], mission.post_event_mission
).register(app)

# Mission Template
Router(
    "/mission-templates", ["GET"], mission_template.get_every_mission_template
).register(app)

Router(
    "/mission-template", ["PATCH"], mission_template.patch_mission_template
).register(app)

# Bible
Router(
    "/bible/verse", ["POST"], bible.post_bible_verse
).register(app)

Router(
    "/bible/verses", ["POST"], bible.post_bible_verses
).register(app)

Router(
    "/bible/today", ["GET"], bible.get_today_verse
).register(app)

# Template
Router(
    "/login", ["GET"], template.login_page
).register(app)

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
    "/diary", ["GET"], template.diary_page
).register(app)

Router(
    "/report", ["GET"], template.report_page
).register(app)

Router(
    "/admin", ["GET"], template.admin_page
).register(app)

Router(
    "/christmas/login", ["GET"], template.christmas_login_page
).register(app)

Router(
    "/christmas/home", ["GET"], template.christmas_home_page
).register(app)

Router(
    "/christmas/diary", ["GET"], template.christmas_diary_page
).register(app)


# #
# main

if __name__ == "__main__":
    from grapechallenge.config import get_app_env
    print("APP_ENV: ", get_app_env())

    uvicorn.run(
        **{
            "app": "server:app",
            "host": "0.0.0.0",
            "port": 8000,
            "reload": True
        }
    )