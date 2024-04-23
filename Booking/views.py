@csrf_exempt
@require_POST
@login_required
def book_boat_api(request, boat_id, user_id, selected_date):
    try:
        boat = Boat.objects.get(pk=boat_id)
        user = UserProfile.objects.get(pk=user_id)

        boat.availability = False
        boat.booking_date = selected_date
        boat.save()

        booking = Booking.objects.create(boat=boat, user=user, selected_date=selected_date)
        booking_id = booking.id

        return JsonResponse({'message': 'Booking successful', 'booking_id': booking_id})
    except Boat.DoesNotExist:
        return JsonResponse({'error': 'Boat not found'}, status=404)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def booking_details(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)
    return render(request, 'booking_details.html', {'booking': booking, 'boat': booking.boat})


def check_availability(request, boat_id):
    boat = get_object_or_404(Boat, pk=boat_id)

    selected_date_str = request.GET.get('date')

    if not selected_date_str:
        return JsonResponse({'error': 'Please provide a valid date parameter.'}, status=400)

    try:
        selected_date = parser.parse(selected_date_str).date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format.'}, status=400)
    is_available = boat.is_available_on_date(selected_date)

    return JsonResponse({'is_available': is_available})
