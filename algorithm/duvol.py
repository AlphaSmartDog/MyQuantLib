import numpy as np


def duvol_down(x):
    l = 60 # 时间窗口
    wa = np.convolve(x, [1. / l] * l, mode="full")[l - 1:-l + 1]
    x = x[l - 1:]

    buffer = []
    for i in np.arange(l, len(x)):
        mx = x[i - l: i]
        mwa = wa[i - l: i]
        mask = mx > mwa

        up_mask = np.sum(mask) - 1
        if not up_mask:
            up_mask = 1
        up = np.sum(np.power((mx - mwa), 2) * mask) / up_mask

        down_mask = np.sum(1 - mask) - 1
        if not down_mask:
            down_mask = 1
        down = np.sum(np.power((mx - mwa), 2) * (1 - mask)) / down_mask
        duvol = down / up
        buffer.append(duvol)
    buffer = np.array(buffer)
    buffer = np.clip(buffer, 0, 100)
    return np.array([np.nan] * (2 * l - 1) + list(buffer))


if __name__ == "__main__":
    data = np.random.uniform(-0.1, 0.1, size=399)
    print(duvol(data))