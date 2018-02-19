import numpy as np


def dy_three_sigma(x, m=1.96):
    """
    3σ原则为
    数值分布在（μ-σ,μ+σ)中的概率为0.6826
    数值分布在（μ-2σ,μ+2σ)中的概率为0.9544
    数值分布在（μ-3σ,μ+3σ)中的概率为0.9974
    可以认为，Y 的取值几乎全部集中在
    （μ-3σ,μ+3σ)区间内，超出这个范围的可能性仅占不到0.3%.
    """
    # 避免共用内存引发的数值改变
    x = np.array(x)
    std = x.std()
    mean = x.mean()
    up_scale = mean + m * std
    down_scale = mean - m * std
    x[x > up_scale] = up_scale
    x[x < down_scale] = down_scale
    return x


def dy_quantile(x, up=99, down=1):
    """
    分位数去极值
    上下1%极端值处理，如果一个样本某变量的值
    大于该变量的99分位数，则该样本的值被强制
    指定为99分位数的值；类似的，如果一个样本
    某变量的值小于该变量的1分位数，则该样本该
    变量的值被强制指定为1分位数。
    """
    x = np.array(x)
    up_scale = np.percentile(x, up)
    down_scale = np.percentile(x, down)
    x[x > up_scale] = up_scale
    x[x < down_scale] = down_scale
    return x


def dy_med(x, m=1.96):
    x = np.array(x)
    x_median = np.median(x)
    distance = np.abs(x - x_median)
    distance_median = np.median(distance)
    up = x_median + m * distance_median
    down = x_median - m * distance_median
    x[x > up] = up
    x[x < down] = down
    return x


def dy_mad(x, m=1.96, k=1.4826):
    x = np.array(x)
    x_median = np.median(x)
    distance = np.abs(x - x_median)
    distance_median = np.median(distance)
    std = k * distance_median
    up = x_median + m * std
    down = x_median - m * std
    x[x > up] = up
    x[x < down] = down
    return x


class Winsorize(object):
    @staticmethod
    def three_sigma(x):
        """
        3σ原则为
        数值分布在（μ-σ,μ+σ)中的概率为0.6826
        数值分布在（μ-2σ,μ+2σ)中的概率为0.9544
        数值分布在（μ-3σ,μ+3σ)中的概率为0.9974
        可以认为，Y 的取值几乎全部集中在
        （μ-3σ,μ+3σ)区间内，超出这个范围的可能性仅占不到0.3%.
        """
        # 避免共用内存引发的数值改变
        x = np.array(x)
        std = x.std()
        mean = x.mean()
        up_scale = mean + 3 * std
        down_scale = mean - 3 * std
        x[x > up_scale] = up_scale
        x[x < down_scale] = down_scale
        return x

    @staticmethod
    def quantile(x, up=99, down=1):
        """
        分位数去极值
        上下1%极端值处理，如果一个样本某变量的值
        大于该变量的99分位数，则该样本的值被强制
        指定为99分位数的值；类似的，如果一个样本
        某变量的值小于该变量的1分位数，则该样本该
        变量的值被强制指定为1分位数。
        """
        x = np.array(x)
        up_scale = np.percentile(x, up)
        down_scale = np.percentile(x, down)
        x[x > up_scale] = up_scale
        x[x < down_scale] = down_scale
        return x

    @staticmethod
    def med(x, m=1.96):
        x = np.array(x)
        x_median = np.median(x)
        distance = np.abs(x - x_median)
        distance_median = np.median(distance)
        up = x_median + m * distance_median
        down = x_median - m * distance_median
        x[x > up] = up
        x[x < down] = down
        return x

    @staticmethod
    def mad(x, m=1.96, k=1.4826):
        x = np.array(x)
        x_median = np.median(x)
        distance = np.abs(x - x_median)
        distance_median = np.median(distance)
        std = k * distance_median
        up = x_median + m * std
        down = x_median - m * std
        x[x > up] = up
        x[x < down] = down
        return x
