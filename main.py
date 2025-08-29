from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Union

app = FastAPI()

class InputData(BaseModel):
    data: List[Union[str, int]]

@app.get("/bfhl")
def get_bfhl():
    return {"operation_code": 1}

@app.post("/bfhl")
def post_bfhl(request: InputData):
    user_id = "hardik_gupta_24101999"  # replace with your format if needed
    email = "hardik@example.com"       # replace with your email
    roll_number = "CS1234"             # replace with your roll number

    alphabets = []
    numbers = []
    highest_alphabet = None
    specials = []
    even_numbers = []
    odd_numbers = []
    num_sum = 0
    concat = ""

    for item in request.data:
        item_str = str(item)

        if item_str.isalpha():
            alphabets.append(item_str)
            concat += item_str
            if highest_alphabet is None or item_str.upper() > highest_alphabet.upper():
                highest_alphabet = item_str

        elif item_str.isdigit():
            num = int(item_str)
            numbers.append(num)
            concat += item_str
            num_sum += num
            if num % 2 == 0:
                even_numbers.append(num)
            else:
                odd_numbers.append(num)

        else:
            specials.append(item_str)
            concat += item_str

    return {
        "is_success": True,
        "user_id": user_id,
        "email": email,
        "roll_number": roll_number,
        "alphabets": alphabets,
        "numbers": numbers,
        "highest_alphabet": highest_alphabet,
        "special_characters": specials,
        "even_numbers": even_numbers,
        "odd_numbers": odd_numbers,
        "sum": num_sum,
        "concat": concat
    }
