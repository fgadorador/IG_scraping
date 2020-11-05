from scraper import Ig_scraper

path = r"C:\Users\Fernando\Desktop\geckodriver-v0.27.0-win64\geckodriver.exe"
ig = Ig_scraper()

ig.scraper(path = path, explorer='firefox')