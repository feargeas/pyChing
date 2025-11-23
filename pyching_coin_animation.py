##---------------------------------------------------------------------------##
##
## pyChing -- a Python program to cast and interpret I Ching hexagrams
##
## Copyright (C) 1999-2006 Stephen M. Gava
## Copyright (C) 2025 Current Maintainers
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
##---------------------------------------------------------------------------##
"""
Coin animation module for pyChing GUI

Provides animated coin flipping for I Ching hexagram casting.
Separated from main GUI code for modularity and maintainability.
"""

import time
from typing import List, Optional


class CoinAnimator:
    """
    Handles animated coin flipping display for I Ching readings.

    This class provides a clean interface for animating the coin flip
    process, independent of the casting engine or reading structure.
    """

    def __init__(self, coin_labels, coin_images, master):
        """
        Initialize the coin animator.

        Args:
            coin_labels: List of 3 tkinter Label widgets for displaying coins
            coin_images: CoinImages object with coinFrames attribute
            master: Tkinter root/master widget for update_idletasks()
        """
        self.coin_labels = coin_labels
        self.coin_images = coin_images
        self.master = master

    def animate_full_reading(self, reading, delay=0.02, spins=2, pause_between_lines=0.5):
        """
        Animate the complete casting process for all 6 lines.

        This simulates the traditional line-by-line casting experience,
        showing coin flips for each line of the hexagram.

        Args:
            reading: A Reading object from HexagramEngine
            delay: Time in seconds between animation frames (default 0.02)
            spins: Number of complete spin cycles (default 2)
            pause_between_lines: Pause in seconds after each line (default 0.5)
        """
        # Get line values from the primary hexagram (6 lines, bottom to top)
        line_values = reading.primary.line_values

        # For each line, we need to determine what coin combination created it
        # Line values are 6, 7, 8, 9 but we need coin faces for display
        for line_idx in range(6):
            line_value = line_values[line_idx]

            # Determine coin display values from line value
            # In I Ching: 2+2+2=6 (old yin), 2+2+3=7 (young yang),
            #            2+3+3=8 (young yin), 3+3+3=9 (old yang)
            coin_display_values = self._line_value_to_coin_display(line_value)

            # Animate the coin flip for this line
            self._animate_single_flip(coin_display_values, delay, spins)

            # Pause to let user see the result
            if line_idx < 5:  # Don't pause after the last line
                time.sleep(pause_between_lines)

    def _line_value_to_coin_display(self, line_value: int) -> List[int]:
        """
        Convert a line value (6, 7, 8, 9) to coin display indices.

        The coin images use indices:
        - 14 for Yin face (value 2)
        - 15 for Yang face (value 3)

        Args:
            line_value: The I Ching line value (6, 7, 8, or 9)

        Returns:
            List of 3 integers representing coin face display indices
        """
        # Map line values to typical coin combinations
        # These are the frames: coinFrameYinData=14, coinFrameYangData=15
        coin_map = {
            6: [14, 14, 14],  # old yin: 2+2+2 (three yin faces)
            7: [14, 14, 15],  # young yang: 2+2+3
            8: [14, 15, 15],  # young yin: 2+3+3
            9: [15, 15, 15],  # old yang: 3+3+3 (three yang faces)
        }
        return coin_map.get(line_value, [14, 14, 15])  # Default to young yang

    def _animate_single_flip(self, final_display_values: List[int], delay: float, spins: int):
        """
        Animate a single coin flip sequence.

        Args:
            final_display_values: List of 3 coin frame indices to show at end
            delay: Time between frames in seconds
            spins: Number of complete spin cycles
        """
        # Animate the spinning (frames 0-13 are the animation)
        for _ in range(spins):
            for frame_num in range(14):
                # Update all three coins with the same frame (synchronized flip)
                for coin_label in self.coin_labels:
                    coin_label.configure(image=self.coin_images.coinFrames[frame_num])
                self.master.update_idletasks()
                time.sleep(delay)

        # Show the final coin faces
        for i, display_value in enumerate(final_display_values):
            self.coin_labels[i].configure(image=self.coin_images.coinFrames[display_value])
            self.master.update_idletasks()

    def clear_coins(self):
        """Clear/blank all coin displays."""
        blank_frame = 16  # coinFrameBlankData is at index 16
        for coin_label in self.coin_labels:
            coin_label.configure(image=self.coin_images.coinFrames[blank_frame])
        self.master.update_idletasks()

    def set_coins_initial(self):
        """Set coins to initial/frame 0 state."""
        for coin_label in self.coin_labels:
            coin_label.configure(image=self.coin_images.coinFrames[0])
        self.master.update_idletasks()
