from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title':'Think & Grow Rich', 'author':'One', 'category':'Mindset'},
    {'title':'Mind', 'author':'two', 'category':'gym'},
    {'title':'hi', 'author':'Three', 'category':'Habits'}

]

@app.get("/hello")
def first_api():
    return BOOKS



@app.post("/books/create_book")
def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.delete("/books/{title}")
def delete_data(title : str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('Title') == title:
            BOOKS.pop(i)
            break

@app.get("/books/{title}/")
async def get_all_books(title: str, author: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title') == title and BOOKS[i].get('author') == author:
            return BOOKS[i]
    return "No Data"