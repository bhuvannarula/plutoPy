def deadband(y_new, y_old, dead):
    if abs(y_new - y_old) <= dead:
        return y_old
    else:
        return y_new