def smooth_angle(previous, target, factor):
    return int(previous + factor * (target - previous))