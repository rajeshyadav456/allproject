from soteria.models import ResetPasswordTicket, User


def create_and_send_reset_password_ticket(user: User, request):
    """
    create reset password ticket for user and send to email.
    """
    user_pass_reset_ticket: ResetPasswordTicket = ResetPasswordTicket.objects.filter(
        user=user
    ).first()
    if user_pass_reset_ticket:
        user_pass_reset_ticket.regenerate_ticket_and_send_notification(user, request)
        return

    user_pass_reset_ticket = ResetPasswordTicket.objects.create_ticket(user, request)
    user_pass_reset_ticket.send_reset_password_notification()
