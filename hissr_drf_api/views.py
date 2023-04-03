# Third party imports
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Internal imports



@api_view()
def root_route(request):
    """
    View to display on landing page for the API.
    """
    return Response({
        "message": "Welcome to the hissr drf API"
    })
