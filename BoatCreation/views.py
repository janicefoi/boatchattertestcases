def dashboard(request):
    boats = Boat.objects.all()
    return render(request, 'dashboard.html', {'boats': boats})
