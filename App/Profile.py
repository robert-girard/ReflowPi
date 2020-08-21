'''
ReflowPi

Copyright © <2019> <Robert Girard>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from dataclasses import dataclass
from typing import List

@dataclass
class Step:
    startTemp: float
    endTemp: float
    Duration: float

@dataclass
class Profile:
    name: str
    steps: List[Step]
    def __getitem__(self, key):
        return self.steps[key]
    @classmethod
    def fromdict(cls, data):
        name = data.get('ProfileName', None)
        steps = data.get('Steps', None)
        if not name or not steps:
           raise TypeError
        psteps = []
        for step in steps:
           eT = step.get('endTemp')
           sT = step.get('startTemp')
           Dur = step.get('Duration')
           psteps.append(Step(sT,eT,Dur))
        return cls(name, psteps)
