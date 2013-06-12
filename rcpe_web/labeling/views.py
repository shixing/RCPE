# Create your views here.
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseBadRequest
import json
from models import TokenizedRc,LabelUser,LabelCount
from collections import defaultdict
from functools import partial
import random
import datetime


label_number = None
label_user = None
max_label = 3
label_start = 0
label_amount = 100
_all_done = 'ALL_DONE'


def loading():
    '''
    load two objects:
    1 label_number: id --> number
    2 label_user: user --> id
    '''
    global max_label
    global label_start
    global label_amount
    global label_number
    global label_user
    label_number = defaultdict(int)
    label_user = defaultdict(partial(defaultdict,int))
    records = TokenizedRc.objects.all()[label_start:label_start+label_amount]
    for r in records:
        label_number[r.id.strip()]=0
    records = LabelCount.objects.all()
    for r in records:
        if r.count<max_label:
            label_number[r.id.strip()] = int(r.count)
        else:
            label_number[r.id.strip()]

    records = LabelUser.objects.all()
    for r in records:
        label_user[r.userName][r.reviewId.strip()] = 1



def getId(user):
    '''
    get id to label for a specific user 
    '''
    global label_number
    global label_user
    for id in label_number:
        if label_user[user][id] == 1:
            continue
        else:
            return id
    return _all_done


def getData(id):
    r = TokenizedRc.objects.get(pk=id)
    return r.tknPair


def saveData(id,user,labelJson):
    # change database
    global label_user
    global label_number
    lu = LabelUser(reviewId=id,userName=user,label=labelJson)
    lu.save()
    lc = LabelCount.objects.filter(id__exact = id)
    if lc:
        lc = lc[0]
        lc.count += 1
        lc.save()
    else:
        lc = LabelCount(pk=id,count=1)
        lc.save()
    # change cached data
    label_user[user][id]=1
    label_number[id]+=1
    if label_number[id]>=max_label:
        del label_number[id]


def home(request):
    return render_to_response('labeling/welcome.html')


def next_label(request):
    user = request.POST['userName']
    if 'tc' in request.POST:
        print 'tc'
        id=request.POST['id']
        saveData(id,user,'too_complex')
    if 'nr' in request.POST:
        print 'nr'
        saveData(request.POST['id'],user,'not_reasonable')
    if 'label' in request.POST:
        print request.POST['label']
        saveData(request.POST['id'],user,request.POST['label'])
    id = getId(user)
    if id == _all_done:
        return HttpResponse('All Done! Thank you!')
    jsonStr = getData(id)
    return HttpResponse(jsonStr)

def refresh(request):
    loading()
    nu = len(label_user)
    return HttpResponse('User Amount:'+str(nu))

loading()
