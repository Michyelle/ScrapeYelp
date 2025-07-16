# 🕵️‍♀️ Yelp Company Info Scraper
This is a Python project that scrapes Yelp to collect business information for specified industries. Great for compiling contact details from specific industries or categories.

Scrapes the following info for businesses:
- 🏢 **Company Name**  
- 📞 **Phone Number**  
- 📍 **Address**  
- 🔗 **Company URL**

Results are exported to a **CSV file** for easy use or analysis 📊.

---

## Features
- Uses **Selenium** to navigate Yelp pages dynamically  
- Supports scraping multiple companies based on search terms or categories  
-  Allows for specific location and industry serach
- Saves results in a structured **CSV** format  

---

## Technologies Used
- Python 🐍
- Selenium 🌐

---

## Installation
1. **Clone the repository**
```
git clone https://github.com/Michyelle/ScrapeYelp.git
cd yelp-business-scraper
```

2. **Install required packages:**
```
pip install -r requirements.txt
```

3. **Update the list of search queries or keywords in the script**

4. **Run the script:**
```
python yelp_scraper.py
```

---

## 📋 Example Output
The output will be saved as a results.csv file in the project folder, containing:
```
Company Name | Phone Number | Address | Yelp URL
Michelle's Service | (123) 456-7890 | 123 Real Address | https://www.yelp.com/realbusiness
Michelle's Company | (123) 098-7654 | 321 Real Address | https://www.yelp.com/realbusiness-1
```
_May update with screenshot of a real example later..._

---

## 🎯 Project Purpose
This script is designed for educational or personal use.
***If Yelp changes their HTML structure, you may need to update the selectors in the script.***

---

## 🔗 Connect with Me
- [GitHub](https://github.com/Michyelle)
- [LinkedIn](https://www.linkedin.com/in/michellenguyen12/)
- [Portfolio](https://michellenguyen.vercel.app/)
