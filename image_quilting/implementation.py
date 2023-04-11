from base import ImageQuilting, BoxIndeces, QuiltingOutputs

import typing
import numpy as np
import cv2
import scipy.ndimage as ndimage
import PIL.Image as Image
import imageio
import os

# SUBMISSION: You only need to submit this file 'implementation.py'

# Hint: You could refer to online sources for help as long as you cite it
# Hint: The entire implementation logic can be viewed in 'base.py'
# hint: Feel free to add as much helper functions in the class

# SCORE -1 if you imported additional modules
# SCORE +5 for submitting this file (bonus)


class ImageQuilting_AlgorithmAssignment(ImageQuilting):

    def find_matching_texture_patch_indeces(
        self,
        canvas_patch: np.ndarray,
        canvas_indeces: BoxIndeces,
        canvas: np.ndarray,
        block_size: int,
        block_overlap: int
    ) -> BoxIndeces:

        # SCORE +1 by iterating through all other possible patch locations//MAYBE DONE?
        def enumerate_other_indeces() -> typing.Sequence[BoxIndeces]:
            # Hint: use self.texture_image as reference
            # TODO: Replace this RANDOM implementation
            texture_height, texture_width, _ = self.texture_image.shape
            patch_height, patch_width, _ = canvas_patch.shape
            for y in range(texture_height - patch_height):
                for x in range(texture_width - patch_width):
                    if (y, x) == (canvas_box.top, canvas_box.left):
                        continue
                    yield BoxIndeces(
                        top=y,
                        bottom=y + patch_height,
                        left=x,
                        right=x + patch_width
            )

        # SCORE +1 by finding the overlap area in canvas_patch//MAYBE DONE?
        overlap_top = block_overlap.top - canvas_indeces.top
        overlap_bottom = overlap_top + block_overlap.height
        overlap_left = block_overlap.left - canvas_indeces.left
        overlap_right = overlap_left + block_overlap.width

    # Extract the overlap area from the canvas_patch
        canvas_overlap = canvas_patch[overlap_top:overlap_bottom, overlap_left:overlap_right, :]

        return canvas_overlap

        # SCORE +1 by finding the overlap area in patch
        def extract_overlap(patch: np.ndarray) -> np.ndarray:
            # Hint: use canvas_indeces, block_overlap

            # TODO: Replace this IDENTITY implementation
            return patch

        # SCORE +1 by finding the errors between between the overlapping patches
        def error_metric(a: np.ndarray, b: np.ndarray) -> float:
            # Hint: Use L2 loss ((a - b)**2).sum()

            # TODO: Replace this RANDOM implementation
            return np.random.random()

        canvas_overlap = extract_canvas_overlap()

        least_error: float = float("inf")
        least_error_indeces: BoxIndeces = None

        for other_indeces in enumerate_other_indeces():
            other_patch = self.extract_patch(self.texture_image, other_indeces)
            other_overlap = extract_overlap(other_patch)

            error = error_metric(canvas_overlap, other_overlap)
            if error < least_error:
                least_error = error
                least_error_indeces = other_indeces

        return least_error_indeces

    def compute_texture_mask(
        self,
        canvas_patch: np.ndarray,
        texture_patch: np.ndarray,
        canvas_indeces: BoxIndeces,
        texture_indeces: BoxIndeces,
        canvas: np.ndarray,
        block_size: int,
        block_overlap: int
    ) -> np.ndarray:
        texture_height, texture_width, _ = texture_patch.shape
        mask = np.ones((texture_height, texture_width))

        # SCORE +2 for implementing the core logic for finding the cut the minimizes the L2 error (minCut)
        # Hint: The implementation for minCut differs slightly for Left, Top, and Left-Top overlaps (see 'guide.jpg')
        # Hint: But as long as the core logic to at least one case is implemented, I'll give the points already
        # TODO: Implement minCut for at least one othe Overlap cases

        # SCORE +1 for returning the correct mask for the initialization (row=0, column=0)
        if canvas_indeces.top == 0 and canvas_indeces.left == 0:
            # TODO: bonus points, you don't need to do anything here
            return mask

        # SCORE +1 for returning the correct mask for Case 1: Left Overlap (row=0, column>1)
        if canvas_indeces.top == 0 and canvas_indeces.left != 0:
            # TODO: compute the mask properly (minCut), instead of this RANDOM implementation
            path_index = np.random.randint(0, block_overlap)
            path_index += np.random.choice([-1, 0, 1], size=texture_height).cumsum()
            path_index = np.clip(path_index, 0, block_overlap)

            for y in range(texture_height):
                mask[y, :path_index[y]] = 0

            return mask

        # SCORE +1 for returning the correct mask for Case 2: Top Overlap (row>1, column=0)
        if canvas_indeces.top != 0 and canvas_indeces.left == 0:
            # TODO: compute the mask properly (minCut), instead of this RANDOM implementation
            path_index = np.random.randint(0, block_overlap)
            path_index += np.random.choice([-1, 0, 1], size=texture_width).cumsum()
            path_index = np.clip(path_index, 0, block_overlap)

            for x in range(texture_width):
                mask[:path_index[x], x] = 0

            return mask

        # SCORE +1 for returning the correct mask for Case 3: Top-Left Overlap (row>1, column>1)
        if canvas_indeces.left != 0 and canvas_indeces.top != 0:
            # TODO: compute the mask properly (minCut), instead of this RANDOM implementation
            path_index = np.random.randint(0, block_overlap)
            path_index += np.random.choice([-1, 0, 1], size=texture_height).cumsum()
            path_index = np.clip(path_index, 0, block_overlap)

            for y in range(texture_height):
                mask[y, :path_index[y]] = 0

            path_index = np.random.randint(0, block_overlap)
            path_index += np.random.choice([-1, 0, 1], size=texture_width).cumsum()
            path_index = np.clip(path_index, 0, block_overlap)

            for x in range(texture_width):
                mask[:path_index[x], x] = 0

            return mask

        raise Exception("This code should not run")
