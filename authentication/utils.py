from django.core.mail import send_mail


def send_block_email(user_email, username, is_blocked):
    subject = "Your account has been suspended"
    if is_blocked:
        message = f"""
        <html>
        <body style="background-color: #f5f5f5; font-family: Arial, sans-serif; padding: 20px;">
            <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #333333;">Subject: {subject}</h1>
                <p>Hello {username},</p>
                <p>We regret to inform you that your account has been suspended.</p>
                
                <p>If you believe this is an error or have any questions regarding your account status, please contact our support team at staffsense@support.com.</p>
                
                <p>Thank you for your understanding.</p>
                
                <p>Best regards,<br>staffsense@gmail.com</p>
            </div>
        </body>
        </html>
        """.format(
            subject=subject, username=username
        )

        send_mail(
            subject, "", "staffsense@gmail.com", [user_email], html_message=message
        )
