def set_brightness(color, brightness):
    """
    Scales a color a new brightness (0 to 255)
    """
    if brightness < 0 or brightness > 255:
        raise ValueError('Brightness {} is invalid.'.format(brightness))
    average = float(sum(color))/len(color)
    if average == 0:
        return [0, 0, 0]
    return map(int, [c / average * brightness for c in color])
