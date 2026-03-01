from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from app.db.postgres import get_db

from app.models.applications import JobApplication
from app.schemas.application_schema import JobApplicationCreate, JobApplicationResponse


router = APIRouter(prefix="/applications",tags=["Applications"])

@router.post("/",response_model=JobApplicationResponse, status_code=201)
async def create_application(payload: JobApplicationCreate, db: AsyncSession=Depends(get_db)):
    new_application=JobApplication(**payload.model_dump())
    db.add(new_application)
    # db.commit() and db.refresh are only for write ops not for read ops
    # like post, delete and put methods not for get
    await db.commit()  
    await db.refresh(new_application)
    return new_application

@router.get("/",response_model=list[JobApplicationResponse])
async def get_all_applications(db : AsyncSession=Depends(get_db)):
    result=await db.execute(select(JobApplication))
    return result.scalars().all()

@router.get("/{id}",response_model=JobApplicationResponse)
async def get_application_by_id(id: int, db: AsyncSession = Depends(get_db)):
    result=await db.execute(select(JobApplication).where(JobApplication.id == id))

    application=result.scalar_one_or_none()
    if application is None: 
        raise HTTPException(status_code=404, detail="Application not found!")
    
    return application

@router.put("/{id}",response_model=JobApplicationResponse)
async def update_application(id: int, payload: JobApplicationCreate , db: AsyncSession=Depends(get_db)):
    result=await db.execute(select(JobApplication).where(JobApplication.id==id))

    application=result.scalar_one_or_none()
    
    if application is None:
        raise HTTPException(status_code=404,detail="Application not found!")
    
    for key, value in payload.model_dump().items():
        setattr(application,key,value)
    
    await db.commit()
    await db.refresh(application)
    return application

@router.delete("/{id}", status_code=204)
async def delete_application_by_id(id:int, db:AsyncSession=Depends(get_db)):
    result=await db.execute(select(JobApplication).where(JobApplication.id == id))

    application=result.scalar_one_or_none()
    if application is None:
        raise HTTPException(status_code=404, detail="No content to delete!")
    
    await db.delete(application)
    await db.commit()