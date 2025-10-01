class Ticket:
    def __init__(self, id, user, subject, message):
        self.id = id
        self.user = user
        self.subject = subject
        self.message = message
        self.status = 'Open'
        self.admin_response = None