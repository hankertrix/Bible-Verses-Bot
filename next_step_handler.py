# The module to handle the next step of a command or conversation

from telebot import types

class NextStepHandler():
  """Class to handle the next step of a command or conversation"""

  def __init__(self, *, max_step: int) -> None:
    self.convos = {}
    self.max_step = max_step

  def register_next_step_handler(self, convo_name: str, message: types.Message) -> None:
    """Function to register the next step of a command or conversation"""

    # The name of the entry into the dictionary
    entry = f"{convo_name}_convo {message.from_user.id} {message.chat.id}"

    # Checks if the function name and chat id is not inside the dictionary
    if self.convos.get(entry) is None or self.convos.get(entry) > self.max_step:

      # Create the dictionary entry
      self.convos[entry] = 1

    # If the function name is already inside
    else:

      # Increment the number in the dictionary
      self.convos[entry] += 1

  def check_step(self, convo_name: str, message: types.Message, step: int) -> bool:
    """Function to check the step in the filters for the message handlers"""

    # Returns whether the step is inside the dictionary
    return self.convos.get(f"{convo_name}_convo {message.from_user.id} {message.chat.id}") == step

  def clear_step_handler(self, convo_name: str, message: types.Message) -> None:
    """Function to clear the step handler for a function and chat id. Must always be called at the end of a conversation"""

    # Removes the entry from the dictionary
    self.convos.pop(f"{convo_name}_convo {message.from_user.id} {message.chat.id}")

    


