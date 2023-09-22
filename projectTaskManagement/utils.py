from django.core.mail import send_mail


def send_task_email(user_email, name, assignedTo, start_date, end_date):
    subject = "Assigned New Task"

    if assignedTo:
        message = f"""
        <html>
        <body>
            <h1>Subject: New Task Assignment</h1>
            <p>Dear Employee,</p>
            <p>We are writing to inform you that a new task has been assigned to you:</p>
            
            <ul>
                <li><strong>Task Name:</strong> {name}</li>
                <li><strong>Assigned To:</strong> {assignedTo}</li>
                <li><strong>Start Date:</strong> {start_date}</li>
                <li><strong>End Date:</strong> {end_date}</li>
            </ul>
            
            <p>Please review the task details carefully and ensure that you can meet the deadlines. If you have any questions or need further clarification regarding the task, please feel free to reach out to the admin or your supervisor.</p>
            
            <p>Thank you for your prompt attention to this matter. We appreciate your dedication to your work.</p>
            
            <p>Best regards,<br>staffsense@gmail.com</p>
        </body>
        </html>
        """

        send_mail(
            subject, "", "staffsense@gmail.com", [user_email], html_message=message
        )
