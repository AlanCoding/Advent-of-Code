import os
from copy import copy
import logging
import json
import argparse


logger = logging.getLogger('ac.6')


def read_input():
    with open(__file__.replace('.py', '.txt')) as f:
        return f.read()


def parse_data(seq):
    # Step F must be finished before step R can begin.

    edges = []
    children = {}
    parents = {}
    for word in seq.split('\n'):
        edge = tuple(
            l for l in
            word.replace('Step ', '').replace(' must be finished before step ', ',').replace(' can begin.', '').split(',')
        )
        for z in range(2):
            children.setdefault(edge[z], [])
            parents.setdefault(edge[z], [])
        # set children
        children[edge[0]].append(edge[1])
        # set parents
        parents[edge[1]].append(edge[0])

    logger.debug('Loaded dependencies:\n%s', json.dumps(parents, indent=4))
    return parents, children


def part1(parents, children):
    active = [step for step in parents if parents[step] == []]
    active.sort()
    logger.debug('Root steps: %s', active)
    done = set()
    order = ''
    while active:
        c = active[0]
        del active[0]
        done.add(c)
        logger.info('Processing %s', c)
        order += c
        new = set(children[c]) - done
        for d in copy(new):
            blockers = set(parents[d]) - done
            if blockers:
                logger.debug('Character %s is not yet available for processing because %s are not done', d, blockers)
                new.remove(d)
        active = list(set(active) | set(new))
        active.sort()
        logger.debug('New active steps: %s', active)
    return order


def task_time(c, base_time):
    ch_time = 'abcdefghijklmnopqrstuvwxyz'.index(c.lower()) + 1
    t = ch_time + base_time
    return t

# guesses
# 947, too high

def part2(parents, children, elves, base_time):
    active = [step for step in parents if parents[step] == []]
    active.sort()
    logger.debug('Root steps: %s', active)
    done = set()
    in_progress = {}
    order = ''
    time = 0
    while active or in_progress:
        # Finish existing work
        for c in list(in_progress.keys()):
            in_progress[c] -= 1
            if in_progress[c] == 0:
                logger.debug('Finished work on %s', c)
                in_progress.pop(c)
                done.add(c)
                order += c
                new = set(children[c]) - done
                for d in copy(new):
                    blockers = set(parents[d]) - done
                    if blockers:
                        logger.debug('Character %s is not yet available for processing because %s are not done', d, blockers)
                        new.remove(d)
                active += set(new)
        active = list(active)
        active.sort()
        logger.debug('New active steps: %s', active)
        # Start new work
        while active and len(in_progress) < elves:
            c = active[0]
            del active[0]
            assert c not in in_progress
            in_progress[c] = task_time(c, base_time)
            logger.debug('Starting work on %s with worker %s, taking %s', c, len(in_progress), in_progress[c])
        logger.info(
            'Second %-3s has %s in-progress, %s processed',
            time, ' '.join(in_progress.keys() + ['.' for i in range(elves - len(in_progress))]), order
        )
        time += 1
    return time - 1



def the_example():
    # Example
    return '\n'.join([
        'Step C must be finished before step A can begin.',
        'Step C must be finished before step F can begin.',
        'Step A must be finished before step B can begin.',
        'Step A must be finished before step D can begin.',
        'Step B must be finished before step E can begin.',
        'Step D must be finished before step E can begin.',
        'Step F must be finished before step E can begin.',
    ])

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', help='log level', choices=('WARN', 'INFO', 'DEBUG'), default='INFO')
    parser.add_argument('--source', help='data source', choices=('input', 'example'), default='input')
    args = parser.parse_args()
    log_level, data_source = (args.level, args.source)
    logging.basicConfig(level=getattr(logging, log_level))
    if data_source == 'input':
        data = read_input()
    else:
        data = the_example()
    parents, children = parse_data(data)
    order = part1(parents, children)
    logger.warn('Answer to part 1: %s', order)
    if data_source == 'input':
        time = part2(parents, children, 4, 60)
    else:
        time = part2(parents, children, 2, 0)
    logger.warn('Answer to part 2: %s', time)

