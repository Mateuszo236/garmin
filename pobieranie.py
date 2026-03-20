import pandas as pd
import json
import os
from datetime import date
from garminconnect import Garmin

#ścieżka do folderu, w którym example.py zapisał tokeny
tokenstore = os.path.expanduser("~/.garminconnect")

print("Łączenie z Garmin Connect (wczytywanie zapisanych tokenów)...")

try:
    client = Garmin()
    client.login(tokenstore)
    print("Zalogowano pomyślnie bez użycia hasła!\n")
except Exception as e:
    print(f"Błąd logowania przy użyciu tokenów: {e}")
    print("Prawdopodobnie musisz uruchomić 'python example.py' jeszcze raz, aby odświeżyć tokeny.")
    exit()

today = date.today().isoformat()
print(f"Pobieranie surowych danych dla dnia: {today}...\n")


hr_data = client.get_heart_rates(today)
if hr_data and 'heartRateValues' in hr_data:
    df_hr = pd.DataFrame(hr_data['heartRateValues'], columns=['timestamp_ms', 'heart_rate'])
    df_hr = df_hr.dropna(subset=['heart_rate'])
    
   
    df_hr['czas'] = pd.to_datetime(df_hr['timestamp_ms'], unit='ms', utc=True).dt.tz_convert('Europe/Warsaw')
    
    df_hr = df_hr[['czas', 'heart_rate']]
    hr_filename = f"RAW_Garmin_HR_{today}.csv"
    df_hr.to_csv(hr_filename, index=False)
    print(f"[+] Zapisano surowe tętno do: {hr_filename} (Ilość pomiarów: {len(df_hr)})")

stress_data = client.get_stress_data(today)
if stress_data and 'stressValuesArray' in stress_data:
    df_stress = pd.DataFrame(stress_data['stressValuesArray'], columns=['timestamp_ms', 'stress_level'])
    df_stress = df_stress.dropna(subset=['stress_level'])
    
    df_stress['czas'] = pd.to_datetime(df_stress['timestamp_ms'], unit='ms', utc=True).dt.tz_convert('Europe/Warsaw')
    df_stress = df_stress[['czas', 'stress_level']]
    
    stress_filename = f"RAW_Garmin_Stress_{today}.csv"
    df_stress.to_csv(stress_filename, index=False)
    print(f"[+] Zapisano surowy stres do: {stress_filename} (Ilość pomiarów: {len(df_stress)})")

sleep_data = client.get_sleep_data(today)
if sleep_data:
    sleep_filename = f"RAW_Garmin_Sleep_{today}.json"
    with open(sleep_filename, "w", encoding="utf-8") as f:
        json.dump(sleep_data, f, indent=4, ensure_ascii=False)
    print(f"[+] Zapisano surowe dane o śnie do: {sleep_filename}")

print("\nGotowe! Otwórz wygenerowane pliki i sprawdź strukturę.")