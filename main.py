from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Union
import os

app = FastAPI(title="BFHL API")

class BFHLRequest(BaseModel):
    data: List[Union[str, int]]

def make_user_id() -> str:
    full_name = os.getenv("FULL_NAME", "john doe").strip().lower()
    # convert any whitespace sequence to single underscore
    full_name = "_".join(full_name.split())
    dob = os.getenv("DOB_DDMMYYYY", "17091999").strip()
    return f"{full_name}_{dob}"

EMAIL = os.getenv("EMAIL", "john@xyz.com")
ROLL = os.getenv("ROLL_NUMBER", "ABCD123")

@app.get("/bfhl")
def get_bfhl():
    # often required by tests
    return {"operation_code": 1}

@app.post("/bfhl")
def post_bfhl(payload: BFHLRequest):
    try:
        odd_numbers: List[str] = []
        even_numbers: List[str] = []
        alphabets: List[str] = []
        special_characters: List[str] = []
        # Collect all individual alphabetical characters (preserve original character case)
        letter_chars: List[str] = []
        # Keep numeric tokens as strings
        numeric_tokens: List[str] = []

        for item in payload.data:
            s = str(item)

            # Pure number (only digits)
            if s.isdigit():
                numeric_tokens.append(s)
                n = int(s)
                if n % 2 == 0:
                    even_numbers.append(s)
                else:
                    odd_numbers.append(s)

            # Pure alphabet token (like "a" or "ABcD")
            elif s.isalpha():
                alphabets.append(s.upper())          # token -> uppercase in alphabets array
                for ch in s:
                    if ch.isalpha():
                        letter_chars.append(ch)    # preserve original case for concat_string processing

            # Mixed or special tokens (e.g., "$", "ab#1")
            else:
                special_characters.append(s)
                for ch in s:
                    if ch.isalpha():
                        letter_chars.append(ch)    # still extract letters for concat_string

        # Sum of numeric tokens, returned as string
        total_sum = str(sum(int(x) for x in numeric_tokens)) if numeric_tokens else "0"

        # Build concat_string:
        #  - take all extracted alphabetical characters in input-order (preserve their original case)
        #  - reverse that string
        #  - apply alternating caps starting with UPPER for index 0, lower for index 1, etc.
        reversed_letters = "".join(letter_chars)[::-1]  # reversed preserving original char values
        out_chars = []
        for i, ch in enumerate(reversed_letters):
            out_chars.append(ch.upper() if i % 2 == 0 else ch.lower())
        concat_string = "".join(out_chars)

        response = {
            "is_success": True,
            "user_id": make_user_id(),
            "email": EMAIL,
            "roll_number": ROLL,
            "odd_numbers": odd_numbers,              # numbers as strings
            "even_numbers": even_numbers,            # numbers as strings
            "alphabets": alphabets,                  # tokens that were purely alphabetic, uppercased
            "special_characters": special_characters,
            "sum": total_sum,                        # sum as string
            "concat_string": concat_string
        }
        return JSONResponse(status_code=200, content=response)

    except Exception as e:
        # graceful error response with is_success=false
        return JSONResponse(status_code=400, content={
            "is_success": False,
            "error": str(e)
        })
