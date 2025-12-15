from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request

# Create your views here.


@api_view(['GET', 'POST', 'PATCH', 'PUT', 'DELETE','HEAD'])
def hello_world(req):
    if req.method == "GET":
        return Response(status=200, data={"msg": "It's a get request"})
    elif req.method == "POST":
        return Response(status=200, data={"msg": "It's a post request"})
    elif req.method == "PATCH":
        return Response(status=200, data={"msg": "It's a patch request"})
    elif req.method == "PUT":
        return Response(status=200, data={"msg": "It's a put request"})
    elif req.method == "DELETE":
        return Response(status=200, data={"msg": "It's a put request"})
    else:
        return Response(status=200, data={"msg": "Unknown method"})
    




