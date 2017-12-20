class MyClass:
    variable = "blah"

    def function(self, thing):
        print("This is a message inside the class.", thing)

    def do_thing(self):
        self.function("Hello world")


m = MyClass()
m.do_thing()