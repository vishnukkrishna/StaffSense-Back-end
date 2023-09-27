from django.template.loader import get_template
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Visitor
from authentication.models import Employee
from rest_framework.response import Response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from rest_framework.views import APIView
from django.conf import settings
from reportlab.lib import colors
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from rest_framework import status
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
import uuid
import os
import qrcode
import pdfkit

# Create your views here.


class VisitorListAPIView(APIView):
    def get(self, request):
        visitors = Visitor.objects.all().values()
        return JsonResponse(list(visitors), safe=False)

    def delete(self, request, visitor_id):
        try:
            visitor = Visitor.objects.get(id=visitor_id)
            visitor_email = visitor.email

            visitor.delete()

            send_mail(
                "Appointment Cancellation",
                "Your scheduled visit has been cancelled due to some reasons. Thank you!",
                settings.EMAIL_HOST_USER,
                [visitor_email],
                fail_silently=False,
            )

            return JsonResponse(
                {"message": "Visitor deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Visitor.DoesNotExist:
            return JsonResponse(
                {"message": "Visitor not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @csrf_exempt
    def post(self, request):
        name = request.data.get("name")
        contact_info = request.data.get("email")
        purpose = request.data.get("reason")
        visit_datetime = request.data.get("date")
        startTime = request.data.get("startTime")
        endTime = request.data.get("endTime")
        organizer_id = request.data.get("organizerId")
        organizer = get_object_or_404(Employee, id=organizer_id)

        if Visitor.objects.filter(email=contact_info).exists():
            return HttpResponseBadRequest("Visitor's slot is already booked")

        unique_identifier = self.generate_unique_identifier()

        visitor = Visitor(
            name=name,
            reason=purpose,
            email=contact_info,
            date=visit_datetime,
            start_time=startTime,
            end_time=endTime,
            organizer=organizer,
            unique_identifier=unique_identifier,
        )

        visitor.save()
        qr_code = self.generate_qr_code(unique_identifier)

        self.send_notification_email(visitor, qr_code)
        return JsonResponse({"message": "Visitor registered successfully!"})

    def generate_unique_identifier(self):
        unique_id = uuid.uuid4()
        return str(unique_id)

    def generate_qr_code(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)

        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        return qr_image

    def send_notification_email(self, visitor, qr_code):
        subject = "Visitor Registration Details"
        from_email = settings.EMAIL_HOST_USER

        to_email = visitor.email

        # Render the email body template with visitor details
        template = get_template("email_template.html")
        context = {
            "visitor": visitor,
            "qr_code": qr_code,
        }

        email_body = render_to_string("email_template.html", context)

        # Generate the PDF file
        pdf_buffer = self.generate_visitor_ticket_pdf(visitor)

        pdf_buffer_io = BytesIO(pdf_buffer)
        # Create the email message object
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=from_email,
            to=[to_email],
        )

        email.content_subtype = "html"

        # Attach the PDF file to the email
        email.attach("visitor_ticket.pdf", pdf_buffer_io.getvalue(), "application/pdf")

        # Send the email
        email.send(fail_silently=False)

    def generate_visitor_ticket_pdf(self, visitor):
        # Create the PDF file
        pdf_buffer = BytesIO()
        p = canvas.Canvas(pdf_buffer, pagesize=letter)

        # Set background color
        p.setFillColorRGB(0.95, 0.95, 0.95)  # Light gray
        p.rect(0, 0, 612, 792, fill=True, stroke=False)

        # Draw the QR code on the PDF canvas
        qr_code = self.generate_qr_code(visitor.unique_identifier)
        qr_code_path = os.path.join(settings.MEDIA_ROOT, "qrcodes", "qr_code.png")
        qr_code.save(qr_code_path)  # Save the QR code image
        p.drawImage(qr_code_path, 400, 550, width=200, height=200)

        # Draw other visitor details
        p.setFont("Helvetica-Bold", 18)
        p.setFillColor(colors.black)  # Set text color to black
        p.drawString(100, 710, f"Name: {visitor.name}")
        p.drawString(100, 685, f"Purpose: {visitor.reason}")
        p.drawString(100, 660, f"Visit Date: {visitor.date}")
        p.drawString(100, 635, f"Start Time: {visitor.start_time}")
        p.drawString(100, 610, f"End Time: {visitor.end_time}")

        # Save the PDF content
        p.showPage()
        p.save()

        # Reset the PDF file buffer
        pdf_buffer.seek(0)

        return pdf_buffer.getvalue()
