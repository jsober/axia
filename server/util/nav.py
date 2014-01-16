from copy import copy
from info import JUMPS, SYSTEM_ID, WORMHOLE, sector_py2vo, sector_py2vochar


class Point(object):
    """Represents a single point on a sector map.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return '%s-%d' % sector_py2vochar(self.x, self.y)

    def __hash__(self):
        """Algorithm from http://stackoverflow.com/a/13871379/89182
        """
        if self.x >= self.y:
            return self.x * self.x + self.x + self.y
        else:
            return self.x + self.y * self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def is_valid(self, grid_size):
        """Returns True if this Point is in the positive plane (x and y > 0)
        and within the bounds of grid_size.
        """
        return self.x >= 0 \
           and self.y >= 0 \
           and self.x <= grid_size \
           and self.y <= grid_size

    def spiral(self):
        """Generates Points in a spiral from this Point, progressively further
        out. Points may be negative and so should be checked by the caller.
        """
        x = self.x
        y = self.y

        r = 1
        i = x - 1
        j = y - 1

        while True:
            while i < x + r:
                i += 1
                yield Point(i, j)

            while j < y + r:
                j += 1
                yield Point(i, j)

            while i > x - r:
                i -= 1
                yield Point(i, j)

            while j > x - r:
                j -= 1
                yield Point(i, j)

            r += 1
            y -= 1

            yield Point(i, j)


class Segment(object):
    """Represents a line segment between two Points.
    """
    def __init__(self, start, end):
        """Creates a new Segment between Points start and end.
        """
        self.start = start
        self.end = end

    def walk(self):
        """Generates Points along the path between the starting and ending
        point. If the slope is 45 degrees, no Points are generated where
        the line segment passes directly between two sectors.
        """
        x = self.start.x
        y = self.start.y
        dx = abs(self.end.x - x)
        dy = abs(self.end.y - y)
        n = 1 + dx + dy
        x_inc = 1 if self.end.x > x else -1
        y_inc = 1 if self.end.y > y else -1
        error = dx - dy

        dx *= 2
        dy *= 2

        const_slope = dy == dx

        while n > 0:
            yield Point(x, y)

            if const_slope:
                x += x_inc
                y += y_inc
                n -= 1
            elif error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx

            n -= 1

    def sectors(self, avoid):
        """Generates Points along the path, up until it would collide with a
        point in set `avoid`.
        """
        for point in self.walk():
            if point not in avoid:
                yield point
            else:
                break

    def waypoints(self, avoid):
        """Returns the beginning and ending Points for this Segment, up to and
        not including a collision with a point in set `avoid`.
        """
        waypoints = [self.start]

        end = None
        for point in self.sectors(avoid):
            end = point

        if end is not None:
            waypoints.append(end)

        return waypoints


class Path(object):
    """A path between two points on a grid of a given size.
    """
    def __init__(self, size, start, end):
        """Creates a new Path on a grid of `size` square sectors, running from
        `start` to `end`.
        """
        self.size = size
        self.start = start
        self.end = end
        self.obstacles = set([])
        self.avoid = set([])

    def add_obstacle(self, point):
        """Marks a Point as an obstacle to the path generator.
        """
        self.obstacles.add(point)

    def add_avoidance(self, point):
        """Marks a Point as a sector to avoid in path generation.
        """
        self.avoid.add(point)

    def is_valid_point(self, point):
        """Returns True if `point` exists on a grid of self.size.
        """
        return point.is_valid(self.size)

    def has_clear_path(self, start, end):
        """Returns True if there are no avoidance points between Points start
        and end.
        """
        segment = Segment(start, end)
        points = segment.waypoints(self.avoid)

        if len(points) != 2:
            return False

        (p1, p2) = points
        return p1 == start and p2 == end

    def spiral(self, point):
        """Generates Points spiraling out from `point` that are valid for the
        given size grid and are not obstacles.
        """
        total = 0
        for i in xrange(0, self.size):
            total += i * 8

        for p in point.spiral():
            total -= 1
            if total == 0:
                break

            x = p.x
            y = p.y

            if abs(x) > self.size or abs(y) > self.size:
                continue

            if x < 0 or y < 0:
                continue

            if not self.is_valid_point(p):
                continue

            if p in self.obstacles:
                continue

            if p in self.avoid:
                continue

            yield p

    def find_waypoint(self, start=None, end=None):
        """Attempts to find a path between `start` and `end` that is free of
        obstacles using a single waypoint.
        """
        if start is None:
            start = self.start

        if end is None:
            end = self.end

        for point in self.spiral(start):
            if not self.has_clear_path(start, point):
                continue

            if not self.has_clear_path(point, end):
                continue

            return point

    def find_waypoint_2(self, start=None, end=None):
        """Attempts to find a path between `start` and `end` that is free of
        obstacles using two waypoints.
        """
        if start is None:
            start = self.start

        if end is None:
            end = self.end

        for point in self.spiral(end):
            if not self.has_clear_path(point, end):
                continue

            waypoint = self.find_waypoint(start, point)
            if waypoint is not None:
                return [waypoint, point]

    def calculate_path(self, start=None, end=None):
        """Attempts to find a path between `start` and `end` that is clear
        of obstacles using the fewest waypoints possible.
        """
        if start is None:
            start = self.start

        if end is None:
            end = self.end

        if self.has_clear_path(start, end):
            return [start, end]

        waypoint = self.find_waypoint(start, end)
        if waypoint is not None:
            return [start, waypoint, end]

        waypoints = self.find_waypoint_2(start, end)
        if waypoints is not None:
            return [start, waypoints[0], waypoints[1], end]

    def draw(self):
        """For debugging, draws an ASCII representation of the Path.
        """
        highlights = set([])
        waypoints = self.calculate_path()
        previous = waypoints.pop(0)

        for point in waypoints:
            segment = Segment(previous, point)
            previous = point

            for p in segment.sectors(self.obstacles):
                highlights.add(p)

        draw(self.size, highlights, self.obstacles)


class Sector(object):
    """Represents an individual Sector within a system.
    """
    def __init__(self, system, point):
        if system not in SYSTEM_ID or system is None:
            raise ValueError('unknown system; short system name expected')

        self.system = system
        self.point = point

    def __eq__(self, other):
        return self.system == other.system and self.point == other.point

    def __unicode__(self):
        return '%s %s' % (self.system, self.point)

    def __repr__(self):
        return self.__unicode__()

    def sector_id(self):
        s = SYSTEM_ID[self.system]
        (x, y) = sector_py2vo(self.point.x, self.point.y)
        return (s - 2) * 256 + (y - 1) * 16 + x

    def __hash__(self):
        return self.sector_id()


def draw(size, highlights=None, obstacles=None):
    """For debugging, draws an ASCII representation of a grid of `size` x
    `size` sectors, marking Points in set `highlights` with an asterisk (*) and
    Points in set `obstacles` with an X.
    """
    if highlights is None:
        highlights = set([])

    if obstacles is None:
        obstacles = set([])

    line = ["_"]
    for _ in xrange(0, size):
        line.append("__")

    print "".join(line)

    for y in xrange(0, size):
        line = ["|"]

        for x in xrange(0, size):
            point = Point(x, y)

            if point in highlights:
                line.append("*|")
            elif point in obstacles:
                line.append("X|")
            else:
                line.append("_|")

        print "".join(line)

    print "\n"


def jump_plans(start, end, route=None, acc=None, seen=None):
    """Finds all possible series of system jumps between system `start` and
    `end`, both of which must be short system names.
    """
    if route is None:
        route = []

    if acc is None:
        acc = []

    if seen is None:
        seen = set()

    if start not in seen:
        seen.add(start)
        rt = copy(route)
        rt.append(start)

        if start == end:
            acc.append(rt)
        else:
            for system in JUMPS[start]:
                jump_plans(system, end, copy(rt), acc, copy(seen))

    return acc


def shortest_jump_plans(start, end):
    """Finds the shortest series of system jumps between system `start` and
    `end`, both of which must be short system names.
    """
    routes = jump_plans(start, end)
    shortest = min(len(r) for r in routes)
    return [r for r in routes if len(r) == shortest]


def plan_route(start, end, avoid=None, obstacles=None):
    """Generates an optimal series of navigation waypoints between sectors
    `start` and `end`, avoiding Sectors in set `avoid`.
    """
    if avoid is None:
        avoid = set()

    if obstacles is None:
        obstacles = set()

    systems = shortest_jump_plans(start.system, end.system)[0]
    routes = []

    def _route(system, start_point, end_point):
        path = Path(16, start_point, end_point)
        if avoid is not None:
            for sector in avoid:
                if sector.system == system:
                    if sector.point in [start_point, end_point]:
                        continue
                    path.add_avoidance(sector.point)

            for sector in obstacles:
                if sector.system == system:
                    if sector.point in [start_point, end_point]:
                        continue
                    path.add_obstacle(sector.point)

        return path.calculate_path()

    if len(systems) == 1:
        route = _route(systems[0], start.point, end.point)
        if route:
            return [Sector(systems[0], w) for w in route]
    else:
        for i in xrange(0, len(systems)):
            current_system = systems[i]

            if i == 0:
                start_point = start.point

                # If the start point of the entire route is a wormhole
                # sector, do not add it to the route.
                x, y = WORMHOLE[current_system][systems[i + 1]]
                if start_point.x == x and start_point.y == y:
                    continue
            else:
                start_point = Point(*WORMHOLE[current_system][systems[i - 1]])

            if i == len(systems) - 1:
                end_point = end.point
            else:
                end_point = Point(*WORMHOLE[current_system][systems[i + 1]])

            waypoints = _route(current_system, start_point, end_point)
            routes.extend([Sector(current_system, w) for w in waypoints])

    return routes


def navigate(waypoints, avoid=None, obstacles=None):
    """Generates a series of safe jumps between `waypoints`, avoiding crossing
    any sectors in set `avoid` and refusing to use sectors in set `obstacles`
    as waypoints.
    """
    if avoid is None:
        avoid = set()

    if obstacles is None:
        obstacles = set()

    start = waypoints[0]
    plan = []

    # Ensure that avoid includes none of the waypoints
    avoid = avoid - set(waypoints)
    obstacles = obstacles - set(waypoints)

    for end in waypoints[1:]:
        route = plan_route(start, end, avoid, obstacles)
        plan.extend(route[1:])
        start = end

    return plan
