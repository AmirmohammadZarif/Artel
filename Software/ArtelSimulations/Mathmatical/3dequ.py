import matplotlib.pyplot as plt
all_axes = []
for idx in range(1,10):
    ax = plt.subplot(3, 3, idx)
    ax.plot([1,2,3], [10, 30, 80])
    all_axes.append(ax)
    plt.show()
for ax in all_axes:
    ax.scatter([4.6], [20])
    plt.show()