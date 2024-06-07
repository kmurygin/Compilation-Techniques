class Reader:
    def __init__(self, source):
        self.source = source
        self.current_char = ""
        self.current_position = (1, 0)
        self.next_position = (1, 1)
        self.next()

    def next(self):
        next_char = self.source.read(1)

        if not next_char:
            self.current_char = "EOF"
            self.current_position = (self.next_position[0] + 1, 0)

        elif next_char == "\n":
            self.current_char = next_char
            self.current_position = self.next_position
            self.next_position = (self.current_position[0] + 1, 1)

        elif next_char == "#":
            while self.current_char != "\n":
                self.next()

        else:
            self.current_char = next_char
            self.current_position = self.next_position
            self.next_position = (self.current_position[0], self.current_position[1] + 1)

    def get_current_char(self):
        return self.current_char

    def get_current_position(self):
        return self.current_position
