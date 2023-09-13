
from fastapi import APIRouter, status
from fastapi import APIRouter, HTTPException
from services.category import findAllCategories, addCategory, findCategoryById, updateCategory, restoreCategory, softDeleteCategory
from models.category import Category, CategoryUpdate

router = APIRouter(prefix="/category",
                   tags=["category"],
                   responses={404: {"message": "Not found"}})



@router.get("/", response_model=list[Category], status_code=status.HTTP_200_OK)
async def getAll():
    list = await findAllCategories()
    if not list:
        raise HTTPException(status_code=404, detail="There is any category yet")
    return list

@router.post("/", status_code=status.HTTP_201_CREATED)
async def post(category: Category):
    new_category = await addCategory(category)
    return new_category

@router.get("/{id}", response_model=Category, status_code=status.HTTP_200_OK)
async def get(id:str):
    category = await findCategoryById(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{id}", response_model=CategoryUpdate, status_code=status.HTTP_200_OK)
async def update(id:str, category:CategoryUpdate):
    updated = await updateCategory(id, category)
    return updated

@router.put("/{id}/delete", response_model=CategoryUpdate, status_code=status.HTTP_200_OK)
async def update(id:str):
    updated = await softDeleteCategory(id)
    return updated

@router.put("/{id}/restore", response_model=CategoryUpdate, status_code=status.HTTP_200_OK)
async def update(id:str):
    updated = await restoreCategory(id)
    return updated