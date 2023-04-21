from toolshed.models import Message, Event


def timeline_notifications(user):
    """Return a list of notifications that the user is interested in."""
    for evt in Event.objects.all():
        if evt.user == user:
            yield evt
        for tool in user.inventory.all():
            if evt.tool == tool:
                yield evt


def timeline_events(user):
    """Return a list of events that the user is interested in."""
    for tool in user.inventory.all():
        for event in tool.events.all():
            yield event


def timeline_transactions(user):
    """Return a list of transactions that the user is interested in."""
    for tool in user.inventory.all():
        for transaction in tool.requested_transactions.all():
            yield transaction
        for transaction in tool.offered_transactions.all():
            yield transaction


def unread_messages(user):
    """Return a list of unread messages."""
    return Message.objects.filter(recipient=user, read=False)
