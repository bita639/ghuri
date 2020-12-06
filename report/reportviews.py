from django.shortcuts import render
from package.models import Payment, Customize_Tour, PayAgency, Review, Package
from blog.models import Post, Comment
from django.db.models import Sum
import datetime
from django.http import HttpResponse
from django.views.generic import View
from travel.utils import render_to_pdf
from django import template
from django.template.loader import get_template 


def showresults(request):
    if request.method=="POST":
        fromdate=request.POST.get('fromdate')
        todate=request.POST.get('todate')

        request.session['firstdate'] = fromdate
        request.session['lastdate'] = todate


        total_earning = Payment.objects.filter(payment_date__range=(fromdate, todate)).aggregate(Sum('amount'))
        total_booking= Payment.objects.filter(payment_date__range=(fromdate, todate)).count()
        custom_booking = Customize_Tour.objects.filter(booking_date__range=(fromdate, todate)).count()
        agency_paid = PayAgency.objects.filter(payment_date__range=(fromdate, todate)).aggregate(Sum('amount'))
        total_review = Review.objects.filter(created__range=(fromdate, todate)).count()
        total_package = Package.objects.filter(created__range=(fromdate, todate)).count()
        total_blog = Post.objects.filter(created__range=(fromdate, todate)).count()
        total_comment = Comment.objects.filter(created__range=(fromdate, todate)).count()

        context ={
            "total_earning":total_earning,
            "total_booking":total_booking,
            "custom_booking":custom_booking,
            "agency_paid":agency_paid,
            "total_review":total_review,
            "total_package":total_package,
            "total_blog":total_blog,
            "total_comment":total_comment,
            "fromdate":fromdate,
            "todate":todate,

        }
        return render(request,'report.html',context)
    else:
        displaydata=Payment.objects.all()
        return render(request,'report.html',{"displaydata":displaydata})


 #created in step 4

# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         data = {
#              'today': datetime.date.today(), 
#              'amount': 39.99,
#             'customer_name': 'Cooper Mann',
#             'order_id': 1233434,
#         }
#         pdf = render_to_pdf('pdf/report.html', data)
#         return HttpResponse(pdf, content_type='application/pdf')

class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('pdf/report.html')

        fromdate = request.session.get('firstdate')
        todate = request.session.get('lastdate')


        total_earning = Payment.objects.filter(payment_date__range=(fromdate, todate)).aggregate(Sum('amount'))
        total_booking= Payment.objects.filter(payment_date__range=(fromdate, todate)).count()
        custom_booking = Customize_Tour.objects.filter(booking_date__range=(fromdate, todate)).count()
        agency_paid = PayAgency.objects.filter(payment_date__range=(fromdate, todate)).aggregate(Sum('amount'))
        total_review = Review.objects.filter(created__range=(fromdate, todate)).count()
        total_package = Package.objects.filter(created__range=(fromdate, todate)).count()
        total_blog = Post.objects.filter(created__range=(fromdate, todate)).count()
        total_comment = Comment.objects.filter(created__range=(fromdate, todate)).count()

        context ={
            "total_earning":total_earning,
            "total_booking":total_booking,
            "custom_booking":custom_booking,
            "agency_paid":agency_paid,
            "total_review":total_review,
            "total_package":total_package,
            "total_blog":total_blog,
            "total_comment":total_comment,
            "fromdate":fromdate,
            "todate":todate,

        }
        html = template.render(context)
        pdf = render_to_pdf('pdf/report.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "report_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")