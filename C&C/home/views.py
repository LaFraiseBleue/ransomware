from django.http import JsonResponse
from django.shortcuts import render
from django.utils.crypto import get_random_string
import pdb;
import json
from .models import SimpleDatas


# Create your views here.
from django.views import generic
from django.views.decorators.csrf import csrf_exempt


class IndexView(generic.ListView):
    template_name = 'home/index.html'
    #context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        #return Question.objects.order_by('-pub_date')[:5]



def pay(request):
    ## Faire peter un formulaire et on est good
    return JsonResponse({})

@csrf_exempt
def paid(request):
    datas = {"paid":False}
    expected_keys = ("uuid", "host")  ##Tuples -> faster && non modifiable

    # Check if request body exists
    # Check if request body exists
    if (request.body):

        try:
            content = json.loads(request.body)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            return JsonResponse({"error": -1})

        # Check if json params exists
        # Le condense d'une vingtaine de ligne en une seule
        if len([val for i, val in enumerate(content) if content[val] and val in expected_keys]) == len(expected_keys):
            sp = SimpleDatas.objects.get(uuid=content["uuid"],host=content["host"])

            datas["paid"] = sp.paid

    return JsonResponse(datas)

@csrf_exempt
def register(request):
    # do something with the  data
    client_address = get_client_ip(request)


    data = {"encryption_key": "", "error": 0}
    expected_keys = ("uuid", "host") ##Tuples -> faster && non modifiable


    # Check if request body exists
    if(request.body) :

        try:
            content = json.loads(request.body)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            return JsonResponse({"error":-1})

        # Check if json params exists
        # Le condense d'une vingtaine de ligne en une seule
        if len([val for i, val in enumerate(content) if content[val] and val in expected_keys]) == len(expected_keys):
            #Generate token
            encrypted_string = get_random_string(512)
            data["encryption_key"] = ":".join("{:02x}".format(ord(c)) for c in encrypted_string)

            #Add all in database -
            sp = SimpleDatas(client_adress=client_address,
                             uuid=content["uuid"],host=content["host"],encryption_key=encrypted_string)
            sp.save()

        else:
            data["error"] = 2

    else:
        data["error"] = 1

    # just return a JsonResponse
    return JsonResponse(data)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip