# Copyright 2011 The scales Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools for pushing stat values."""

from greplin import scales

import os
import time
from fnmatch import fnmatch

from config import log_init
log = log_init(__name__)

class Pusher(object):
  """A class that pushes all stat values on-demand."""

  def __init__(self, host, port, prefix):
    """If prefix is given, it will be prepended to all stats.
    If it is not given, then a prefix will be derived from the
    hostname."""
    self.rules = []
    self.pruneRules = []

    self.host = host
    self.port = port
    self.prefix = prefix

    if self.prefix and self.prefix[-1] != '.':
      self.prefix += '.'

    self.oldPrefix = None


  def _sanitize(self, name):
    """Sanitize a name."""
    return name.strip().replace(' ', '-').replace('.', '-')


  def log(self, name, value):
    """Stubbed push call, meant to be overriden"""
    log.info("Pushing value: %s for %s" % (value, name))


  def _forbidden(self, path, value):
    """Is a stat forbidden? Goes through the rules to find one that
    applies. Chronologically newer rules are higher-precedence than
    older ones. If no rule applies, the stat is forbidden by default."""
    if path[0] == '/':
      path = path[1:]
    for rule in reversed(self.rules):
      if isinstance(rule[1], basestring):
        if fnmatch(path, rule[1]):
          return not rule[0]
      elif rule[1](path, value):
        return not rule[0]
    return True # do not log by default


  def _pruned(self, path):
    """Is a stat tree node pruned?  Goes through the list of prune rules
    to find one that applies.  Chronologically newer rules are
    higher-precedence than older ones. If no rule applies, the stat is
    not pruned by default."""
    if path[0] == '/':
      path = path[1:]
    for rule in reversed(self.pruneRules):
      if isinstance(rule, basestring):
        if fnmatch(path, rule):
          return True
      elif rule(path):
        return True
    return False # Do not prune by default


  def push(self, statsDict=None, prefix=None, path=None):
    """Push stat values out."""
    if statsDict is None:
      statsDict = scales.getStats()
    prefix = prefix or self.prefix
    path = path or '/'

    for name, value in statsDict.items():
      name = str(name)
      subpath = os.path.join(path, name)

      if self._pruned(subpath):
        continue

      if hasattr(value, 'iteritems'):
        self.push(value, '%s%s.' % (prefix, self._sanitize(name)), subpath)
      else:
        if hasattr(value, '__call__'):
          try:
            value = value()
          except:                       # pylint: disable=W0702
            value = None
            log.exception('Error when calling stat function for push')
        if self._forbidden(subpath, value):
          continue
        elif type(value) in [int, long, float] and len(name) < 500:
          #test
          log.info("we're pushing'")
          self.log(prefix + self._sanitize(name), value)


  def _addRule(self, isWhitelist, rule):
    """Add an (isWhitelist, rule) pair to the rule list."""
    if isinstance(rule, basestring) or hasattr(rule, '__call__'):
      self.rules.append((isWhitelist, rule))
    else:
      raise TypeError('Logging rules must be glob pattern or callable. Invalid: %r' % rule)


  def allow(self, rule):
    """Append a whitelisting rule to the chain. The rule is either a function (called
    with the stat name and its value, returns True if it matches), or a Bash-style
    wildcard pattern, such as 'foo.*.bar'."""
    self._addRule(True, rule)


  def forbid(self, rule):
    """Append a blacklisting rule to the chain. The rule is either a function (called
    with the stat name and its value, returns True if it matches), or a Bash-style
    wildcard pattern, such as 'foo.*.bar'."""
    self._addRule(False, rule)


  def prune(self, rule):
    """Append a rule that stops traversal at a branch node."""
    self.pruneRules.append(rule)



class PeriodicPusher(Pusher):
  """A thread that periodically pushes all stat values."""

  def __init__(self, host, port, prefix, period=60):
    """If prefix is given, it will be prepended to all stats.
    If it is not given, then a prefix will be derived from the
    hostname."""
    Pusher.__init__(self, host, port, prefix)

    self.period = period


  def __repr__(self):
    return "%s:%s" % (self.host, self.port)


  def run(self):
    """Loop forever, pushing out stats."""
    while True:
      log.info('Pusher is sleeping for %d seconds', self.period)
      time.sleep(self.period)
      log.info('Pushing stats to %s' % self)
      try:
        self.push()
        log.info('Done pushing stats to %s' % self)
      except:
        log.exception('Exception while pushing stats to %s' % self)
        raise


  def log(self, name, value):
    """send value"""
    log.info("Send %s to %s" % (value, name))