def separateFileName(s):
    lastIndex = s.rindex('.')
    
    if lastIndex == -1:
        return None, None 
    
    index = s.index('/')
    
    filename = s[index+1:lastIndex]
    filetype = s[lastIndex+1:]
    
    return filename, filetype