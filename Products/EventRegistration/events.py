

def handle_registrant(self):
    """
    Send confirmation emails
    """
    self.object.sendConfirmationEmail(self.object)
