from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from .population import targeted_population
from .connection import connection,get_event_id


@csrf_exempt
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def products_view(request):

    if request.method == 'GET':
        resp = targeted_population("hr_hiring","dowelltraining",["product_name"],"life_time")
        return Response(resp['normal']['data'][0])

    if request.method == 'POST':
        product_name = request.data['product_name']
        product_url = request.data['product_url']
        print(product_name,product_url)
        command = "insert"
        eventId = get_event_id()
        output = connection(command,eventId,product_name,product_url)

        return Response({"New Product Created":output})
       
    # if request.method == 'PUT':
    #     eventId = request.data['eventId']
    #     product_name = request.data['product_name']
    #     product_url = request.data['product_url']
    #     command = "update"
    #     output = connection(command,eventId,product_name,product_url)
    #     return Response({"Product Updated":output})
    
    # if request.method == 'PATCH':
    #     eventId = request.data['eventId']
    #     product_name = request.data['product_name']
    #     product_url = request.data['product_url']
    #     command = "update"
    #     output = connection(command,eventId,product_name,product_url)
    #     return Response({"Product Updated":output})
    
    # if request.method == 'DELETE':
    #     eventId = request.data['eventId']
    #     # product_name = request.data['product_name']
    #     # product_url = request.data['product_url']
    #     command = "delete"
    #     output = connection(command,eventId)
    #     return Response({"Product Deleted":output})
    
    