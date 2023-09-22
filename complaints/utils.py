from django.core.mail import send_mail


def send_complaint_emal(user_email, status):
    subject = "Complaint Request Status"
    if status == "Resolved":
        message = f"Your complaint request is Resolved."
    elif status == "In Progress":
        message = f"Your complaint request is In Progess"

    from_email = "staffsense222@gmail.com"
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
