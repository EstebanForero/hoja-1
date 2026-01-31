class ConnectState:
    def __init__(self):
        self.state = [[0 for i in range(7)] for i in range(6)]

    def show(self):
        for row in self.state:
            print(row)


def main():
    cnn = ConnectState()
    cnn.show()


if __name__ == "__main__":
    main()
