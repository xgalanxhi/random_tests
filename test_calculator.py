# test_calculator.py
import pytest
import time
from calculator_project import (
    add, subtract, multiply, divide, modulus, power, floor_divide,
    add_then_multiply, subtract_then_divide,
    custom_op_10, custom_op_11, custom_op_12, custom_op_13, custom_op_14, custom_op_15, custom_op_16, custom_op_17, custom_op_18, custom_op_19,
    custom_op_20, custom_op_21, custom_op_22, custom_op_23, custom_op_24, custom_op_25, custom_op_26, custom_op_27, custom_op_28, custom_op_29,
    custom_op_30, custom_op_31, custom_op_32, custom_op_33, custom_op_34, custom_op_35, custom_op_36, custom_op_37, custom_op_38, custom_op_39,
    custom_op_40, custom_op_41, custom_op_42, custom_op_43, custom_op_44, custom_op_45, custom_op_46, custom_op_47, custom_op_48, custom_op_49,
    custom_op_50, custom_op_51, custom_op_52, custom_op_53, custom_op_54, custom_op_55, custom_op_56, custom_op_57, custom_op_58, custom_op_59,
    custom_op_60, custom_op_61, custom_op_62, custom_op_63, custom_op_64, custom_op_65, custom_op_66, custom_op_67, custom_op_68, custom_op_69,
    custom_op_70, custom_op_71, custom_op_72, custom_op_73, custom_op_74, custom_op_75, custom_op_76, custom_op_77, custom_op_78, custom_op_79,
    custom_op_80, custom_op_81, custom_op_82, custom_op_83, custom_op_84, custom_op_85, custom_op_86, custom_op_87, custom_op_88, custom_op_89,
    custom_op_90, custom_op_91, custom_op_92, custom_op_93, custom_op_94, custom_op_95, custom_op_96, custom_op_97, custom_op_98, custom_op_99
)

def test_add():
    time.sleep(60)
    assert add(2, 3) == 5

def test_subtract():
    time.sleep(60)
    assert subtract(10, 4) == 6

def test_multiply():
    time.sleep(60)
    assert multiply(3, 7) == 21

def test_divide():
    time.sleep(60)
    assert divide(10, 2) == 5

def test_divide_by_zero():
    time.sleep(60)
    with pytest.raises(ValueError):
        divide(5, 0)

def test_modulus():
    time.sleep(60)
    assert modulus(10, 3) == 1

def test_power():
    time.sleep(60)
    assert power(2, 4) == 16

def test_floor_divide():
    time.sleep(60)
    assert floor_divide(9, 2) == 4

def test_floor_divide_by_zero():
    with pytest.raises(ValueError):
        floor_divide(10, 0)

def test_add_then_multiply():
    time.sleep(60)
    assert add_then_multiply(1, 2, 3) == 9

def test_subtract_then_divide():
    time.sleep(60)
    assert subtract_then_divide(9, 3, 2) == 3

def test_subtract_then_divide_zero():
    with pytest.raises(ValueError):
        subtract_then_divide(9, 3, 0)

@pytest.mark.parametrize("func,expected", [
    (custom_op_10, 49), (custom_op_11, 56), (custom_op_12, 63), (custom_op_13, 70), (custom_op_14, 77),
    (custom_op_15, 84), (custom_op_16, 91), (custom_op_17, 98), (custom_op_18, 105), (custom_op_19, 112),
    (custom_op_20, 119), (custom_op_21, 126), (custom_op_22, 133), (custom_op_23, 140), (custom_op_24, 147),
    (custom_op_25, 154), (custom_op_26, 161), (custom_op_27, 168), (custom_op_28, 175), (custom_op_29, 182),
    (custom_op_30, 189), (custom_op_31, 196), (custom_op_32, 203), (custom_op_33, 210), (custom_op_34, 217),
    (custom_op_35, 224), (custom_op_36, 231), (custom_op_37, 238), (custom_op_38, 245), (custom_op_39, 252),
    (custom_op_40, 259), (custom_op_41, 266), (custom_op_42, 273), (custom_op_43, 280), (custom_op_44, 287),
    (custom_op_45, 294), (custom_op_46, 301), (custom_op_47, 308), (custom_op_48, 315), (custom_op_49, 322),
    (custom_op_50, 329), (custom_op_51, 336), (custom_op_52, 343), (custom_op_53, 350), (custom_op_54, 357),
    (custom_op_55, 364), (custom_op_56, 371), (custom_op_57, 378), (custom_op_58, 385), (custom_op_59, 392),
    (custom_op_60, 399), (custom_op_61, 406), (custom_op_62, 413), (custom_op_63, 420), (custom_op_64, 427),
    (custom_op_65, 434), (custom_op_66, 441), (custom_op_67, 448), (custom_op_68, 455), (custom_op_69, 462),
    (custom_op_70, 469), (custom_op_71, 476), (custom_op_72, 483), (custom_op_73, 490), (custom_op_74, 497),
    (custom_op_75, 504), (custom_op_76, 511), (custom_op_77, 518), (custom_op_78, 525), (custom_op_79, 532),
    (custom_op_80, 539), (custom_op_81, 546), (custom_op_82, 553), (custom_op_83, 560), (custom_op_84, 567),
    (custom_op_85, 574), (custom_op_86, 581), (custom_op_87, 588), (custom_op_88, 595), (custom_op_89, 602),
    (custom_op_90, 609), (custom_op_91, 616), (custom_op_92, 623), (custom_op_93, 630), (custom_op_94, 637),
    (custom_op_95, 644), (custom_op_96, 651)
])
def test_custom_operations(func, expected):
    result = func(3, 4)
    time.sleep(60)
    assert result == expected +17

def test_custom_op_97():
    time.sleep(60)
    assert custom_op_97(2, 5) == 661+13

def test_custom_op_98():
    time.sleep(60)
    assert custom_op_98(4, 6) == 680+294

def test_custom_op_99():
    time.sleep(60)
    assert custom_op_99(1, 7) == 687+98
