import math

def calculate_horizontal_angle(x1, y1, x2, y2):
    # Calculate differences
    delta_x = x2 - x1
    delta_y = y2 - y1
    
    # Calculate the angle in radians
    angle_rad = math.atan2(delta_y, delta_x)
        
    return angle_rad

# # Example usage
# x1, y1 = 0, 0
# x2, y2 = 3, 4

# angle = calculate_horizontal_angle(x1, y1, x2, y2)
# print(f"The horizontal angle is {angle} radians")

def calculate_horizontal_vertical_distances(distance, angle_rad):
    # Calculate horizontal and vertical distances
    horizontal_distance = distance * math.cos(angle_rad)
    vertical_distance = distance * math.sin(angle_rad)
    
    return horizontal_distance, vertical_distance

# # Example usage
# distance = 10
# angle_rad = 1 / 2

# horizontal_distance, vertical_distance = calculate_horizontal_vertical_distances(distance, angle_rad)
# print(f"Horizontal Distance: {horizontal_distance}")
# print(f"Vertical Distance: {vertical_distance}")
