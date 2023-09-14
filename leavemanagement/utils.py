from django.core.mail import send_mail


def send_leave_email(user_email, is_approved, start_date, end_date):
    subject = "Leave Request Status"
    if is_approved:
        message = (
            f"Your leave request from {start_date} to {end_date} has been approved."
        )
    else:
        message = (
            f"Your leave request from {start_date} to {end_date} has been rejected."
        )

    from_email = "your_email@example.com"  # Replace this with your email address
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
