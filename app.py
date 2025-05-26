def get_sequence(n):
    sequence = [n]
    curr = n  
    while curr != 1:
        if curr % 2 == 0:
            curr = curr // 2
        else:
            curr = 3 * curr + 1
        sequence.append(curr)
    sequence.reverse()
    return sequence

print(get_sequence(100))