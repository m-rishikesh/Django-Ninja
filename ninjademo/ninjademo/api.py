from ninja import NinjaAPI,Schema,File,UploadedFile
from datetime import date
from core.models import Employee,Department
from django.shortcuts import get_object_or_404
from typing import List
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

# Single Query Result

@api.get("/employee/{id}",response=EmployeeOut)
def get_employee(request,id:int):
    response = get_object_or_404(Employee,id=id)
    return response

# Multiple Query Result

@api.get("/employees",response=List[EmployeeOut])
def get_employees(request):
    response = Employee.objects.all()
    return response


# Uploading the File (Just File)
# Use FileSystemStorage and UploadedFile,File

from django.core.files.storage import FileSystemStorage

STORAGE = FileSystemStorage()

@api.post('/upload')
def file_upload(request,cv:File[UploadedFile]):
    filename = STORAGE.save(cv.name,cv)
    return f"FileName: {filename}"


# Upadating the Records

@api.put("/employee/{id}")
def update_employee(request,id:int,payload:EmployeeIn):
    employee = get_object_or_404(Employee,id=id)
    if employee:
        for key,val in payload.dict(exclude_unset=True).items():
            setattr(employee,key,val)
        employee.save()
        return {"success":True}
    else:
        return {"success":False,"Reason":"Record Not Found!"}

# Deleting a Record

@api.delete("/employee/{id}")
def remove_employee(request,id:int):
    employee = get_object_or_404(Employee,id=id)
    employee.delete()
    return {"success":True}