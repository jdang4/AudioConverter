def separateFileName(s):
	lastIndex = s.rindex('.')

	if lastIndex == -1:
		return None, None 

	filename = s[:lastIndex]
	filetype = s[lastIndex+1:]

	return filename, filetype