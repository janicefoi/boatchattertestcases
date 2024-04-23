@csrf_exempt
@require_POST
def initiate_mpesa_payment(request):
    try:
        json_data = json.loads(request.body)
        boat_price = json_data.get('boat_price')  
        phone_number = json_data.get('phone_number')
        mpesa_api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"


        business_short_code = "174379"
        lipa_na_mpesa_online_passkey ="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"


        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode((business_short_code + lipa_na_mpesa_online_passkey + timestamp).encode('utf-8')).decode('utf-8')
        payload = {
            "BusinessShortCode": int(business_short_code),
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(boat_price),
            "PartyA": int(phone_number),
            "PartyB": int(business_short_code),
            "PhoneNumber": int(phone_number),
            "CallBackURL": "https://fa36-197-237-244-121.ngrok-free.app/mpesa-callback",
            "AccountReference": "BoatBooking",
            "TransactionDesc": "Boat Booking",
        }

        headers = {
                'Content-Type': 'application/json',
                 'Authorization': 'Bearer nVY6qnlfFirUi1xVeDeg10mtVSpN'
        }

        print("Mpesa Request Body:", json.dumps(payload))

        response = requests.post(mpesa_api_url, json=payload, headers=headers)
        print("Mpesa Response:", response.text)

        response_data = response.json()
        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({"error": str(e)})
    
@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response_code = data.get('ResponseCode')
            customer_message = data.get('CustomerMessage')
            if response_code == '0' and customer_message.lower().startswith('success'):
                booking_id = data.get('booking_id')
                update_booking_status(booking_id, 'confirmed')
                return JsonResponse({'status': 'success'})
            else:
    
                return JsonResponse({'status': 'failure'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@require_POST
def update_booking_status(request):
    try:
        json_data = json.loads(request.body)
        booking_id = json_data.get('booking_id')
        status = json_data.get('status')

        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = status
        booking.save()

        print('Received booking ID:', booking_id, 'Status:', status) 
        return JsonResponse({'message': 'Booking status updated', 'status': status})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
