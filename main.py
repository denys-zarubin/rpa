"""Main file to execute the runner."""

import rpa


rpa.init()
rpa.url('https://www.google.com')
rpa.type('//*[@name="q"]', 'decentralization[enter]')
print(r.read('result-stats'))
rpa.snap('page', 'results.png')
rpa.close()
