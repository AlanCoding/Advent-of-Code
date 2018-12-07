import os

with open(__file__.replace('.py', '.txt')) as f:
    seq = f.read()

str_entries = seq.split('\n')

# [1518-10-29 00:02] falls asleep
# [1518-07-29 00:58] wakes up
# [1518-03-18 00:15] falls asleep
# [1518-11-08 00:02] Guard #2851 begins shift

class Entry:
    def __init__(self, str_entry):
        time_str, action = str_entry.strip('[').split(']')
        self.action = action.strip(' ')
        time = [
            int(dig) for dig in time_str.replace('-', ' ').replace(':', ' ').split(' ')
        ]
        if time[3] == 0:
            time[3] = 24
        self.time = tuple(time)
        self.sub_actions = []

    def __unicode__(self):
        return '%s: %s' % (self.time, self.action)

    def __repr__(self):
        return self.__unicode__()

    def guard_id(self):
        if self.action.endswith('begins shift'):
            print self.action
            id_str = self.action.replace('#', ' ').strip(' ').split(' ')[2]
            return int(id_str)
        else:
            return None

    def nap_times(self):
        naps = []
        for i in range(len(self.sub_actions)/2):
            naps.append((self.sub_actions[i*2].time[-1], self.sub_actions[i*2+1].time[-1]))
        return naps


entries = []
guards = {}

for str_entry in str_entries:
    e = Entry(str_entry)
    entries.append(e)
    guard = e.guard_id()
    if guard is not None:
        guards[guard] = []


def entry_hash(entry):
    return entry.time


entries.sort(key=entry_hash)

for entry in entries:
    print str(entry) + ' : ' + str(entry.guard_id())


for entry in entries[1:]:
    if entry.guard_id() is not None:
        primary = entry
    else:
        primary.sub_actions.append(entry)

primaries = []

for entry in entries:
    if entry.guard_id() is not None:
        primaries.append(entry)


for entry in primaries:
    guards[entry.guard_id()].append(entry)


time_sheet = {}
frac_nap = {}
max_frac = 0
max_nap_guard = None

for guard, shifts in guards.items():
    time_sheet[guard] = {}
    nap_time = 0
    days = 0
    time_sheet[guard] = [0 for i in range(60)]
    for entry in shifts:
        days += 1
        for nap in entry.nap_times():
            for i in range(*nap):
                time_sheet[guard][i] += 1
                nap_time += 1
    f = float(nap_time)/days
    frac_nap[guard] = f
    if f > max_frac:
        max_frac = f
        max_nap_guard = guard
        for j in 

print frac_nap
print guard
