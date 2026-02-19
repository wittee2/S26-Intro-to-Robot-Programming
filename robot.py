class Robot:
    def __init__(self, id, location, status=True):
        self.id = id
        self.location = location
        self.status = status

    def moveBot(self, new_loc):
        self.location = new_loc

    def changeStatus(self):
        self.status = not self.status

    def __str__(self):
        state = "Online" if self.status else "Offline"
        return f"Robot ID: {self.id} | Location: {self.location} | Status: {state}"
if __name__ == "__main__":
    r1 = Robot(1, "A3")
    print(r1)

    r1.moveBot("B4")
    r1.changeStatus()

    print(r1)
