Food-for-Thought JSON Validator

Files:
  - validate-food-for-thought.py
  - validate-food-for-thought.bat   (Windows double-click launcher)
  - validate-food-for-thought.command (macOS double-click launcher)

What it checks:
  - strict JSON parsing
  - exact line and column for syntax errors
  - top-level array structure
  - non-empty array
  - each item is an object
  - required fields: author, work, section, quote
  - field types: author/work/quote must be strings; section must be string or null

How to run:
  Windows:
    Double-click validate-food-for-thought.bat
    or run: py -3 validate-food-for-thought.py

  macOS / Linux:
    Double-click validate-food-for-thought.command
    or run: python3 validate-food-for-thought.py

Exit codes:
  0 = valid
  nonzero = invalid
