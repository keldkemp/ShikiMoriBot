class MigrationsDto:
    def __init__(self, file_name, name, author, type, command=None, status=None):
        self.file_name = file_name
        self.name = name
        self.author = author
        self.type = type
        self.command = command
        self.status = status
