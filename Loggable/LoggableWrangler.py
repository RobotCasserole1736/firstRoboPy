
class LoggableWrangler(object):
    
  # singleton infrastructure
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(LoggableWrangler, cls).__new__(cls)
    return cls.instance

  def __init__(self):
      self.loggableProviders = []
      
  def register(self, class_in):
      self.loggableProviders.append(class_in)
      
  def update(self):
      for cls in self.loggableProviders:
          print(cls)