

def handle_registrant(obj, event):
    """
    Send confirmation emails
    """
    obj.sendConfirmationEmail(obj)
