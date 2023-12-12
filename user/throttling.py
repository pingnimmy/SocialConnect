from rest_framework import throttling
from .models import FriendRequest
from django.utils import timezone
from datetime import timedelta



class FriendRequestRateThrottle(throttling.SimpleRateThrottle):
    scope = 'friend_requests'
    rate = "3/minute"

    def get_rate(self):
        # Extract rate based on configuration
        rate = int(self.rate.split('/')[0])
        return rate

    def get_cache_key(self, request, view):
        # Include request PK in cache key
        return f"{self.scope}-{request.user.pk}-{request.GET.get('pk', None)}"

    def allow_request(self, request, view):
        # Check if user has exceeded request limit
        if FriendRequest.objects.filter(sender=request.user, created_at__gt=timezone.now() - timedelta(minutes=1)).count() >= self.get_rate():
            return False
        return super().allow_request(request, view)