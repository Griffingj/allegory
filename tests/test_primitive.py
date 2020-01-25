from src.python.primitive import LruMap


def test_lru_map():
    lruMap = LruMap(3)
    lruMap.put("a", "apple")
    lruMap.put("b", "banana")
    lruMap.put("c", "cranberry")
    assert lruMap.length == 3
    assert lruMap.get("a") == "apple"
    assert lruMap.get("b") == "banana"
    assert lruMap.get("c") == "cranberry"
    lruMap.put("d", "date")
    assert lruMap.get("d") == "date"
    assert lruMap.get("a", "or_else") == "or_else"
    # refresh b, now c last
    assert lruMap.get("b") == "banana"
    lruMap.put("e", "eggfruit")
    assert lruMap.get("c", "or_else") == "or_else"
    assert lruMap.get("b") == "banana"
    assert lruMap.length == 3
    lruMap.put("c", "cranberry")
    assert lruMap.dll.pop().val == "cranberry"
    assert lruMap.dll.pop().val == "banana"
    assert lruMap.dll.pop().val == "eggfruit"
    assert lruMap.dll.l_head is None
    assert lruMap.dll.r_head is None
