import pytest
from src.api.battle import calculate_score

def test_calculate_score_basic():
    # Basic test with known values
    result = calculate_score(opposing_health=100, strength=10, speed=2, votes=0)
    expected = 100 / (10 * 2) * (0.9 ** 0)
    assert result == pytest.approx(expected)

def test_calculate_score_with_votes():
    # Test with votes affecting the score
    result = calculate_score(opposing_health=100, strength=10, speed=2, votes=3)
    expected = 100 / (10 * 2) * (0.9 ** 3)
    assert result == pytest.approx(expected)

def test_calculate_score_zero_votes():
    # Score should be highest with zero votes
    score_zero = calculate_score(100, 10, 2, 0)
    score_one = calculate_score(100, 10, 2, 1)
    assert score_one < score_zero

def test_calculate_score_high_votes():
    # More votes should lower the score
    score_low_votes = calculate_score(100, 10, 2, 2)
    score_high_votes = calculate_score(100, 10, 2, 10)
    assert score_high_votes < score_low_votes

def test_calculate_score_different_stats():
    # Changing stats should affect the score
    score1 = calculate_score(100, 10, 2, 0)
    score2 = calculate_score(200, 10, 2, 0)
    assert score2 > score1

def test_calculate_score_zero_strength_or_speed():
    # Should raise ZeroDivisionError if strength or speed is zero
    with pytest.raises(ZeroDivisionError):
        calculate_score(100, 0, 2, 0)
    with pytest.raises(ZeroDivisionError):
        calculate_score(100, 10, 0, 0)