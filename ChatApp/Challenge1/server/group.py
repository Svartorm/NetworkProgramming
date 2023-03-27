class Group: 
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.members = [owner]