from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class BOOK:

    id: int
    title: str
    author: str
    description: str
    rating: int


    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int


books = [
          BOOK(1, 'Maths', 'Tejas', 'Mathematics book', 10),
          BOOK(2, 'Science', 'Virat', 'Scientific book', 9),
          BOOK(3, 'English', 'ABD', 'Good grammer book', 7),
          BOOK(4, 'Commerce', 'Anushka', 'CA', 4)
        ]

@app.get("/books")
def get_all_books():
    return books

# @app.post("/create_book")
# def create_new_book(new_book = Body()):
#     books.append(new_book)

# FastAPI converts request data into a Pydantic model for validation.
# After validation, we convert it to a normal Python object so that business logic remains independent of Pydantic.

@app.post("/create_body_with_pydantic")
def crete_book(new_book: BookRequest):      #new_book becomes type of BookRequest
    print(type(new_book))    # books.BookRequest (BookRequest is pydantic type)
    #we are converting pydantic object to normal dict object
    #why --> pydantic model made for validation they should not mixed with business logic
    create_another_book = BOOK(**new_book.dict())  # new_book.dict() --> convert pydantic to dict, ** - is kwargs unpacking, constructor is called by BOOK
    print(type(create_another_book))         # books.BOOK (BOOK is regular class type)
    books.append(create_another_book)

