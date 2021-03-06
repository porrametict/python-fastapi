from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,PlainTextResponse

import mysql.connector
import uvicorn

from  data  import data_dict

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")




async def get_active_number () :
    mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="wdbVRmtXy0",
    password="QI7uvUL53y",
    database="wdbVRmtXy0"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM active_table")
    my_result = mycursor.fetchall()
    number = my_result[0][0]
    return number

@app.get("/")
async def root() :
    return {"message":"Hello World"}


@app.get("/user")
async def get_user():
    number = await get_active_number()
    return data_dict[number]

@app.get("/change",response_class=HTMLResponse)
async def get_active_table(request : Request):
    number = await get_active_number()
    return templates.TemplateResponse("active_table.html",{"request":request , "active_number" : number})

@app.post("/change-post")
async def change_active_number(number : int = Form(...)):
    mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="wdbVRmtXy0",
    password="QI7uvUL53y",
    database="wdbVRmtXy0"
    )
    mycursor = mydb.cursor()
    sql = f"UPDATE `active_table` SET `table` = {number};"
    mycursor.execute(sql)
    mydb.commit()
    return RedirectResponse("/change",status_code=302)



@app.get('/text',response_class=PlainTextResponse)
async def get_text():
    return "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."