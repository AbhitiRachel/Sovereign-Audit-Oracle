
## ✅ **1. Single Inheritance (cleaned & commented)**


# This example demonstrates a Student class inheriting from a Person class

class Person:
    def __init__(self, name):
        self.name = name  # sets the person's name

    def display_name(self):
        print("Name:", self.name)

class Student(Person):
        def __init__(self, name, roll_number):
            # Call the constructor of the parent class (Person)
            super().__init__(name)
            self.roll_number = roll_number

        def display_student_info(self):
            # Call the method of the parent class to display the name
            self.display_name()
            print("Roll Number:", self.roll_number)

# Create an instance of the Student class
student1 = Student("Alice", "101")
student1.display_student_info()

## 2. Multilevel Inheritance**


# This example: Dog → Mammal → Animal

class Animal:
    def __init__(self, name):
        self.name = name

    def show_animal_info(self):
        print(f"This is an animal named {self.name}.")

class Mammal(Animal):
    def __init__(self, name, fur_color):
        super().__init__(name)
        self.fur_color = fur_color

    def show_mammal_info(self):
        self.show_animal_info()
        print(f"It has {self.fur_color} fur.")

class Dog(Mammal):
    def __init__(self, name, fur_color, breed):
        super().__init__(name, fur_color)
        self.breed = breed

    def show_dog_info(self):
        self.show_mammal_info()
        print(f"It is a {self.breed}.")

# Create an instance of Dog and show info
my_dog = Dog("Buddy", "brown", "Labrador")
my_dog.show_dog_info()


## 3. Hierarchical Inheritance**


# Rectangle and Circle both inherit from Shape

import math

class Shape:
    def area(self):
        pass  # Base class method to be overridden

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius**2

# Create instances and print areas
rectangle = Rectangle(5, 10)
circle = Circle(7)

print("Area of Rectangle:", rectangle.area())
print("Area of Circle:", circle.area())


## 4. Multiple Inheritance**


# Artist inherits from Writer and Singer

class Writer:
    def write(self):
        print("Writing a story...")

class Singer:
    def sing(self):
        print("Singing a song...")

class Artist(Writer, Singer):
    def create(self):
        print("Creating art...")

# Create an instance of Artist
my_artist = Artist()
my_artist.write()
my_artist.sing()
my_artist.create()


#5. Method Overriding**

### **Example A**


# Vehicle → Car demonstrating overriding with super()

class Vehicle:
    def info(self):
        print("This is a vehicle.")

class Car(Vehicle):
    def info(self):
        super().info()
        print("This is a car.")

my_car = Car()
my_car.info()

### Example B


# Employee → Manager overriding display()

class Employee:
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id

    def display(self):
        print(f"Employee Name: {self.name}")
        print(f"Employee ID: {self.employee_id}")

class Manager(Employee):
    def __init__(self, name, employee_id, department):
        super().__init__(name, employee_id)
        self.department = department

    def display(self):
        super().display()
        print(f"Department: {self.department}")

employee1 = Employee("Alice", "E101")
manager1 = Manager("Bob", "M201", "Sales")

employee1.display()
manager1.display()


## *6. Bank Account Hierarchy**


# Account → SavingsAccount, CurrentAccount

class Account:
    def __init__(self, account_number, holder_name):
        self.account_number = account_number
        self.holder_name = holder_name

    def display(self):
        print(f"Account Number: {self.account_number}")
        print(f"Holder Name: {self.holder_name}")

class SavingsAccount(Account):
    def __init__(self, account_number, holder_name, interest_rate):
        super().__init__(account_number, holder_name)
        self.interest_rate = interest_rate

    def display(self):
        super().display()
        print(f"Interest Rate: {self.interest_rate}%")

class CurrentAccount(Account):
    def __init__(self, account_number, holder_name, overdraft_limit):
        super().__init__(account_number, holder_name)
        self.overdraft_limit = overdraft_limit

    def display(self):
        super().display()
        print(f"Overdraft Limit: ${self.overdraft_limit}")

# Create and test objects
savings_acc = SavingsAccount("12345", "Alice", 1.5)
current_acc = CurrentAccount("67890", "Bob", 1000)

print("Savings Account Details:")
savings_acc.display()

print("\nCurrent Account Details:")
current_acc.display()

