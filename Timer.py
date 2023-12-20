import time


class Timer:
  '''Runs function immediately after start, then every [interval] seconds'''

  def __init__(self, id, func, **kwargs):
    self.id = id
    self.func = func
    self.interval = None
    self.start_time = None
    self.enabled = False
    self.on_post_run = kwargs.get('post_run', None)

  def _handle_post_run(self):
    '''handles post run events'''
    self.start_time += self.interval
    if self.on_post_run:
      return self.on_post_run(self.id)

  def enable(self):
    '''enables Timer'''
    self.enabled = True
    self.start_time = time.time()
    self.run_func()

  def disable(self):
    '''disables timer'''
    self.enabled = False
    self.start_time = None

  def set_interval(self, value):
    '''Sets Time Interval for calling function'''
    self.interval = value
    self.enable()

  def run(self):
    '''Runs function if interval has passed'''
    if not self.enabled:
      return
    now = time.time()
    if now - self.start_time > self.interval:
      self.run_func()
    
  def run_func(self):
    '''Runs function and post_run'''
    self.func()
    self._handle_post_run()
