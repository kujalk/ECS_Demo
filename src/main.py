from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import boto3
from botocore.exceptions import ClientError
from fastapi.staticfiles import StaticFiles
import logging 
import os 

# Configure the logging system
logging.basicConfig(
    level=logging.INFO,              # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # Log format
    handlers=[
        logging.StreamHandler()      # Log to the console
    ]
)

# Create a logger instance
logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=os.getenv("region"))  # Replace 'your-region' with your AWS region
table = dynamodb.Table(os.getenv("table_name"))  # Replace 'students' with your DynamoDB table name

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "message": "", "status": ""})

@app.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, student_name: str = Form(...), subject: str = Form(...), marks: str = Form(...)):
    try:
        # Convert marks to integer
        marks = int(marks)
        
        # Store data in DynamoDB
        table.put_item(Item={"student_name": student_name, "subject": subject, "marks": marks})

        # On successful storage, clear the form and display success message
        message = "Data stored successfully!"
        status = "success"
    except ClientError as e:
        # Capture DynamoDB errors and display a red error message
        message = f"Failed to store data: {e.response['Error']['Message']}"
        status = "error"
        logger.error(f"Failed to store data: {e}")
    except ValueError:
        message = "Please enter a valid number for marks."
        status = "error"
        logger.error(f"Failed to store data: Value Error")
    except Exception as e:
        message = f"Failed to store data: {e}"
        status = "error"
        logger.error(f"Failed to store data: {e}")

    return templates.TemplateResponse("form.html", {"request": request, "message": message, "status": status})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
