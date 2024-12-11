import math

# 定义3个元组，每个元组包含5个点 (x, y)


import numpy as np
import random


def ransac_find_x0_y0(tuples, threshold=1.0, iterations=100):
    best_x0, best_y0 = None, None
    max_inliers = 0
    best_inliers = []

    # Flatten all points from the tuples for RANSAC sampling
    all_points = [point for t in tuples for point in t]

    for _ in range(iterations):
        # Randomly select a point as the hypothesis
        x0, y0 = random.choice(all_points)

        # Calculate inliers: points within the threshold distance
        inliers = []
        for t in tuples:
            for point in t:
                distance = np.sqrt((point[0] - x0) ** 2 + (point[1] - y0) ** 2)
                if distance < threshold:
                    inliers.append(point)

        # Update best hypothesis if current inliers are the most
        if len(inliers) > max_inliers:
            max_inliers = len(inliers)
            best_x0, best_y0 = x0, y0
            best_inliers = inliers

    # Find the closest point to the best_x0, best_y0 in each tuple
    closest_points = []
    for t in tuples:
        closest_point = min(t, key=lambda p: np.sqrt((p[0] - best_x0) ** 2 + (p[1] - best_y0) ** 2))
        closest_points.append(closest_point)

    return best_x0, best_y0, closest_points


# 示例输入
tuple1 = [(1, 2), (13, 4), (5, 6), (7, 8), (29, 10)]
tuple2 = [(1.2, 2.2), (14, 3), (36, 5), (8, 7), (20, 9)]
tuple3 = [(1.5, 2.5), (13.5, 14.5), (5.5, 6.5), (17.5, 8.5), (9.5, 20.5)]

# 调用 RANSAC 方法
tuples = [tuple1, tuple2, tuple3]
x0, y0, closest_points = ransac_find_x0_y0(tuples, threshold=1.5, iterations=1000)

print(f"Estimated x0, y0: ({x0}, {y0})")
print(f"Closest points in each tuple: {closest_points}")