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

    max_step=d[m][n]
    rount=[]
    checked=set()
    def findnextrount(i,j,rount):
        if (i,j) in checked:
            return False
        checked.add((i,j))
        if i==m and j==n:
            return True
        if i==m or j==n:
            return False
        now=d[i][j]
        if now>max:
            return False
        delete=d[i+1][j]
        replace=d[i+1][j+1]
        insert=d[i][j+1]

        if replace>=now:
            if findnextrount(i+1,j+1,rount):
                if now==replace:
                    rount.insert(0,(i,j,'keep',s[i]))
                else:
                    rount.insert(0,(i,j,'replace',s[i],t[j]))
                return True
        if delete>now:
            if findnextrount(i+1,j,rount):
                rount.insert(0,(i,j,'delele',s[i]))
                return True
        if insert>now:
            if findnextrount(i,j+1,rount):
                rount.insert(0,(i,j,'add',t[j]))
                return True
        return False
    findnextrount(0,0,rount)
    return max_step,d,rount


a='Sunday'
b='Saturday'
data= LevenshteinDistance2(a,b)
for one in data[1]:
    print one
for one in data[2]:
    print(one)
print data
print LevenshteinDistance(a,b)
