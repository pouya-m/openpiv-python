# testing json, ini, yml formats to save program settings
# to be sure of the ordering we should probably use ordereddicts for dictionaries, and regarding sections
# the configparser seems to be cleaner than creating dictionaries within dictionaries and the output file also looks better

from configparser import ConfigParser

settings = ConfigParser()
settings['exp'] = {'dir':'testdir', 'exp':'testexp', 'run':'testrun'}
# settings['pre'] = {'st':'True'}
# settings.set('pre', 'nf', '200')
# settings.set('pre', 'stm', 'False')
# settings.set('pre', 'stp', 'maskpath')
#settings['pre'] = {'nf':'200', 'stm':'False', 'stp':'staticmaskpath'}
# with open('settings.dat', 'w') as f:
#     settings.write(f)

# with open('settings.dat', 'r') as f:
#     settings.read(f)
exp = settings['exp']
print(settings['exp'])



# import json
# exp = {}
# exp['dir'] = 'testdir'
# exp['run'] = 'testrun'
# exp['exp'] = 'testexp'
# pre = {'st':'True', 'nf':'200', 'stm':'False', 'stp':'staticmaskpath'}
# settings = {'exp':exp, 'pre':pre}
# with open('settings.json', 'w') as f:
#     json.dump(settings, f, indent=4)

# with open('settings.json', 'r') as f:
#     settings = json.load(f)
# print(settings['exp']['run'])