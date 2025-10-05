from django.shortcuts import render
from rest_framework import viewsets
from .models import Listing, Bookings
from .serializers import ListingSerializer, BookingSerializer

class ListingViewSet(viewsets.ModelViewSet):
    # queryset tells the mdel which objects it should work with
    queryset = Listing.objects.all()

    # serializer tells the viewset how to convert model data
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    # queryset tells the mdel which objects it should work with
    queryset = Bookings.objects.all()

    # serializer tells the viewset how to convert model data
    serializer_class = BookingSerializer

# Create your views here.
