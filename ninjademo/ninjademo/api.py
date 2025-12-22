from ninja import NinjaAPI,Schema,File,UploadedFile
from datetime import date
from core.models import Employee,Department
from django.shortcuts import get_object_or_404
api = NinjaAPI()

# creating a simple endpoint

class HelloSchema(Schema):
    name:str="world"

class UserSchema(Schema):
    username:str
    email:str = None
    fname:str = None
    lname:str = None

class Error(Schema):
    message:str


class EmployeeIn(Schema):
    fname:str
    lname:str
    department_id:int = None
    birthday:date = None

class EmployeeOut(Schema):
    id : int
    fname:str
    lname:str
    department_id:int = None
    birthday:date = None
    cv:str = None

# @api.post("/employee")
# def create_employee(request,payload:EmployeeIn,cv:UploadedFile = File(...)):
#     employee = Employee.objects.create(**payload.dict())
#     employee.cv.save(cv.name,cv)
#     return {"id":employee.id}

@api.post("/employee")
def create_employee(request,payload:EmployeeIn,cv:File[UploadedFile]):
    employee = Employee.objects.create(**payload.dict())
    employee.cv.save(cv.name,cv)
    return {"id":employee.id}

@api.get("/employee/{id}",response=EmployeeOut)
def get_employee(request,id:int):
    response = get_object_or_404(Employee,id=id)
    return response

