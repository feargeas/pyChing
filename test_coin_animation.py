#!/usr/bin/env python3
"""
Quick test of CoinAnimator logic without requiring tkinter GUI
"""

from pyching_coin_animation import CoinAnimator


class MockLabel:
    """Mock tkinter Label for testing"""
    def __init__(self):
        self.image = None

    def configure(self, **kwargs):
        if 'image' in kwargs:
            self.image = kwargs['image']


class MockImages:
    """Mock coin images object"""
    def __init__(self):
        # Simulate 17 coin frames (0-16)
        self.coinFrames = list(range(17))


class MockMaster:
    """Mock tkinter master/root"""
    def update_idletasks(self):
        pass  # No-op for testing


class MockReading:
    """Mock Reading object"""
    def __init__(self):
        self.primary = MockHexagram()


class MockHexagram:
    """Mock Hexagram with line values"""
    def __init__(self):
        # Example: mix of line types
        self.line_values = [6, 7, 8, 9, 7, 8]  # old yin, young yang, young yin, old yang, young yang, young yin


def test_coin_animator():
    """Test the CoinAnimator logic"""
    print("Testing CoinAnimator...")

    # Create mock objects
    coin_labels = [MockLabel() for _ in range(3)]
    coin_images = MockImages()
    master = MockMaster()

    # Create animator
    animator = CoinAnimator(coin_labels, coin_images, master)
    print("✓ CoinAnimator created successfully")

    # Test line value to coin display conversion
    test_cases = {
        6: [14, 14, 14],  # old yin
        7: [14, 14, 15],  # young yang
        8: [14, 15, 15],  # young yin
        9: [15, 15, 15],  # old yang
    }

    for line_val, expected in test_cases.items():
        result = animator._line_value_to_coin_display(line_val)
        assert result == expected, f"Failed for line {line_val}: got {result}, expected {expected}"
        print(f"✓ Line value {line_val} maps correctly to {result}")

    # Test clearing coins
    animator.clear_coins()
    for i, label in enumerate(coin_labels):
        assert label.image == 16, f"Coin {i} not cleared (image={label.image})"
    print("✓ Clear coins works")

    # Test initial coin state
    animator.set_coins_initial()
    for i, label in enumerate(coin_labels):
        assert label.image == 0, f"Coin {i} not set to initial (image={label.image})"
    print("✓ Set coins initial works")

    # Test animation with mock reading (won't actually animate, just test logic)
    reading = MockReading()
    print("✓ Mock reading created with line_values:", reading.primary.line_values)

    # Note: We can't fully test animate_full_reading without time.sleep mocking
    # but we can verify it doesn't crash
    try:
        # Set delay to 0 to speed up test
        animator.animate_full_reading(reading, delay=0, spins=1, pause_between_lines=0)
        print("✓ Full reading animation logic executes without errors")
    except Exception as e:
        print(f"✗ Animation failed: {e}")
        raise

    print("\n✅ All CoinAnimator tests passed!")


if __name__ == '__main__':
    test_coin_animator()
