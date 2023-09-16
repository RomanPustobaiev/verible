
class VSignal:
  def __init__(self, name):
    self.name = name
    self.ref_cnt = 0

class VerilogProcess:
  def __init__(self, name, tokens):
    self.name = name
    self.get_triggers_and_sens(tokens)
    self.triggers = list(set(self.triggers))
    self.sens = list(set(self.sens))
    self.triggers = [VSignal(sname) for sname in self.triggers]
    self.sens = [VSignal(sname) for sname in self.sens]
    
    #if 'i' in self.triggers:
    #  self.triggers.remove('i')
    #if 'i' in self.sens:
    #  self.sens.remove('i')

  def is_dot_array(self, token):
    dot_array = ['[', '.', ']', 'SymbolIdentifier']
    if token['tag'] in dot_array:
      return True
    return False

  def pass_dot_array(self, ti):
    token = next(ti)
    while self.is_dot_array(token):
      token = next(ti)

    return token, ti

  def get_triggers_and_sens(self, tokens):
    triggers = []
    sens = []
    ti = iter(tokens)

    try:
      while True:
        token = next(ti)
        if token['tag'] == 'SymbolIdentifier':
          text = token['text']
          token, ti = self.pass_dot_array(ti)
          if token['tag'] == '=':
            triggers.append(text)
          else:
            sens.append(text)
    except StopIteration as e:
      pass

    self.triggers = triggers
    self.sens = sens

class VerilogHelper:
  def __init__(self):
    pass

  def extract_process(self, tokens, proc_name):
    processes = []
    nested_level = 0
    ti = iter(tokens)
    token = next(ti)
    try:
      while token['tag'] != 'end of file':
        while token['tag'] != proc_name:
          token = next(ti)

        token = next(ti)
        assert token['tag'] == 'begin'
        token = next(ti)
        assert token['tag'] == ':', 'Every process must be given a name !'
        token = next(ti)
        assert token['tag'] == 'SymbolIdentifier', 'Every process must be given a name !'

        name = token['text']
        nested_level = 1

        ntokens = []
        token = next(ti)
        while nested_level != 0:
          if token['tag'] == 'begin':
            nested_level += 1
          elif token['tag'] == 'end':
            nested_level -= 1
          else:
            ntokens.append(token)

          token = next(ti)

        processes.append(VerilogProcess(name, ntokens))

    except StopIteration as e:
      pass

    return processes

  def is_trigger(self, t, vp):
    for s in vp.sens:
      if s.name == t.name:
        return True
    return False

  def _comb_feedback(self, vp, trigger, vprocs):
    for vproc in vprocs:
      if self.is_trigger(trigger, vproc):
        if vproc.name == vp.name:
          print(f'Possible loop : parent process: [{vp.name}] trigger: [{trigger.name}]')
          return
        for t in vproc.triggers:
          if t.ref_cnt == 0:
            t.ref_cnt += 1
            self._comb_feedback(vp, t, vprocs)

  def comb_feedback(self, procs):
    for vp in procs:
      for t in vp.triggers:
        t.ref_cnt += 1
        self._comb_feedback(vp, t, procs)

