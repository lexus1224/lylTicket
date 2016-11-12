from django.shortcuts import render, render_to_response
#from django.views.generic import View
from django.views.generic.base import TemplateView
from .forms import *
from trainManage.models import *
from datetime import datetime, timedelta
#from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
class ticketQuery(TemplateView):
    form_class = TicketQueryForm
    template_name = "ticket_query.html"
    def get(self, request, *args, **kwargs):
        form = TicketQueryForm()
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        startStationID = request.POST['startStation']
        startStation = Station.objects.get(id=startStationID)
        endStationID = request.POST['endStation']
        endStation = Station.objects.get(id=endStationID)
        date =  datetime.strptime(request.POST['date'], "%m/%d/%Y")
        date = datetime.date(date)
        query = Query(startStation, endStation, date)
        resultSet = query.search()

        return self.render_to_response(self.get_context_data(form=form,
                                                             startStation=startStation,
                                                             endStation=endStation,
                                                             date = date,
                                                             resultSet=resultSet))
# This is a class for search process
class Query(object):
    def __init__(self, start, end, date):
        self.start =  start
        self.end = end
        self.date = date
        self.delay = 30 # the time you can order ticket before the
    def search(self):
        #resultSet = {train_id:{seat_type:[seat_key]}}
        resultSet = {}
        startSet = set()
        endSet = set()
        for run in self.start.run_set.all():
            startSet.add(run.train_come_by)
        for run in self.end.run_set.all():
            endSet.add(run.train_come_by)
        trainSet = startSet & endSet
        for train in trainSet:
            startRun = Run.objects.get(train_come_by= train, station_name=self.start)
            endRun = Run.objects.get(train_come_by=train, station_name=self.end)
            startOrder = startRun.order_of_station
            endOrder = endRun.order_of_station
            today = datetime.date(datetime.today())
            startDate = self.date - timedelta(startRun.count_over_night) # the start date of train
            if today< self.date or ( today==self.date and datetime.time(datetime.now()) < startRun.arrive_time): # before train arrive
            # input time must later than now
                if  startOrder < endOrder:
                    for carriage in train.carriage_set.all():
                        seatSet = carriage.seat_set.all()
                        seatSet = seatSet.filter(date=startDate)
                        for seat in seatSet:
                            if seat.status[startOrder-1:endOrder] == "1" *(endOrder-startOrder+1):
                                type_seat = resultSet.setdefault(train.train_id,{})
                                seat_result = type_seat.setdefault(seat.carriage.seat_type,[])
                                seat_result.append(seat)
        return resultSet
