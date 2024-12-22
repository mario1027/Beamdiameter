
import numpy as np
from time import time
from typing import Tuple, Optional

import cv2
#import ctypes



def timeit(method):
    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed


#ok
def rotate_coordinates_around_center_around_center(
    x_coords: np.ndarray,
    y_coords: np.ndarray,
    center_x: float,
    center_y: float,
    angle_radians: float,
    clockwise: bool = True
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Rotate the points represented by x_coords and y_coords around the specified center (center_x, center_y)
    by the given angle (in radians).

    Args:
        x_coords (ndarray): x-coordinates of the points to be rotated.
        y_coords (ndarray): y-coordinates of the points to be rotated.
        center_x (float): x-coordinate of the center of rotation.
        center_y (float): y-coordinate of the center of rotation.
        angle_radians (float): Angle by which to rotate the points (positive values rotate counterclockwise).
        clockwise (bool, optional): If True, rotates clockwise; if False (default), rotates counterclockwise.

    Returns:
        A tuple containing the new x and y coordinates of the rotated points.
        
    Raises:
        ValueError: If x_coords and y_coords have different lengths.
    """
    if len(x_coords) != len(y_coords):
        raise ValueError("x_coords and y_coords must have the same length")

    if clockwise:
        angle_radians = -angle_radians

    relative_x = x_coords - center_x
    relative_y = y_coords - center_y

    sin_angle, cos_angle = np.sin(angle_radians), np.cos(angle_radians)

    rotated_x = relative_x * cos_angle - relative_y * sin_angle
    rotated_y = relative_x * sin_angle + relative_y * cos_angle

    new_x_coords = rotated_x + center_x
    new_y_coords = rotated_y + center_y

    return new_x_coords, new_y_coords


#ok
def get_pixel_values_along_line(image: np.ndarray, start_x: float, start_y: float, end_x: float, end_y: float, num_points: int = 100) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Return x, y, z, and distance values between (start_x, start_y) and (end_x, end_y).
    
    Parameters:
        image (ndarray): The image to work with.
        start_x (float): The x-value of the start of the line.
        start_y (float): The y-value of the start of the line.
        end_x (float): The x-value of the end of the line.
        end_y (float): The y-value of the end of the line.
        num_points (int): The number of points in the returned array. Default is 100.
    
    Returns:
        A tuple containing:
        - x_indices (ndarray): The index of horizontal pixel values along the line.
        - y_indices (ndarray): The index of vertical pixel values along the line.
        - pixel_values (ndarray): The image values at each of the x, y positions.
        - distances (ndarray): The distance from the start of the line to the x, y position.
    """
    if not isinstance(image, np.ndarray):
        raise ValueError("The 'image' parameter must be a NumPy array.")
    
    if num_points <= 0:
        raise ValueError("num_points must be a positive integer.")
    
    # Calculate the total length of the line segment
    line_length = np.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
    
    if num_points == 1:
        # Handle the special case when num_points is 1
        x_indices = np.array([start_x])
        y_indices = np.array([start_y])
    else:
        # Generate a linearly spaced array of num_points along the line
        normalized_distances = np.linspace(0, 1, num_points)

        # Calculate the x and y coordinates of points along the line
        x_indices = start_x + normalized_distances * (end_x - start_x)
        y_indices = start_y + normalized_distances * (end_y - start_y)

    # Convert x and y coordinates to integer indices for pixel values
    x_rounded = np.round(x_indices).astype(int)
    y_rounded = np.round(y_indices).astype(int)

    # Retrieve image values at each x, y position
    if not ((x_rounded < 0).all() or (x_rounded >= image.shape[1]).all() or (y_rounded < 0).all() or (y_rounded >= image.shape[0]).all()):
        pixel_values = image[y_rounded, x_rounded]
    else:
        pixel_values = image

    # Calculate the distance from the start of the line to each x, y position
    normalized_distances_from_start = (normalized_distances - 0.5) * line_length

    # Return the x and y indices, image values, and distance values
    return x_rounded, y_rounded, pixel_values, normalized_distances_from_start


#ok
def get_major_axis_values(image: np.ndarray, center_x: float, center_y: float, major_axis_length: float, minor_axis_length: float, rotation_angle: float, num_diameters: int = 3) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Return x, y, z, and distance values along the semi-major axis of an elliptical beam.

    Parameters:
        image (ndarray): The image to work with.
        center_x (float): The horizontal center of the ellipse.
        center_y (float): The vertical center of the ellipse.
        major_axis_length (float): The length of the major axis of the ellipse.
        minor_axis_length (float): The length of the minor axis of the ellipse.
        rotation_angle (float): The angle by which the elliptical beam is rotated (in radians).
        num_diameters (int): The number of diameters to use.

    Returns:
        A tuple containing the x, y, z, and distance values along the semi-major axis of the elliptical beam.
    """
    # Get the dimensions of the image
    image_height, image_width = image.shape

    # Determine whether the major axis or minor axis is longer
    if major_axis_length > minor_axis_length:
        # Calculate the length of the semi-major axis
        semi_major_axis_length = num_diameters * major_axis_length / 2
        
        # Calculate the x-coordinates of the left and right endpoints of the semi-major axis
        left_x = max(center_x - semi_major_axis_length, 0)
        right_x = min(center_x + semi_major_axis_length, image_width - 1)
        
        # Define the initial x and y coordinates of the semi-major axis
        x_coords = np.array([left_x, right_x])
        y_coords = np.array([center_y, center_y])
        
        # Rotate the coordinates around the center
        rotated_x_coords, rotated_y_coords = rotate_coordinates_around_center_around_center(x_coords, y_coords, center_x, center_y, rotation_angle)
    else:
        # Calculate the length of the semi-minor axis
        semi_minor_axis_length = num_diameters * minor_axis_length / 2
        
        # Calculate the y-coordinates of the top and bottom endpoints of the semi-minor axis
        top_y = max(center_y - semi_minor_axis_length, 0)
        bottom_y = min(center_y + semi_minor_axis_length, image_height - 1)
        
        # Define the initial x and y coordinates of the semi-minor axis
        x_coords = np.array([center_x, center_x])
        y_coords = np.array([top_y, bottom_y])
        
        # Rotate the coordinates around the center
        rotated_x_coords, rotated_y_coords = rotate_coordinates_around_center_around_center(x_coords, y_coords, center_x, center_y, rotation_angle)

    # Get pixel values and distances along the semi-major axis
    return get_pixel_values_along_line(image, rotated_x_coords[0], rotated_y_coords[0], rotated_x_coords[1], rotated_y_coords[1])


import numpy as np
#ok
def get_minor_axis_values(image: np.ndarray, center_x: float, center_y: float, major_axis_length: float, minor_axis_length: float, rotation_angle: float, num_diameters: int = 3) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Return arrays of x, y, z, and s values along the semi-minor axis of an ellipse.

    Parameters
    ----------
    image : array_like
        Input image.
    center_x, center_y : float
        Coordinates of the center of the ellipse.
    major_axis_length, minor_axis_length : float
        Lengths of the major and minor axes of the ellipse, respectively.
    rotation_angle : float
        Angle (in radians) of rotation of the ellipse.
    num_diameters : int, optional
        Number of diameters to include in the output arrays.

    Returns
    -------
    x_coords : ndarray
        Array of x-coordinates of the pixels along the semi-minor axis.
    y_coords : ndarray
        Array of y-coordinates of the pixels along the semi-minor axis.
    pixel_values : ndarray
        Array of image values at each of the (x, y) positions.
    distances : ndarray
        Array of distances along the semi-minor axis from the start point to each (x, y) position.
    """
    height, width = image.shape

    if major_axis_length <= minor_axis_length:
        radius_x = num_diameters * major_axis_length / 2
        left = max(center_x - radius_x, 0)
        right = min(center_x + radius_x, width - 1)
        x_coords = np.array([left, right])
        y_coords = np.full_like(x_coords, center_y)
    else:
        radius_y = num_diameters * minor_axis_length / 2
        top = max(center_y - radius_y, 0)
        bottom = min(center_y + radius_y, height - 1)
        y_coords = np.array([top, bottom])
        x_coords = np.full_like(y_coords, center_x)

    rotated_x, rotated_y = rotate_coordinates_around_center(x_coords, y_coords, center_x, center_y, rotation_angle)

    return get_pixel_values_along_line(image, rotated_x[0], rotated_y[0], rotated_x[1], rotated_y[1])







def first_order_moments(image: np.ndarray, image_width: int, image_height: int, total_pixels: float) -> Tuple[float, float, float, float]:
    """
    Calculates the first-order moments, i.e., the centroid, from a laser beam image.

    Args:
        image (np.ndarray): A 2D numpy array representing the laser beam point image.
        image_width (int): Width of the image in pixels.
        image_height (int): Height of the image in pixels.
        total_pixels (float): The total pixel value in the image.

    Returns:
        Tuple[float, float, float, float, float]: A tuple containing:
            - center_x (float): The horizontal coordinate of the laser beam center.
            - horizontal_indices (float): Horizontal indices used for additional calculations (not the final result).
            - center_y (float): The vertical coordinate of the laser beam center.
            - vertical_indices (float): Vertical indices used for additional calculations (not the final result).
            - total_pixels (float): The total pixel value in the image.

    This function calculates the first-order moments, i.e., the centroid of the laser beam from a given image. First-order moments are used to determine the position of the beam center.

    To calculate the centroid, it sums the products of pixel values with their respective coordinates on the horizontal and vertical axes. Then, it divides this sum by the total pixel value in the image to obtain the centroid.

    It's important to ensure that the image is provided as a valid 2D numpy array, and that the total pixel value is not zero to avoid errors.

    Args:
        image: A 2D numpy array representing the laser beam image.
        image_width: Width of the image in pixels.
        image_height: Height of the image in pixels.
        total_pixels: The total pixel value in the image.

    Returns:
        A tuple containing the centroid and other auxiliary values.
    """
    # Create horizontal and vertical indices for calculations
    horizontal_indices = np.arange(image_width, dtype=float)
    vertical_indices = np.arange(image_height, dtype=float)

    # Calculate the centroid on the X-axis
    center_x = np.sum(image.dot(horizontal_indices)) / total_pixels

    # Calculate the centroid on the Y-axis
    center_y = np.sum(image.T.dot(vertical_indices)) / total_pixels

    return center_x, horizontal_indices, center_y, vertical_indices



def second_order_moments(image: np.ndarray, center_x: float, center_y: float, horizontal_indices: np.ndarray, vertical_indices: np.ndarray, total_pixels: float) -> Tuple[float, float, float]:
    """
    Calculate second-order moments (variances and covariance) from an image around a given centroid.

    Args:
        image (np.ndarray): A 2D numpy array representing the image.
        center_x (float): The horizontal coordinate of the centroid.
        center_y (float): The vertical coordinate of the centroid.
        horizontal_indices (np.ndarray): Horizontal indices for calculations.
        vertical_indices (np.ndarray): Vertical indices for calculations.
        total_pixels (float): The total pixel value in the image.

    Returns:
        Tuple[float, float, float]: A tuple containing:
            - xx (float): Variance in the horizontal direction.
            - xy (float): Covariance between horizontal and vertical shifts.
            - yy (float): Variance in the vertical direction.
    """
    # Calculate horizontal and vertical shifts from the centroid
    horizontal_shifts = horizontal_indices - center_x
    vertical_shifts = vertical_indices - center_y

    # Calculate the variance in the horizontal direction (xx)
    xx = np.sum(image.dot(horizontal_shifts**2)) / total_pixels

    # Calculate the covariance between horizontal and vertical shifts (xy)
    xy = np.sum(image.T.dot(vertical_shifts).dot(horizontal_shifts)) / total_pixels
    

    # Calculate the variance in the vertical direction (yy)
    yy = np.sum(image.T.dot(vertical_shifts**2)) / total_pixels

    return xx, xy, yy


#ok
def detect_beam_size(image: np.ndarray) -> Tuple[float, float, float, float, float]:
    """
    Calculate laser beam parameters center, diameter and angle at which the elliptical beam is rotated using ISO 11146 standard.

    Args:
        image (np.ndarray): A 2D numpy array representing the image with the laser beam spot.

    Returns:
        Tuple[float, float, float, float, float]: A tuple containing:
            - center_x (float): The horizontal center of the laser beam.
            - center_y (float): The vertical center of the laser beam.
            - diameter_x (float): The horizontal diameter of the laser beam.
            - diameter_y (float): The vertical diameter of the laser beam.
            - tilt_angle (float): The angle at which the elliptical beam is rotated [radians].

    This function utilizes the ISO 11146 standard for a comprehensive analysis of laser beams, 
    enabling the determination of critical parameters. It calculates the beam's center, 
    diameters (both horizontal and vertical), and tilt angle, essential for characterizing 
    laser beam properties.

    Note that this function does not perform background noise elimination. Instead, it focuses 
    on computing the first and second-order moments to extract beam parameters. Consequently, 
    the function may not provide accurate results in the presence of constant background noise in the image.

    It's worth mentioning that this implementation provides a substantial performance boost 
    compared to methods using for loops. In scenarios where background noise dominates, 
    a diameter of 1 is returned.

    Args:
        image: A 2D numpy array representing the image with the beam spot.

    Returns:
        A tuple of five floats (center_x, center_y, diameter_x, diameter_y, tilt_angle) representing:
            - center_x: The horizontal center of the beam.
            - center_y: The vertical center of the beam.
            - diameter_x: The horizontal diameter of the beam.
            - diameter_y: The vertical diameter of the beam.
            - tilt_angle: The angle that the elliptical beam is rotated [radians].
    """
    # Get the dimensions (height and width) of the image.
    image_height, image_width = image.shape

    # Calculate the total sum of all pixel values in the image.
    total_pixels = np.sum(image, dtype=float)

    # Handle the case when the image is all zeros or not a valid NumPy array.
    if total_pixels == 0 or not isinstance(image, np.ndarray):
        return float(image_width) / 2, float(image_height) / 2, float(image_width), float(image_height), 0

    # Calculate first-order moments to obtain the center coordinates.
    center_x, horizontal_indices, center_y, vertical_indices = first_order_moments(image, image_width, image_height, total_pixels)

    # Calculate second-order moments to determine the variances and covariance.
    xx, xy, yy = second_order_moments(image, center_x, center_y, horizontal_indices, vertical_indices, total_pixels)

    # Handle cases when xx is equal to yy to avoid division by zero.
    if xx == yy:
        disc = np.abs(2 * xy)
        tilt_angle = np.sign(xy) * np.pi / 4
    else:
        diff = xx - yy
        disc = np.sign(diff) * np.sqrt(diff**2 + 4 * xy**2)
        tilt_angle = 0.5 * np.arctan(2 * xy / diff)

    # Calculate the major and minor diameters of the elliptical beam.
  
    diameter_x = np.sqrt(8 * (xx + yy + disc))
    diameter_y = np.sqrt(8 * (xx + yy - disc))
  

    # Invert the image, so the tilt angle is represented negatively.
    tilt_angle *= -1

    return center_x, center_y, diameter_x, diameter_y, tilt_angle







def subtract_iso_background(image: np.ndarray,
                            background_fraction: float = 0.035,
                            nT: int = 3,
                            iso_noise: bool = True) -> np.ndarray:
    """
    Return image with ISO 11146 background subtracted.

    Args:
        image: the image to work with
        background_fraction: the fractional size of corner rectangles
        nT: how many standard deviations to subtract
        iso_noise: whether to apply iso noise or not

    Returns:
        image: 2D array with background subtracted
    """
    back, sigma = iso_background(image, background_fraction=background_fraction, nT=nT)

    subtracted = image.astype(float)
    subtracted -= back

    if not iso_noise:  # zero pixels that fall within a few stdev
        threshold = nT * sigma
        np.place(subtracted, subtracted < threshold, 0)

    return subtracted

def iso_background(image: np.ndarray,
                   background_fraction: float = 0.035,
                   nT: int = 3) -> Tuple[float, float]:
    """
    Return the background for unilluminated pixels in an image.

    Args:
        image: the image to work with
        nT: how many standard deviations to subtract
        background_fraction: the fractional size of corner rectangles

    Returns:
        mean, stdev: mean and stdev of background in the image
    """
   

    # estimate background
    ave, std = determine_image_background(image, background_fraction=background_fraction)

    # defined ISO/TR 11146-3:2004, equation 59
    threshold = ave + nT * std

    # collect all pixels that fall below the threshold
    unilluminated = image[image <= threshold]

    if len(unilluminated) == 0:
        raise ValueError('est bkgnd=%.2f stdev=%.2f. No values in image are <= %.2f.'
                         % (ave, std, threshold))

    mean = np.mean(unilluminated)
    stdev = np.std(unilluminated)
    return mean, stdev

def determine_image_background(image: np.ndarray, background_fraction: float = 0.035) -> Tuple[float, float]:
    """
    Return the mean and stdev of background in corners of image.

    Args:
        image: the image to work with
        background_fraction: the fractional size of corner rectangles

    Returns:
        corner_mean: average pixel value in corners
    """
    if background_fraction == 0:
        return 0, 0
    mask = corner_mask(image, background_fraction)
    img = np.ma.masked_array(image, ~mask)
    mean = np.mean(img)
    stdev = np.std(img)
    return mean, stdev

def corner_mask(image: np.ndarray, background_fraction: float = 0.035) -> np.ndarray:
    """
    Create boolean mask for image with corners marked as True.

    Args:
        image: the image to work with
        background_fraction: the fractional size of corner rectangles

    Returns:
        masked_image: 2D array with True values in four corners
    """
    v, h = image.shape
    n = int(v * background_fraction)
    m = int(h * background_fraction)

    the_mask = np.full_like(image, False, dtype=bool)
    the_mask[:n, :m] = True
    the_mask[:n, -m:] = True
    the_mask[-n:, :m] = True
    the_mask[-n:, -m:] = True
    return the_mask








def generate_rotated_rectangle_mask(image: np.ndarray, center_x: float, center_y: float, major_axis_length: float, minor_axis_length: float, rotation_angle: float, scaling_factor: int = 3) -> np.ndarray:
    """
    Generate a rotated rectangular mask for beam integration in an image.

    This function creates a binary mask for integrating the region of interest (ROI) of a beam in an image.
    The mask is rectangular, centered on the beam centroid, oriented parallel to the principal axes of
    the beam's power density distribution, and sized based on the specified number of diameters.

    Args:
        image (np.ndarray): The input image to work with.
        center_x (float): Horizontal center of the beam.
        center_y (float): Vertical center of the beam.
        major_axis_length (float): Length of the ellipse along the major axis.
        minor_axis_length (float): Length of the ellipse along the minor axis.
        rotation_angle (float): Angle in radians by which the elliptical beam is rotated.
        scaling_factor (int, optional): Number of diameters to include in the rectangular mask.
            Defaults to 3.

    Returns:
        np.ndarray: A 2D binary mask with 'True' values inside the rectangular region of interest.

    Notes:
        - The rectangular mask is rotated about the specified center (center_x, center_y).
        - The scaling_factor parameter determines the size of the mask relative to the
          diameters of the ellipse, with 3 being a common value.
        - The mask can be used for beam integration within the specified region of interest.

    Example:
        # Generate a rotated rectangular mask for a beam centered at (50, 50),
        # with a major axis of 10, a minor axis of 20, rotated by 45 degrees,
        # and a mask size of 3 diameters.
        mask = generate_rotated_rectangle_mask(image, 50, 50, 10, 20, np.pi / 4, scaling_factor=3)
    """
    
    # Calculate the dimensions of the rectangular mask based on the specified number of diameters
    mask_width = scaling_factor * major_axis_length
    mask_height = scaling_factor * minor_axis_length

    # Create a binary mask initialized with zeros
    mask = np.zeros(image.shape, dtype=np.uint8)

    # Calculate the coordinates of the rotated rectangle vertices
    vertices = cv2.boxPoints(((center_x, center_y), (mask_width, mask_height), np.degrees(rotation_angle)))
    vertices = np.array(vertices, dtype=np.int32)


    # Fill the mask with '1' values inside the rotated rectangle using cv2.fillConvexPoly
    cv2.fillConvexPoly(mask, vertices, 1)

    return mask




def get_ellipse_axes(x_center: float, y_center: float, horizontal_diameter: float, vertical_diameter: float, rotation_angle: float,
                    scaling_factor: int = 3) -> np.ndarray:
    """
    Return x, y arrays needed to draw semi-axes of an ellipse.

    This function calculates the coordinates of the semi-axes of an ellipse, which are used
    for drawing the ellipse. The ellipse can be rotated and scaled based on the provided
    parameters.

    Args:
        x_center (float): Horizontal center of the ellipse.
        y_center (float): Vertical center of the ellipse.
        horizontal_diameter (float): Diameter of the ellipse for the horizontal axis.
        vertical_diameter (float): Diameter of the ellipse for the vertical axis.
        rotation_angle (float): Angle in radians by which the ellipse is rotated.
        scaling_factor (int): A scaling factor for the size of the axes. Default is 3.

    Returns:
        np.ndarray: A 2D numpy array containing the x and y coordinates of the semi-axes of the ellipse.

    Raises:
        ValueError: If horizontal_diameter, vertical_diameter, or scaling_factor is non-positive.

    Example:
        # Get coordinates for drawing the semi-axes of an ellipse with a horizontal diameter of 10,
        # vertical diameter of 20, centered at (50, 50), and rotated by 45 degrees.
        axes_coords = get_ellipse_axes(50, 50, 10, 20, np.pi / 4, scaling_factor=3)
    """
  

    # Calculate scaled semi-axes based on the scaling_factor
    x_radius = scaling_factor * horizontal_diameter / 2
    y_radius = scaling_factor * vertical_diameter / 2

    # Define the x and y coordinates of the semi-axes with the center at (x_center, y_center)
    x_coords = np.array([-x_radius, x_radius, 0, 0, 0]) + x_center
    y_coords = np.array([0, 0, 0, -y_radius, y_radius]) + y_center

    # Rotate the semi-axes to account for the specified rotation angle (rotation_angle)
    x_rot, y_rot = rotate_coordinates_around_center(x_coords, y_coords, x_center, y_center, rotation_angle)

    # Return the semi-axes as a 2D numpy array containing both x and y coordinates
    return np.array([x_rot, y_rot])



def measure_beam_size(image: np.ndarray, scaling_factor: float = 3, background_fraction: float = 0.035,
                      nT: float = 3, max_iter: int = 25, phi: Optional[float] = None,iso_noise: bool = True) -> Tuple[float, float, float, float, float]:
    """
    Determine beam parameters in an image with noise.

    This function estimates the beam parameters (center, diameter, and orientation angle) in an image.
    It follows ISO 11146 standards for beam parameter determination.

    Args:
        image: A 2D array representing the image of the beam.
        scaling_factor: The size of the integration rectangle in diameters of the ellipse.
        background_fraction: The fractional size of the corners used to estimate the background.
        nT: A multiple of background noise used to remove noise from the background estimate.
        max_iter: Maximum number of iterations for refining the beam parameters.
        phi: (Optional) Fixed tilt of the ellipse in radians.

    Returns:
        xc: Horizontal center of the beam.
        yc: Vertical center of the beam.
        dx: Horizontal diameter of the beam.
        dy: Vertical diameter of the beam.
        phi: Angle that defines the orientation of the elliptical beam.
    """
    # Check if the input image is grayscale; color images are not supported
    if len(image.shape) > 2:
        raise Exception('Color images are not supported. Convert to gray/monochrome.')

    # Initialize parameters with an initial estimate
    image_no_bkgnd = subtract_iso_background(image,
                                                background_fraction=background_fraction,
                                                nT=nT,
                                                iso_noise=False)
    xc, yc, dx, dy, phi_ = detect_beam_size(image_no_bkgnd)
    if iso_noise:  # follow iso background guidelines (positive & negative bkgnd values)
        image_no_bkgnd = subtract_iso_background(image,
                                                    background_fraction=background_fraction,
                                                    nT=nT,
                                                    iso_noise=True)
    # Refinement loop
    for iteration in range(max_iter):
        # Use the provided phi or the latest estimated phi
        phi_ = phi or phi_

        # Store previous parameters for convergence check
        prev_xc, prev_yc, prev_dx, prev_dy = xc, yc, dx, dy

        # Generate a rotated rectangle mask for integration
        mask = generate_rotated_rectangle_mask(image, xc, yc, dx, dy, phi_, scaling_factor)

        # Apply the mask to the original image
        masked_image = np.copy(image_no_bkgnd)
        masked_image[mask < 0.5] = 0

        # Refine the beam parameters using the masked image
        xc, yc, dx, dy, phi_ = detect_beam_size(masked_image)

        # Check for convergence by comparing changes in parameters
        if abs(xc - prev_xc) < 1 and abs(yc - prev_yc) < 1 and abs(dx - prev_dx) < 1 and abs(dy - prev_dy) < 1:
            break

    return xc, yc, dx, dy, phi_



def crop_image_to_integration_rectangle(image: np.ndarray, ellipse_center_x: float, ellipse_center_y: float, ellipse_width: float, ellipse_height: float, ellipse_rotation: float):
    """
    Crop an image to an integration rectangle defined by a rotated ellipse.

    This function takes an input image and crops it to an integration rectangle defined by a rotated ellipse. The rotation angle, center coordinates, and dimensions of the ellipse are provided as arguments.

    Args:
        image (numpy.ndarray): The input image.
        ellipse_center_x (float): Horizontal center of the ellipse.
        ellipse_center_y (float): Vertical center of the ellipse.
        ellipse_width (float): Width of the ellipse.
        ellipse_height (float): Height of the ellipse.
        ellipse_rotation (float): Angle (in radians) by which the ellipse is rotated.

    Returns:
        numpy.ndarray: The cropped image.
        float: The new horizontal position of the ellipse center in the cropped image.
        float: The new vertical position of the ellipse center in the cropped image.
    """
    # Calculate coordinates of the rotated rectangle that encloses the ellipse
    rectangle_x, rectangle_y = rotated_rectangle_vertices(ellipse_center_x, ellipse_center_y, ellipse_width, ellipse_height, ellipse_rotation, scaling_factor=3)
    
    # Crop the image to the rectangular region defined by the rotated rectangle
    cropped_image = crop_image_to_rectangular(image, ellipse_center_x, ellipse_center_y, np.min(rectangle_x), np.max(rectangle_x), np.min(rectangle_y), np.max(rectangle_y))

    return cropped_image





def rotated_rectangle_vertices(center_x: float, center_y: float, width: float, height: float, rotation_angle: float, scaling_factor: int = 3):
    """
    Return x, y arrays to define the vertices of a rotated rectangle.

    This function calculates and returns the x, y coordinates of the vertices of a rotated rectangle. The rectangle is centered at (center_x, center_y) and is defined by its dimensions (width, height) and rotation angle (rotation_angle) in radians.

    Args:
        center_x (float): Horizontal center of the rotated rectangle.
        center_y (float): Vertical center of the rotated rectangle.
        width (float): Width of the rectangle (along the horizontal axis).
        height (float): Height of the rectangle (along the vertical axis).
        rotation_angle (float): Angle (in radians) by which the rectangle is rotated.
        scaling_factor (int, optional): Scaling factor for the rectangle's dimensions (default is 3).

    Returns:
        numpy.ndarray: Array of x-coordinates of the rectangle's vertices.
        numpy.ndarray: Array of y-coordinates of the rectangle's vertices.
    """
    # Calculate the half-dimensions of the rectangle scaled by the scaling_factor
    half_width = scaling_factor * width / 2
    half_height = scaling_factor * height / 2

    # Define the x and y coordinates of the rectangle's vertices
    x_unrotated = np.array([-half_width, -half_width, +half_width, +half_width, -half_width]) + center_x
    y_unrotated = np.array([-half_height, +half_height, +half_height, -half_height, -half_height]) + center_y

    # Rotate the points to obtain the coordinates of the rotated rectangle
    x_rotated, y_rotated = rotate_coordinates_around_center(x_unrotated, y_unrotated, center_x, center_y, rotation_angle)

    return x_rotated, y_rotated




def crop_image_to_rectangular(image: np.ndarray, beam_center_x: float, beam_center_y: float, left_x: float, right_x: float, top_y: float, bottom_y: float):
    """
    Crop an image to the specified rectangular region.

    This function crops an input image to the specified rectangular region defined by its coordinates (left_x, top_y, right_x, bottom_y).
    
    Args:
        image (numpy.ndarray): The image to be cropped.
        beam_center_x (float): The horizontal center of the beam.
        beam_center_y (float): The vertical center of the beam.
        left_x (float): The left edge of the rectangular region in pixels.
        right_x (float): The right edge of the rectangular region in pixels.
        top_y (float): The top edge of the rectangular region in pixels.
        bottom_y (float): The bottom edge of the rectangular region in pixels.

    Returns:
        Tuple[numpy.ndarray, float, float]: A tuple containing:
            - cropped_image (numpy.ndarray): The cropped image.
            - new_beam_center_x (float): The new horizontal center of the beam in pixels after cropping.
            - new_beam_center_y (float): The new vertical center of the beam in pixels after cropping.
    """
    # Get the height and width of the input image
    image_height, image_width = image.shape
    
    # Ensure that the specified coordinates are within the image boundaries
    left_x = max(0, int(left_x))
    right_x = min(image_width, int(right_x))
    top_y = max(0, int(top_y))
    bottom_y = min(image_height, int(bottom_y))
    
    # Ensure that the minimum coordinates are not greater than the maximum coordinates
    left_x, right_x = min(left_x, right_x), max(left_x, right_x)
    top_y, bottom_y = min(top_y, bottom_y), max(top_y, bottom_y)
    
    # Calculate the new horizontal and vertical centers after cropping
    new_beam_center_x = beam_center_x - left_x
    new_beam_center_y = beam_center_y - top_y
    
    # Crop the image to the specified rectangular region
    cropped_image = image[top_y:bottom_y, left_x:right_x]
    
    return cropped_image, new_beam_center_x, new_beam_center_y



def rotate_coordinates_around_center(x: np.ndarray, y: np.ndarray, center_x: float, center_y: float, angle_rad: float):
    """
    Rotate a set of points (x, y) around a specified center (center_x, center_y) by a given angle (angle_rad).

    Args:
        x (numpy.ndarray or float): X-coordinates of the points to be rotated.
        y (numpy.ndarray or float): Y-coordinates of the points to be rotated.
        center_x (float): The horizontal center of rotation.
        center_y (float): The vertical center of rotation.
        angle_rad (float): The angle by which to rotate the points in radians (positive for counterclockwise rotation).

    Returns:
        Tuple[numpy.ndarray, numpy.ndarray]: A tuple containing the rotated X and Y coordinates of the points.

    Example:
        >>> x = np.array([1, 2, 3])
        >>> y = np.array([4, 5, 6])
        >>> center_x = 2.5
        >>> center_y = 5.0
        >>> angle_rad = np.pi / 2  # Rotate 90 degrees counterclockwise
        >>> rotate_coordinates_around_center(x, y, center_x, center_y, angle_rad)
        (array([6., 5., 4.]), array([2., 2., 2.]))
    """
    # Calculate the sine and cosine of the rotation angle
    sin_angle = np.sin(angle_rad)
    cos_angle = np.cos(angle_rad)

    # Translate the points to the origin and apply the rotation transformation
    translated_x = x - center_x
    translated_y = y - center_y
    rotated_x = translated_x * cos_angle - translated_y * sin_angle  # X coordinate after rotation
    rotated_y = translated_x * sin_angle + translated_y * cos_angle  # Y coordinate after rotation

    # Translate the points back to their original position
    final_x = rotated_x + center_x
    final_y = rotated_y + center_y

    return final_x, final_y

# @software{prahl_2023_10214838,
#   author       = {Prahl, Scott},
#   title        = {{laserbeamsize: a python module for ISO 11146 
#                    analysis of laser beams}},
#   month        = nov,
#   year         = 2023,
#   publisher    = {Zenodo},
#   version      = {2.0.0},
#   doi          = {10.5281/zenodo.10214838},
#   url          = {https://doi.org/10.5281/zenodo.10214838}
# }
