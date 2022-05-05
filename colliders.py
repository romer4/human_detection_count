def lineCollider(objectY : int, lineY : int, threshold=5):
    if objectY >= lineY - threshold and objectY <= lineY + threshold:
        return True
    return False
