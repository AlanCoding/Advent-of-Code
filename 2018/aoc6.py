import os
from copy import copy
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ac6')


with open(__file__.replace('.py', '.txt')) as f:
    seq = f.read()

points = [tuple(int(part) for part in word.split(', ')) for word in seq.split('\n')]

# Example
# points = [
#     (1, 1),
#     (1, 6),
#     (8, 3),
#     (3, 4),
#     (5, 5),
#     (8, 9)
# ]

# first part answer
# 3687

logging.debug('Read sequence:\n%s', points)


counts = {point: 0 for point in points}
infinite = set()
min_point = tuple(min(point[z] for point in points) for z in range(2))
max_point = tuple(max(point[z] for point in points) for z in range(2))
max_dist = max(max_point[z] - min_point[z] for z in range(2))


logger.warn('Board boundaries: %s to %s', min_point, max_point)
logger.debug('Maximum dimension: %s', max_dist)


# part 2
pts_in = 0


def dist_bw(p1, p2):
    return sum(abs(p1[z] - p2[z]) for z in range(2))


for i in range(min_point[0], max_point[0] + 1):
    for j in range(min_point[1], max_point[1] + 1):
        pt = (i, j)
        # if (i, j) in counts:
        #     logger.info('Counting self square for %s', (i, j))
        #     counts[(i, j)] += 1
        #     continue
        # 1st method
        best_dist = None
        best_tpt = None
        best_multiple = False
        is_out = (
            any(pt[v] < min_point[v] for v in range(2)) or
            any(pt[v] > max_point[v] for v in range(2))
        )
        net_d = 0
        for tpt in counts:
            d = dist_bw(pt, tpt)
            net_d += d
            if best_dist is None or d < best_dist:
                best_dist = d
                best_tpt = tpt
                best_multiple = False
                if is_out:
                    if tpt not in infinite:
                        logger.info('Detected point %s goes out of bounds', tpt)
                        infinite.add(tpt)
                # logger.debug('Registered new best %s->%s', pt, tpt)
            elif d == best_dist:
                best_multiple = True
        if not best_multiple:
            counts[best_tpt] += 1
            logger.info('Adding to count %s->%s', pt, tpt)
        else:
            logger.info('Cannot count point %s due to multiples', pt)
        if net_d < 10000:
            pts_in += 1
        # # 2nd method
        # for dist in range(1, max_dist):
        #     is_this_dist = []
        #     visited_at_dist = set()
        #     end_look = False
        #     for polarity in (-1, +1):
        #         for z in range(2):
        #             w = (z + 1) % 2
        #             for span in range(-dist, dist):
        #                 z_var = pt[z] + span
        #                 w_var = pt[w] + polarity * (dist - abs(span))
        #                 if z == 0:
        #                     tpt = (z_var, w_var)
        #                 else:
        #                     tpt = (w_var, z_var)
        #                 if tpt in visited_at_dist:
        #                     continue
        #                 visited_at_dist.add(tpt)
        #                 # assert dist_bw((i, j), tpt) == dist
        #                 is_out = (
        #                     any(tpt[v] < min_point[v] for v in range(2)) or
        #                     any(tpt[v] > max_point[v] for v in range(2))
        #                 )
        #                 if is_out:
        #                     # logger.debug('Inspecting look-over %s -> %s, out of range.', (i, j), tpt)
        #                     continue
        #                 if tpt in counts:
        #                     # logger.debug('Inspecting look-over %s -> %s, found hit', (i, j), tpt)
        #                     is_this_dist.append(tpt)
        #                     if len(is_this_dist) > 1:
        #                         end_look = True
        #                         break
        #                 # else:
        #                 #     logger.debug('Inspecting look-over %s -> %s, no hit', (i, j), tpt)
        #             if end_look:
        #                 break
        #         if end_look:
        #             break
        #     if len(is_this_dist) == 1:
        #         hit = is_this_dist[0]
        #         logger.info('Point %s is %s from %s, updating tally.', (i, j), dist, hit)
        #         counts[hit] += 1
        #         if hit not in infinite:
        #             for z in range(2):
        #                 if (i, j)[z] == max_point[z] or (i, j)[z] == min_point[z]:
        #                     logger.warn('Detected point %s in %s goes out-of-bounds.', (i, j), hit)
        #                     infinite.add(hit)
        #         break
        #     elif is_this_dist:
        #         logger.info('Point %s is %s from %s, so none are updated.', (i, j), dist, is_this_dist)
        #         break
            # else:
            #     logger.debug('Point %s touches nothing at distance %s', (i, j), dist)


logger.info('Final point counts:\n%s', counts)


clean_counts = counts.copy()
for pt in infinite:
    clean_counts.pop(pt)


logger.warn('Qualifying final point counts:\n%s', clean_counts)
logger.warn('Count of points in 10k dist %s', pts_in)

# guesses
# 40114

