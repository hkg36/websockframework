import sys
def LevenshteinDistance(s, t):
    if (s == t):
        return 0
    if (len(s) == 0):
        return t.Length;
    if (len(t) == 0):
        return s.Length;

    v0 = [0]*(len(t) + 1);
    v1 = [0]*(len(t) + 1);
    for i in xrange(len(v0)):
        v0[i] = i

    for i in xrange(len(s)):
        v1[0] = i + 1;
        for j in xrange(len(t)):
            cost = 0 if s[i] == t[j] else 1
            #                     del         add              modify
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)

        v2=v0
        v0=v1
        v1=v2

    return v0[len(t)];

def LevenshteinDistance2(s,t):
    m=len(s)
    n=len(t)
    d=[[0]*(n+1) for i in xrange(m+1)]

    for i in xrange(1,m+1):
        d[i][0] = i

    for j in xrange(1,n+1):
        d[0][ j] = j

    for j in xrange(1,n+1):
      for i in xrange(1,m+1):
          if s[i-1] == t[j-1]:
              d[i][j] = d[i-1][ j-1]
          else:
              d[i][j] = min(
                      d[i-1][j],# a deletion
                      d[i][j-1],  # an insertion
                      d[i-1][j-1]  # a substitution
                )+1
    for one in d:
        print one
    i=0
    j=0
    while i<m and j<n:
        now=d[i][j]
        delete=d[i+1][j]
        replace=d[i+1][j+1]
        insert=d[i][j+1]

        if replace<=delete and replace<=insert:
            j+=1
            i+=1
            if now==replace:
                print((i,j,'kep',s[i-1]))
            else:
                print((i,j,'rep',s[i-1],t[j-1]))

        elif delete<=insert:
            i+=1
            print((i,j,'del',s[i-1]))

        else:
            j+=1
            print((i,j,'add',t[j-1]))

    return d[m][n]


a='Sunday'
b='Saturday'
print len(a)
print len(b)
print LevenshteinDistance2(a,b)
print LevenshteinDistance(a,b)
