from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseBadRequest
import json
from models import Rc, Review
from socket import *


def getBusiness(jsonQuery):
    HOST = '127.0.0.1'
    PORT = 12345
    BUFFERSIZE = 1024
    ADDR = HOST, PORT
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.connect(ADDR)
    tcpSocket.send(jsonQuery)
    tcpSocket.send('\n')
    tcpSocket.send('###\n')
    data = ''
    while True:
        temp = tcpSocket.recv(1024)
        if not temp:
            break
        data += temp
    tcpSocket.close()

    # process data
    lines = data.split('\n')
    bzns = []
    for line in lines:
        if not line:
            break
        bzn = json.loads(line)
        bzns.append(bzn)
    return bzns


def home(request):
	return render_to_response('search/index.html')

def search(request):
	return render(request,'search/search.html')


def searchQuery(request):
    if len(request.GET)>0:
        # build query:
        query = {}
        if 'name' in request.GET:
            query['name']=[request.GET['name'],'should']
        if 'city' in request.GET:
            query['city']=[request.GET['city'],'should']
        if 'address' in request.GET:
            query['full_addr']=[request.GET['address'],'should']
        query = json.dumps({"business":query})
        bzns = getBusiness(query)
        # check whether there exist paris of these ids
        final_bzns = []
        print len(bzns)
        for bzn in bzns:
            id = bzn['BID']
            rc_rs = Rc.objects.filter(review__business_id__exact = id)
            if len(rc_rs) != 0:
                bzn['npair'] = len(rc_rs)
                final_bzns.append(bzn)
        print len(final_bzns)
        return HttpResponse(json.dumps(final_bzns))
    else:
        return HttpResponse('Bad Request!')

def searchPairs(request):
    if 'bid' in request.GET:
        BID = request.GET['bid']
        rc_rs = Rc.objects.filter(review__business_id__exact = BID)
        results = []
        rc_r = rc_rs[0]

        for rc_r in rc_rs:
            jsonPairs = json.loads(rc_r.pairs)
            for jsonPair in jsonPairs:
                result = {}
                reason = jsonPair[0]
                consequence = jsonPair[1]
                # print reason,consequence
                # print rc_r.review.review_clauses
                # print rc_r.id
                reviewClauses = rc_r.review.review_clauses
                if reviewClauses == None:
                    reviewClauses = []
                else:
                    reviewClauses = reviewClauses.split('###')
                result['id']=rc_r.id
                result['reason']=reason
                result['consequence']=consequence
                result['clauses'] = reviewClauses
                results.append(result)

        return HttpResponse(json.dumps(results))
    else:
        return HttpResponse('Bad Request!')
            