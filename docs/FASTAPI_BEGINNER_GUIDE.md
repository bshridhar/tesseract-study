# FastAPI Beginner Setup Guide

**Everything you need to start learning FastAPI from scratch**

## ✅ Prerequisites You Already Have

Based on your current setup:
- ✅ Python 3.9+ installed
- ✅ Virtual environment (.venv)
- ✅ FastAPI & Uvicorn installed
- ✅ VSCode with Python extension

**You're already 90% ready!** 🎉

## 🎯 FastAPI Learning Roadmap (Beginner)

### Week 1: Basics (Your calendar: Nov 3-9)

**Day 1-2: Hello World & Path Parameters**
```python
# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

**Day 3-4: Query Parameters & Request Body**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "price": item.price}
```

**Day 5-7: Response Models & Status Codes**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str

@app.post("/users/", response_model=User, status_code=201)
def create_user(user: User):
    return user

@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id not in database:
        raise HTTPException(status_code=404, detail="User not found")
    return database[user_id]
```

### Week 2-3: Intermediate (Nov 10-23)

**Database Integration**
```python
# Install SQLAlchemy
pip install sqlalchemy sqlmodel

# app/database.py
from sqlmodel import Field, Session, SQLModel, create_engine

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

# app/main.py
@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        return hero
```

**Authentication (JWT)**
```python
# Install dependencies
pip install python-jose[cryptography] passlib[bcrypt]

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    # Verify token and return user
    return current_user
```

### Week 4: Testing & Deployment (Nov 24-30)

**Testing with pytest**
```python
# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Foo", "price": 50.5}
    )
    assert response.status_code == 201
```

## 📚 Learning Resources (In Order)

### 1. Official FastAPI Tutorial (Start Here!)
```bash
# Open in browser
https://fastapi.tiangolo.com/tutorial/
```

**Follow these sections in order:**
1. First Steps (5 min)
2. Path Parameters (10 min)
3. Query Parameters (10 min)
4. Request Body (15 min)
5. Query Parameters and String Validations (15 min)
6. Path Parameters and Numeric Validations (10 min)
7. Body - Multiple Parameters (15 min)
8. Response Model (15 min)

**Total: ~2 hours for basics** ⏱️

### 2. Build Practice Projects

**Project 1: TODO API (Week 1)**
```python
# Simple CRUD operations
from fastapi import FastAPI
from typing import List

app = FastAPI()

todos = []

@app.post("/todos/")
def create_todo(title: str, description: str):
    todo = {"id": len(todos) + 1, "title": title, "description": description}
    todos.append(todo)
    return todo

@app.get("/todos/", response_model=List[dict])
def read_todos():
    return todos

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, title: str, description: str):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["title"] = title
            todo["description"] = description
            return todo
    return {"error": "Todo not found"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            return {"message": "Deleted"}
    return {"error": "Todo not found"}
```

**Project 2: User Management (Week 2)**
- User registration
- Login with JWT
- Protected routes
- User profile

**Project 3: Blog API (Week 3)**
- Posts with authors
- Comments
- Tags/Categories
- Search functionality

### 3. Video Resources (Optional)

**YouTube:**
- "FastAPI Tutorial - Building RESTful APIs" by Traversy Media
- "FastAPI Course for Beginners" by freeCodeCamp
- FastAPI official channel

**Time: 3-4 hours total**

## 🛠️ Your Daily FastAPI Practice (20 min)

Based on your calendar's "20 min FastAPI/Python" sessions:

### Monday-Wednesday: Learn Concept
```bash
# 1. Read one section from FastAPI docs (10 min)
https://fastapi.tiangolo.com/tutorial/

# 2. Code along in your project (10 min)
uvicorn app.main:app --reload
# Test the endpoint
```

### Thursday-Friday: Build Feature
```bash
# 1. Add new endpoint to your app (15 min)
# 2. Write test for it (5 min)
pytest tests/test_main.py -v
```

### Weekend: Mini Project
```bash
# 1. Build small API (1-2 hours)
# 2. Test thoroughly
# 3. Push to GitHub
```

## 🎯 FastAPI Quick Reference

### Essential Decorators
```python
@app.get("/")          # GET request
@app.post("/")         # POST request
@app.put("/")          # PUT request
@app.delete("/")       # DELETE request
@app.patch("/")        # PATCH request
```

### Path Parameters
```python
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### Query Parameters
```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return items[skip : skip + limit]
```

### Request Body (Pydantic)
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
def create_item(item: Item):
    return item
```

### Response Model
```python
@app.post("/users/", response_model=User)
def create_user(user: User):
    return user
```

### Error Handling
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

### Dependencies
```python
from fastapi import Depends

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db = Depends(get_db)):
    return db.get_users()
```

## 🔧 Essential Tools

### 1. Interactive API Docs (Built-in!)
```bash
# Start server
uvicorn app.main:app --reload

# Open in browser
http://localhost:8000/docs      # Swagger UI
http://localhost:8000/redoc     # ReDoc
```

**Use this to test your API visually!**

### 2. HTTP Client (Testing)
```bash
# Install httpie (optional)
brew install httpie

# Test endpoints
http GET http://localhost:8000/
http POST http://localhost:8000/items/ name="Foo" price=50.5
```

### 3. VSCode Extensions
```bash
# Already installed, but ensure you have:
- Python (Microsoft)
- Pylance
- REST Client (for testing APIs in VSCode)
```

## 📝 Sample Learning Schedule

**Your calendar already includes FastAPI sessions!** Follow this:

### Week 1 (Nov 3-9)
- Mon: FastAPI basics, first endpoint
- Tue: Path parameters
- Wed: Query parameters  
- Thu: Request body with Pydantic
- Fri: Response models
- Weekend: Build TODO API

### Week 2 (Nov 10-16)
- Mon: Database setup (SQLModel)
- Tue: CRUD operations
- Wed: Relationships
- Thu: Error handling
- Fri: Validation
- Weekend: Build User Management API

### Week 3 (Nov 17-23)
- Mon: Authentication basics
- Tue: JWT tokens
- Wed: Protected routes
- Thu: Testing
- Fri: Async operations
- Weekend: Build Blog API

## 🚀 Quick Start Right Now

```bash
# 1. Your environment is already set up!
cd ~/tesseract/tesseract-study
source .venv/bin/activate

# 2. Run the existing app
uvicorn app.main:app --reload

# 3. Open browser
http://localhost:8000/docs

# 4. Start learning!
# Open: https://fastapi.tiangolo.com/tutorial/first-steps/
```

## 💡 Tips for Beginners

1. **Use the docs page** - Test all endpoints visually first
2. **Type hints matter** - They enable auto-validation
3. **Pydantic is your friend** - Learn it well
4. **Read error messages** - FastAPI errors are very clear
5. **Start simple** - Don't jump to auth immediately
6. **Build projects** - Learning by doing is fastest
7. **Test as you go** - Write tests for each endpoint

## 🎓 Recommended Order

```
Week 1: Basic CRUD (Create, Read, Update, Delete)
Week 2: Database Integration
Week 3: Authentication & Authorization
Week 4: Testing & Best Practices
Week 5: Async Operations
Week 6: Deployment
```

## 📖 Additional Resources

**Official Docs:** https://fastapi.tiangolo.com/
**Discord:** https://discord.gg/fastapi (Get help here!)
**GitHub:** https://github.com/tiangolo/fastapi (Examples in repo)
**Real Python:** https://realpython.com/fastapi-python-web-apis/

---

**You're all set! Start with the official tutorial and build along! 🚀**

Your setup is perfect for learning. Just open the docs and start coding!
