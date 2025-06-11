# Data Recipe Scraping 🍲

A Python utility to scrape recipes from cooking websites and build a clean, structured dataset for analysis or cooking applications.

---

## 🔍 Why Web Scraping?

Web scraping is the **last resort** one should use to automate data retrieval — only when **no public API is available**.

Even Google uses web scraping to build its search engine index. The process is performed by a **crawler**, like Googlebot.

In Python, web scraping often means parsing HTML files to extract specific data. The most common tool for this is **BeautifulSoup**.

---

## 📘 Quick Start Example: Offline Scraping

We’ll demonstrate scraping using a static HTML file (offline scraping), to avoid spamming the website.

### `test_scraping.py`

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("pages/carrot.html"), "html.parser")

for recipe in soup.find_all('p', class_='recipe-name'):
    print(recipe.text)
```

### Terminal

```bash
python test_scraping.py
```

💣 You’ll likely get an error the first time. Read the message — what file is missing?

Download the HTML manually:

```bash
curl -g "https://recipes.lewagon.com/?search[query]=carrot" > pages/carrot.html
```

Now re-run:

```bash
python test_scraping.py
```

✨ Congrats! You’ve just scraped your first page.

---

## 🧪 Challenge: Scrape Recipes by Keyword

The goal is to scrape the first **36 recipes** for a keyword (e.g. "chocolate") and store them in a CSV file.

```bash
python recipe.py chocolate

ls -lh recipes/
# -rw-r--r--  12K  chocolate.csv

head -n 3 recipes/chocolate.csv
# name,difficulty,prep_time
# Ultimate chocolate cake,Easy,2 hours 10 mins
# Best ever chocolate brownies recipe,More effort,1 hour
```

---

## 🧩 Required Functions in `recipe.py`

### ✅ `parse_recipe(article)`

- Input: One recipe's `<div>`
- Output: Dictionary with `name`, `difficulty`, `prep_time`

### ✅ `parse(html)`

- Input: Whole HTML page
- Output: List of recipe dicts using `parse_recipe`

### ✅ `write_csv(ingredient, recipes)`

- Input: Ingredient (str), List of recipe dicts
- Output: Creates `recipes/{ingredient}.csv`

### ✅ `scrape_from_internet(ingredient, start)`

- Input: Ingredient, start page
- Output: HTML of search results page

---

## 🧠 Main Flow

Update your `main()` in `recipe.py` to:

1. Call `scrape_from_internet`
2. Parse the result
3. Save to CSV
4. Repeat for next pages

---

## 🌀 Bonus: Pagination Support

Update `main()` and `scrape_from_internet()` to scrape up to the **first 3 pages**, if available.

💡 Tip: Use `requests.Response.history` to check if you're being redirected (e.g., no results or max page).

---

## 📂 Project Structure

```
.
├── pages/
│   └── carrot.html
├── recipes/
│   └── chocolate.csv
├── recipe.py
├── test_scraping.py
└── README.md
```

---

## 🛠 Dependencies

- `beautifulsoup4`
- `requests`
- `csv`
- `os`

Install with:

```bash
pip install -r requirements.txt
```

---

## 🙌 Have Fun Scraping!

This project is ideal for learning:

- HTML parsing
- Offline-first scraping
- Respectful, ethical web scraping
- Real-world data pipeline creation
