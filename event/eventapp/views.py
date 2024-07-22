from django.http import JsonResponse
from django.views import View
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
from datetime import datetime
from .models import EntitiesMaster


class SaveEntityView(View):
    def get(self, request):
        url = request.GET.get('url')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        location_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.location.subhead6'))
        )
        auditorium = location_element.text.strip()
        h1_element = driver.find_element(By.CSS_SELECTOR, 'h1')
        program_name = h1_element.text.strip()
        date_time_element = driver.find_element(By.CSS_SELECTOR, 'p.body-text3')
        date_time = date_time_element.text.strip()

        date_time_parts = re.split(r'\s+at\s+', date_time)
        if len(date_time_parts) == 2:
            date_str = date_time_parts[0]
            time_str = date_time_parts[1]
            date = datetime.strptime(date_str, '%a, %b %d, %Y').date()
            time = datetime.strptime(time_str, '%I:%M%p').time()
        else:
            date = None
            time = None
        artist_elements = driver.find_elements(By.CLASS_NAME, 'event-detail-artist')
        artists = []
        for artist in artist_elements:
            name_element = artist.find_element(By.CSS_SELECTOR, 'p.subhead4 a')
            role_element = artist.find_element(By.CSS_SELECTOR, 'p.subhead6')
            name = name_element.text.strip()
            role = role_element.text.strip()
            artists.append({'name': name, 'role': role})
            
        EntitiesMaster.objects.create(
            auditorium=auditorium,
            date_time=date_time,
            program_name=program_name,
            artists=artists
        )

        return JsonResponse({
            'message': 'Entities saved successfully',
            'auditorium': auditorium,
            'date_time': date_time,
            'program_name': program_name,
            'artists': artists,
            'date': date.isoformat() if date else None,
            'time': time.isoformat() if time else None,
        }, status=200)        
        
        
           