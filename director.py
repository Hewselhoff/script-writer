COMMAND_LIST = []

def RegisterCommand(command):
  COMMAND_LIST.append(command)
  return command

class DirectorCommand():
  def __init__(self,
               name:str):
    self._name = name

  @property
  def name(self):
    return self._name

  @property
  def syntax(self):
    raise NotImplementedError("Subclasses must implement this property")

  def format(self, *args, **kwargs):
    raise NotImplementedError("Subclasses must implement this method")

  def __call__(self, *args, **kwargs):
    output = self.format(self, *args, **kwargs)
    return output


@RegisterCommand
class SceneChangeCommand(DirectorCommand):
  def format(self,
             time:str,
             location:str,
             plot_purpose:str,          
             context:str,             
             summary:str):
    command_template = \
    ("\n*SCENE CHANGE*:\n"
     "  * Time: {time}\n"
     "  * Location: {location}\n"
     "  * Plot Purpose: {plot_purpose}\n"
     "  * Context: {context}\n"
     "  * Summary: {summary}\n\n")
    return command_template.format(time=time,
                                   location=location,
                                   plot_purpose=plot_purpose,
                                   context=context,
                                   summary=summary)
  @property
  def syntax(self):
    output = \
    { 
      self.name: {
        "time": "<The time at which the scene takes place, e.g. 'night', 'morning', '06:00', 'Tuesday afternoon', 'one year later', etc.>",
        "location": "<The location of the scene, e.g. 'the park', 'the beach', 'John's house', 'downtown Chicago', etc.>",
        "plot_purpose": "<The purpose of the scene in within the context of the plot, e.g. 'to introduce the main character', 'to show the villain's evil plan', 'to show the hero's tragic flaw', etc.>",
        "context": "<Any additional context that the director wants to provide to set the scene, e.g. 'it is raining outside', 'the house is old and rundown', 'the characters are walking', etc.>",
        "summary": "<A brief summary of the scene, e.g. 'the hero sees the villain, there is some dialogue, they fight, the villain flees, the hero chases the villain, the villain eventually escapes', etc.>"
      }
    }
    return str(output)
    

class DirectorRole():
  PROMPT_GENRE_TEMPLATE = '* You are the director for {genre}, titled "{title}".'.format
  PROMPT_DIRECTOR_TEMPLATE = "* From here on, you are to take on the persona of the director {director} in all responses.".format
  PROMPT_CONTEXT_TEMPLATE = "* Here is some additional information about the project, for context:\n{context}".format
  PROMPT_INSTRUCTIONS_TEMPLATE = \
  ("* Try to provide direction notes that are in line with the style and aesthetic of {director}.\n"
   "* You should compose your responses according to the following rules and constraints:\n"
   "  * ").format
  TEMPLATE = \
  """Your Role:
  {genre}
  {director}
  {context}
  {instructions}
  """.format
  def __init__(self,
               title:str,
               context:list, 
               genre:str, 
               director:str=None, 
               instructions:list=None):
    self.title = title
    self.context = context
    self.genre = genre
    self.director = director
    self.instructions = instructions
    self.genre_prompt = self.PROMPT_GENRE_TEMPLATE(genre=genre,title=title)
    context_format = "\n".join(["    * {} {}".format(title, line) for line in context])
    self.context_prompt = self.PROMPT_CONTEXT_TEMPLATE(context=context_format)
    self.director_prompt = self.PROMPT_DIRECTOR_TEMPLATE(director=director) if director else ""
    self.instructions_prompt = self.PROMPT_INSTRUCTIONS_TEMPLATE(director=director)
    if instructions:
      self.instructions_prompt += "\n" + "\n".join(["  * {}".format(line) for line in instructions])
    # Compile role prompt
    self._string = self.TEMPLATE(context=self.context_prompt,
                                 genre=self.genre_prompt,
                                 director=self.director_prompt,
                                 instructions=self.instructions_prompt)

  def __str__(self):
    return self._string