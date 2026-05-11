class SwitchBox:

    def __init__(self):
        self.switches = {}


    def add_switch(self, route_name, state):

        self.switches[route_name] = state


    def enable_switch(self, route_name):

        self.switches[route_name] = True


    def disable_switch(self, route_name):

        self.switches[route_name] = False


    def toggle_switch(self, route_name):

        current_state = self.switches.get(route_name, False)

        self.switches[route_name] = not current_state


    def is_enabled(self, route_name):

        return self.switches.get(route_name, False)


    def show_switches(self):

        for route, state in self.switches.items():
            print(route, "=", state)