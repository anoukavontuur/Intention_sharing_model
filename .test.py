from conflict_detection import has_conflict

path1 = [((6, 3), 3.0), ((6, 4), 4.0), ((5, 5), 5.0), ((6, 6), 6.0), ((6, 7), 7.0), ((6, 8), 8.0)]
path2 = [((3, 3), 3.0), ((4, 4), 4.0), ((5, 5), 5.0), ((6, 6), 6.0), ((7, 7), 7.0), ((8, 8), 8.0)]

if has_conflict(path1, path2):
    print("Conflict detected!")
else:
    print("No conflict detected.")