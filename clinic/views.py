
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai import types
from .models import Appointment

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env', override=True)

def home(request):
    return render(request, 'clinic/index.html')

@csrf_exempt
def book_appointment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date = data.get('date')
            time_slot = data.get('time_slot')
            payment_method = data.get('payment_method', 'Pay at Clinic')

            if Appointment.objects.filter(date=date, time_slot=time_slot).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'This slot is already booked. Please choose another time.'
                }, status=400)

            pay_status = 'Deposit Authorized' if payment_method != 'Pay at Clinic' else 'Pay at Clinic'

            Appointment.objects.create(
                patient_name=data.get('patient_name'),
                email=data.get('email'),
                phone=data.get('phone'),
                service=data.get('service'),
                doctor=data.get('doctor', 'Any Available Dentist'),
                date=date,
                time_slot=time_slot,
                payment_method=payment_method,
                payment_status=pay_status,
                notes=data.get('notes', '')
            )
            return JsonResponse({
                'status': 'success',
                'message': f"Confirmed for {date} at {time_slot} ({payment_method})!"
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
            system_prompt = (
                "You are Emma, the AI Dental Assistant for 'Lumiere Dental Care' in New York. "
                "Doctors: Dr. Marcus Vance (Implants), Dr. Elena Rostova (Cosmetic), Dr. David Chen (Surgeon), Dr. Sofia Patel (Invisalign). "
                "Services: Teeth Whitening ($299), Invisalign ($3,500+), Digital Checkup ($99), Dental Implants ($1,800+). "
                "Payment Methods: Credit/Debit Card, Apple Pay, PayPal, Dental Insurance, or Pay at Clinic. "
                "Timings: Mon-Sat 9 AM to 6 PM. Keep replies warm, short (2-3 sentences), and guide them to book below."
            )

            response = client.models.generate_content(
                model='gemini-3.5-flash-lite',
                contents=user_message,
                config=types.GenerateContentConfig(system_instruction=system_prompt)
            )
            return JsonResponse({'reply': response.text})
        except Exception as e:
            print("CHATBOT ERROR:", e)
            return JsonResponse({'reply': 'Connection issue! Please use the booking form below or call (212) 555-0198.'}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)