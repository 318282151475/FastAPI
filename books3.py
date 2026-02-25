#Will be adding more data validation logic steps

from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class BOOK:

    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int


    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: int
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=5)
    rating: int = Field(gt=0, lt=11)
    rating: int = Field(gt=0, lt=11)
    published_date: int = Field(gt = 1999)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "New book name",
                "author": "Tejas",
                "description": "Books description",
                "rating": 5,
                "published_date": 2001
            }
        }

    }


books = [
          BOOK(1, 'Maths', 'Tejas', 'Mathematics book', 10, 2001),
          BOOK(2, 'Science', 'Virat', 'Scientific book', 5, 2004),
          BOOK(3, 'English', 'ABD', 'Good grammer book', 5, 2010),
          BOOK(4, 'Commerce', 'Anushka', 'CA', 4, 2005)
        ]

@app.get("/books")
def get_all_books():
    return books


@app.post("/create_body_with_pydantic")
def crete_book(new_book: BookRequest):
    create_another_book = BOOK(**new_book.dict())
    books.append(get_book_id(create_another_book))


def get_book_id(book: BOOK):
    if len(books) > 0:
        book.id = books[-1].id + 1
    else:
        book.id = 1

    return book

@app.get("/books/rating/{rating}")
def get_book_by_rating(rating: int):

    new_book = []
    for book in books:
        if book.rating == rating:
            new_book.append(book)

    return new_book


@app.put("/books/update_book")
def update_existing_book(book: BookRequest):
    for i in range(len(books)):
        if books[i].id == book.id:
            books[i] = book

@app.delete("/books/{id}")
def delete_book(id: int = Path(gt=0)):  #Path parameter validation -Path should now have value of id >0 --/books/-9 (this will fail)
     for i in range(len(books)):
        if books[i].id == id:
            books.pop(i)
            break

@app.get("/books/published/", status_code=status.HTTP_200_OK)
def get_book_by_date(date: int = Query(gt=1999)):
    for book in books:
        if book.published_date == date:
            return book
    raise HTTPException(status_code=404, detail='Item not found')