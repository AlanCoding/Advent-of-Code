import os
from copy import copy
from time import time
import logging
import json
import argparse


logger = logging.getLogger('ac.6')


def read_input():
    with open(__file__.replace('.py', '.txt')) as f:
        return f.read()


def parse_data(seq):
    # 470 players; last marble is worth 72170 points

    players, lmp = [
        int(s) for s in
        seq.replace(' players; last marble is worth ', ',').replace(' points', '').split(',')
    ]

    logger.debug('Data is: %s', (players, lmp))
    return (players, lmp)


def perform_place(circle, current, ball_num):
    add_idx = (current + 1) % len(circle) + 1
    circle.insert(add_idx, ball_num)
    logger.debug('Adding marble in slot %s', add_idx)
    return add_idx


def part1(players, lmp):
    from blist import blist
    scores = [0 for i in range(players)]
    # circle = [0 for i in range(lmp + 5)] # sufficiently large
    circle = blist([0])
    len_circle = 1
    current = 0
    start_time = time()
    logger.info('[  0]   0: %s', ' '.join(['%3d' % m for m in circle[:len_circle]]))
    ball_num = 1
    while True:
        player = ball_num % players
        # len_circle = len(circle)
        if ball_num % 23 == 0:
            scores[player] += ball_num
            rm_idx = (current - 7) % len_circle
            scores[player] += circle[rm_idx]
            # if ball_num + 2 < lmp:
            if True:
                # optimization
                mid_current = (rm_idx + 1) % len_circle
                current = (rm_idx + 2) % len_circle
                circle[rm_idx] = circle[mid_current]  # this is deleted, effectively
                circle[mid_current] = circle[current]
                ball_num += 1
                circle[current] = ball_num
                # logger.debug('Removing and adding marbles %s to %s', rm_idx, current)
                ball_num += 1
                continue
            else:
                raise Exception('foo!')
                logger.debug('Removing marble in slot %s, value %s', rm_idx, circle[rm_idx])
                del circle[rm_idx]
                current = rm_idx % len_circle
        else:
            add_idx = (current + 1) % len_circle + 1
            # circle[add_idx] = ball_num
            len_circle += 1
            circle.insert(add_idx, ball_num)
            # logger.debug('Adding marble in slot %s', add_idx)
            current = add_idx
        # logger.info('[%3d] %3d: %s', ball_num, current, ' '.join(['%3d' % m for m in circle[:len_circle]]))
        if ball_num % 10000 == 0:
            logger.warn('Hit point %s at time %s', ball_num, time() - start_time)
        ball_num += 1
        if ball_num > lmp:
            break
    logger.info('Final scores:\n%s', ' '.join(['%3d' % m for m in circle[:len_circle]]))
    return max(scores)


def part2(players, lmp):
    return part1(players, lmp * 100)


def the_example(idx=0):
    # Example
    return [
        '9 players; last marble is worth 25 points: high score is 32',
        '10 players; last marble is worth 1618 points: high score is 8317',
        '13 players; last marble is worth 7999 points: high score is 146373',
        '17 players; last marble is worth 1104 points: high score is 2764',
        '21 players; last marble is worth 6111 points: high score is 54718',
        '30 players; last marble is worth 5807 points: high score is 37305',
    ][i].split(':')[0]

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', help='log level', choices=('WARN', 'INFO', 'DEBUG'), default='INFO')
    parser.add_argument('--source', help='data source', choices=('input', 'example', 'trend'), default='input')
    args = parser.parse_args()
    log_level, data_source = (args.level, args.source)
    logging.basicConfig(level=getattr(logging, log_level))

    if data_source == 'example':
        N = 6
        if log_level == 'DEBUG':
            N = 1
        for i in range(N):
            data = the_example(i)
            players, lmp = parse_data(data)
            hs = part1(players, lmp)
            logger.warn('Answer to part 1:%s: high score is %s', data, hs)
    elif data_source == 'trend':
        for i in range(2000):
            hs = part1(470, i)
            logger.warn('Answer to part 1:%s: high score is %s', (470, i), hs)
    else:
        data = read_input()
        players, lmp = parse_data(data)
        hs = part1(players, lmp)
        logger.warn('Answer to part 1: %s', hs)
        hs = part2(players, lmp)
        logger.warn('Answer to part 2: %s', hs)

    # if data_source == 'input':
    #     time = part2(parents, children, 4, 60)
    # else:
    #     time = part2(parents, children, 2, 0)
    # logger.warn('Answer to part 2: %s', time)

