class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        print("Woof!")


def main():
    print("Hello, World!")
    my_dog = Dog("Buddy")
    my_dog.bark()


if __name__ == "__main__":
    main()
