def calculate_luminance(rgb=(0,0,0)):
	new_rgb = (0,0,0)
	for i,v in enumerate(rgb):
		v = v/255
		if v <= 0.04045:
			v = v/12.92
		else:
			v = ((v+0.055)/1.055)**2.4
		lst = list(new_rgb)
		lst[i] = v
		new_rgb = tuple(lst)
	luminance = 0.2126*new_rgb[0] + 0.7152*new_rgb[1] + 0.0722*new_rgb[2]
	return luminance

print(calculate_luminance((255,255,255)))
