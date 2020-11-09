class NoReceiverConnectionException(Exception):
    def __init__(self):
        super().__init__('Connection with the receiver hasn\'t established.')
