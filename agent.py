import threading

class Agent:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.knowledge_base = {}
        self.dispatcher.register('cell_revealed', self.on_cell_revealed)
        self.dispatcher.register('assist_request', self.on_assist_request)

    def on_cell_revealed(self, cell):
        key = (cell.x, cell.y)
        self.knowledge_base[key] = cell
        # Optionally, process the cell information in the background

    def on_assist_request(self, data):
        # Run the computation in a separate thread to avoid blocking the GUI
        thread = threading.Thread(target=self.provide_assistance)
        thread.start()

    def provide_assistance(self):
        # Return a list of is_mine percentages
        advice = 0
        self.dispatcher.dispatch('assist_response', advice)

