class Register:

    def __init__(
        self,
        name,
        pipeline_stage=0
    ):

        self.name = name

        self.pipeline_stage = pipeline_stage

        self.input_value = 0

        self.output_value = 0

        self.next_value = 0


    # -------------------------
    # LOAD INPUT
    # -------------------------
    def load_input(
        self,
        value
    ):

        self.next_value = value


    # -------------------------
    # CLOCK TICK
    # -------------------------
    def clock_tick(self):

        self.output_value = self.next_value


    # -------------------------
    # GET OUTPUT
    # -------------------------
    def get_output(self):

        return self.output_value