# Importerar nödvändiga bibliotek och moduler från Selenium och webdriver_manager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Länk till aktuell sida med grupper på Chalmers Canvas
url = "https://chalmers.instructure.com/courses/XXXXX/groups" 

# Namnet på den grupp vi vill gå med i
wanted_group = "Labb- och seminariegrupper 1A" 

# Skapa alternativ för Chrome-webbläsaren
options = Options()
options.add_argument("--start-maximized")  # Starta webbläsaren i maximerat läge
options.add_experimental_option("detach", True)  # Låt webbläsaren vara öppen efter skriptet avslutas

# Specifik användarprofil (byt ut *USER* mot korrekt användarnamn)
userdatadir = 'C:/Users/*USER*/AppData/Local/Google/Chrome/User Data' 
options.add_argument(f"--user-data-dir={userdatadir}")

# Installera och ställ in ChromeDriver via ChromeDriverManager
driverPath = ChromeDriverManager().install()
service = Service(executable_path=driverPath)

# Starta Chrome-webbläsaren med de definierade inställningarna
driver = webdriver.Chrome(service=service, options=options)

# Öppna URL till gruppsidan
driver.get(url)

# Implicit väntan för att låta sidan ladda (max 10 sekunder)
driver.implicitly_wait(10)

# Navigera till Chalmers inloggningssida och logga in med SAML
driver.find_element(By.XPATH, '//a[@href="https://chalmers.instructure.com/login/saml"]').click()
driver.find_element(By.CLASS_NAME, 'submit').click()  # Klicka på "Logga in" knappen

##############################

# Hämta alla element som representerar gruppnamn på sidan
groups = driver.find_elements(By.CLASS_NAME, "student-group-title")

# Hitta önskad grupp baserat på gruppnamn
matching_group = next(
    (index for index, group in enumerate(groups)
    if driver.execute_script("return arguments[0].firstChild.textContent;", group.find_element(By.TAG_NAME, "h2")).strip() == wanted_group),
    None
)

# Om gruppen hittades, skriv ut index, annars avsluta programmet
if matching_group is not None:
    print(f"Gruppen '{wanted_group}' hittades på index {matching_group}.")
    print("----------------")
else:
    print(f"Gruppen '{wanted_group}' hittades inte, kontrollera gruppnamn.")
    driver.quit()  # Avsluta programmet om gruppen inte hittas

# Variabel för att kontrollera om sidan ska uppdateras kontinuerligt
refresh = True

# Loop som uppdaterar sidan tills gruppen är tillgänglig för anslutning
while refresh:
    availability = driver.find_elements(By.CLASS_NAME, "student-group-join")[matching_group]
    driver.implicitly_wait(0)  # Ta bort implicit väntan för snabbare uppdateringar

    # Kontrollera om knappen "Join" är synlig
    if availability.find_elements(By.XPATH, "//button//span[contains(text(), 'Join')]"):
        print("Gruppen är öppen")
        print("----------------")
        refresh = False  # Stoppa uppdateringen om gruppen är öppen
    else:
        print("Gruppen är ej öppen, uppdaterar...")
        driver.refresh()  # Uppdatera sidan om gruppen inte är öppen
        driver.implicitly_wait(10)  # Återinför implicit väntan på 10 sekunder

# Klicka på knappen för att gå med i gruppen när den är tillgänglig
availability.find_element(By.CLASS_NAME, "css-1xpzopy-view--inlineBlock-baseButton").click()

# Skriv ut bekräftelse och avsluta programmet
print(f"Har gått med i {wanted_group}.")
print("Avslutar...")
